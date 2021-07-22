from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import views
from django.contrib.auth import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Post, Featured, Reservation, Dog, Article
from django.utils import timezone
import datetime
from .forms import RegistrationForm, ProductReservationForm
from django.urls import reverse_lazy
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout


class indexView(generic.ListView):
    template_name = 'webapp/index.html'
    model = Featured

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class profileView(LoginRequiredMixin, generic.ListView):
    login_url = 'webapp:login'
    template_name = 'webapp/profile.html'
    model = Reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['reservas_disponibles'] = 3 - \
            len(Reservation.objects.filter(
                type='D', user=self.request.user, status='A'))
        product_prices = []
        res = Reservation.objects.filter(user=self.request.user, status='A')
        for r in res:
            if r.type == 'P':
                product_prices.append(r.quantity * r.post.product.price)
            else:
                product_prices.append(0)
        context['product_prices'] = product_prices
        print(product_prices)
        return context

    def get_queryset(self):
        """ Queryset """
        if self.request.user.is_authenticated:
            return Reservation.objects.filter(user=self.request.user, status='A')


class profile_configView(LoginRequiredMixin, generic.edit.UpdateView):
    login_url = 'webapp:login'
    model = User
    fields = ['first_name', 'last_name']
    template_name = 'webapp/user_update_form.html'
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('webapp:profile')


