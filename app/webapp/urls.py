from django.urls import path, re_path
from . import views
from django.contrib.auth import views as auth_views

app_name='webapp'
urlpatterns = [
       path('', views.indexView.as_view(), name='index'),
       path('buscar/', views.search, name='search'),
       path('buscar/<busqueda>', views.search, name='search'),
       path('perfil/', views.profileView.as_view(), name='profile'),
       path('perfil/configuracion/<pk>', views.profile_configView.as_view(), name='profile_config'),
       path('perfil/configuracion/contrasenia/', views.change_password, name='change_pw'),
       path('perfil/remove/<int:res_id>', views.remove_reservation, name='remove_reservation'),
       path('productos/', views.productsView.as_view(), name='products'),
       path('productos/<int:index>/', views.productsView.as_view(), name='products'),
       path('productos/detalles/<int:pk>', views.detail_product, name='product_details'),
       path('productos/detalles/<int:pk>/<success>', views.detail_product, name='product_details'),
       path('mascotas/', views.petsView.as_view(), name='pets'),
       path('mascotas/<int:index>/', views.petsView.as_view(), name='pets'),
       path('mascotas/detalles/<pk>', views.detail_petView.as_view(), name='pet_details'),
       path('reservacion/<int:post_id>/', views.reservation, name='reservation'),
       path('reservacion/exitosa/', views.success_reservation, name='success_reservation'),
       path('contacto/', views.contactView, name='contact'),
       path('sucess_signin/', views.sucess_signin, name='sucess_signin'),
       path('registrarse/', views.signin, name='signin'),
       path('ingresar/', auth_views.LoginView.as_view(template_name='webapp/login.html'), name='login'),
       path('desconectar/', auth_views.LogoutView.as_view(template_name='webapp/logout.html',next_page='webapp:index'), name='logout'),
       path('restablecer_contraseña/', views.indexView, name='password_reset'),
    ]