class petsView(generic.ListView):
    template_name = 'webapp/pets_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            i = self.kwargs['index']
            if i < 0:
                i = 1
            if i > len(Post.objects.filter(type='D'))//8 + 1:
                i = 1
            context['index'] = i
        except Exception as e:
            context['index'] = 1
        try:
            #context['total_objects'] = [i for i in range(50)]
            context['total_objects'] = [i for i in range(
                len(Post.objects.filter(type='D'))//8 + 1)]
            print("context buscado")
            print("mascotas: ", context['total_objects'])
        except Exception as e:
            print("Exception in petsView", e)
            context['total_objects'] = []
        return context

    def get_queryset(self):
        """ Queryset """
        try:
            i = self.kwargs['index']
        except:
            i = 1
        posts = Post.objects.filter(type='D')
        print("POSTS: ", posts)
        print("Test POSTS: ", Post.objects.all())
        post_list = []
        for p in posts:
            if p.dog.status == 'Disponible' or p.dog.status == 'Reservado':
                post_list.append(p)
        if len(posts) > 8:
            if i < 0:
                i = 1
            if i > len(post_list)//8 + 1:
                i = 1
            try:
                return post_list[(i-1)*8:i*8]
            except:
                print('Error')
                return []
        return post_list[:8]


class detail_petView(generic.DetailView):
    template_name = 'webapp/pet_details.html'
    model = Dog
    context_object_name = 'pet'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['edad'] = timezone.now().year - \
            Dog.objects.filter(pk=1)[0].birthdate.year
        return context


def detail_product(request, pk, success=''):
    context = {}
    post = get_object_or_404(Post, pk=pk)
    context['post'] = post
    form = ProductReservationForm()
    if request.method == 'POST':
        form = ProductReservationForm(request.POST)
        if form.is_valid():
            if post.type == 'P':
                q = form.cleaned_data['quantity']
                if q <= post.product.stock:
                    r = None
                    try:
                        r = Reservation.objects.get(post__product=post.product)
                    except Exception as e:
                        print(e)
                        pass
                    if r:
                        reservation = r
                        reservation.quantity = reservation.quantity + q
                    else:
                        reservation = Reservation(
                            user=request.user,
                            post=post,
                            quantity=q,
                            type='P',
                            status='A',
                            reservation_date=timezone.now() - datetime.timedelta(hours=4)
                        )
                    reservation.save()
                    reservation.post.product.stock = post.product.stock - q
                    reservation.post.product.save()
                else:
                    form.add_error(
                        'quantity', 'La cantidad ingresada es superior al total de productos disponibles')
                    context['form'] = form
                    return render(request, 'webapp/product_details.html', context)
            return HttpResponseRedirect(reverse('webapp:product_details', kwargs={
                'pk': post.id,
                'success': 'reservacion exitosa'
            }))
    context['form'] = form
    context['success'] = success
    return render(request, 'webapp/product_details.html', context)


class detail_productView(generic.DetailView):
    template_name = 'webapp/product_details.html'
    model = Post
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class productsView(generic.ListView):
    template_name = 'webapp/products_list.html'
    context_object_name = 'object_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            i = self.kwargs['index']
            if i < 0:
                i = 1
            if i > len(Post.objects.filter(type='P'))//8 + 1:
                i = 1
            context['index'] = i
        except Exception as e:
            context['index'] = 1
        try:
            #context['total_objects'] = [i for i in range(50)]
            context['total_objects'] = [i for i in range(
                len(Post.objects.filter(type='P'))//8 + 1)]

        except:
            context['total_objects'] = []
        return context

    def get_queryset(self):
        """ Queryset """
        try:
            i = self.kwargs['index']
        except:
            i = 1
        posts = Post.objects.filter(type='P')
        if len(posts) > 8:
            if i < 0:
                i = 1
            if i > len(posts)//8 + 1:
                i = 1
            try:
                return Post.objects.filter(type='P')[(i-1)*8:i*8]
            except:
                print('Error')
        else:
            return Post.objects.filter(type='P')[:8]


def search(request, busqueda=''):
    context = {}
    query1 = []
    query2 = []
    try:
        search = request.POST['search']
    except Exception as e:
        print(e)
    try:
        query1 = Post.objects.filter(dog__name__istartswith=search)
        print(query1)
    except Exception as e:
        print(e)
    try:
        query2 = Post.objects.filter(product__name__istartswith=search)
        print(query2)
    except Exception as e:
        print(e)
    context['result1'] = query1
    context['result2'] = query2
    return render(request, 'webapp/search.html', context)


@login_required(login_url='webapp:login')
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['new_password2'])
            request.user.save()
            return HttpResponseRedirect(reverse('webapp:profile'))
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'webapp/change_pw.html', {'form': form})


@login_required(login_url='webapp:login')
def reservation(request, post_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            dog = get_object_or_404(Dog, pk=post_id)
            post = Post.objects.get(dog=dog)
            print(post)
            try:
                if post.type == 'P':
                    raise ValueError('Error producto')
                elif post.type == 'D':
                    if len(Reservation.objects.filter(user=request.user, type='D')) < 3:
                        reservation = Reservation(
                            user=request.user,
                            post=post,
                            type='D',
                            status='A',
                            reservation_date=timezone.now() - datetime.timedelta(hours=4)
                        )
                        reservation.save()
                        dogy = post.dog
                        dogy.status = 'Reservado'
                        dogy.save()
                    else:
                        return render(request, 'webapp/error_reservation.html', {
                            'reservation_title': 'Ha superado el numero maximo de reservas',
                            'reservation_text': 'Debera relizar el proceso de compra en nuestras instalaciones para concretar sus reservas anteriores',
                            'reservation_footer': 'O puede esperar a que el plazo de validez de la reserva finalice el cual es de 24 horas.'
                        })
            except ValueError as e:
                return render(request, 'webapp/error_reservation.html', {
                    'reservation_title': "La cantidad a reservar debe ser un numero entero positivo",
                })
            except Warning as e:
                return render(request, 'webapp/error_reservation.html', {
                    'reservation_title': e,
                })
            except Exception as e:
                print(e)
                return render(request, 'webapp/error_reservation.html', {
                    'reservation_title': 'Ha ocurrido un error inesperado al intentar realizar la reserva',
                })

            return HttpResponseRedirect(reverse('webapp:success_reservation'))
        else:
            return HttpResponseRedirect(reverse('webapp:products'))
    else:
        return HttpResponseRedirect(reverse('webapp:login'))


def success_reservation(request):
    return render(request, 'webapp/success_reservation.html', {})


def remove_reservation(request, res_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            reservation = get_object_or_404(Reservation, pk=res_id)
            try:
                if reservation.type == 'D':
                    reservation.post.dog.status = 'Disponible'
                    reservation.post.dog.save()
                    print('Estado del perro actualizado')
                elif reservation.type == 'P':
                    aux = reservation.post.product.stock
                    reservation.post.product.stock = aux + reservation.quantity
                    reservation.post.product.save()
                    print('Cantidad en stock actualizada de {} a {}'.format(
                        aux, reservation.quantity+aux))
                reservation.delete()
                print('Reservacion eliminada')
            except Exception as e:
                print(e)
                pass
            return HttpResponseRedirect(reverse('webapp:profile'))
        else:
            return HttpResponseRedirect(reverse('webapp:profile'))
    else:
        return HttpResponseRedirect(reverse('webapp:login'))


def contactView(request):
    context = {
        'telf': '02611234567',
        'direction': 'Av 5 de julio frente a la ferreteria pernoInc. Maracaibo-Zulia',
        'emails': 'northveterinarianclinic@example.com, clinicaveterinariadelnorte@ejemplo.com',
    }
    return render(request, 'webapp/contact.html', context)


def signin(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email']
            )
            return HttpResponseRedirect(reverse('webapp:sucess_signin'))
    else:
        form = RegistrationForm()
    return render(request, 'webapp/signin.html', {'form': form})


def sucess_signin(request):
    return render(request, 'webapp/sucess_regist.html', {
        'output': 'Usuario registrado exitosamente'
    })
