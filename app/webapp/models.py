from django.db import models
from django.contrib.auth.models import User
import datetime

class Postable(models.Model):
    name = models.CharField(max_length=45, null=False)
    img_url = models.CharField(max_length=64, null=False)
    price = models.IntegerField(null=False)
    description = models.CharField(max_length=255, null=False)
    class Meta:
        abstract = True

class Dog(Postable):
    TYPES = (
        ('Disponible', 'Disponible'),
        ('Reservado', 'Reservado'),
        ('Vendido','Vendido')
    )
    race = models.CharField(max_length=45, null=False)
    gender = models.CharField(max_length=1, null=False)
    birthdate = models.DateTimeField(null=False)
    status = models.CharField(max_length=45, null=False, choices=TYPES)
    def __str__(self):
        return super().name

    def get_age(self):
        today = datetime.date.today()
        return (today.year - self.birthdate.year) - int( (today.month, today.day) <
        (self.birthdate.month, self.birthdate.day))
        pass

class Article(Postable):
    TYPES = (
        ('C', 'Comestibles'),
        ('S', 'Atuendos'),
        ('A', 'Accesorios'),
        ('O', 'Otros')
    )
    stock = models.IntegerField(default=1,null=False)
    category = models.CharField(max_length=1, null=False, default='O', choices=TYPES)
    def __str__(self):
        return super().name
    pass

class Post(models.Model):
    TYPES = (
        ('D', 'Dog'),
        ('P', 'Product'),
    )
    dog = models.OneToOneField(Dog, on_delete=models.CASCADE, blank=True, null=True)
    product = models.OneToOneField(Article, on_delete=models.CASCADE, blank=True, null=True)
    type = models.CharField(max_length=1, choices=TYPES)# D - DOG // P - Product
    def __str__(self):
        if self.type == 'D':
            return 'Dog {0} - {1}'.format(self.id,self.dog.name)
        else:
            return 'Product {0} - {1}'.format(self.id,self.product.name)
    pass

class Reservation(models.Model):
    TYPES = (
        ('D', 'Dog'),
        ('P', 'Product'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, default=None)
    quantity = models.IntegerField(default=1, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, default=None)
    type = models.CharField(max_length=1, choices=TYPES)# D - DOG // P - Product
    status = models.CharField(max_length=1, choices=(('A','Activa'),('F','Finalizada')), blank=True, null=True)
    reservation_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        if self.type == 'D':
            return 'Dog: {0} --> Usuario: {1}'.format(self.post.dog.name, self.user.email)
        else:
            return 'Producto: {0} --> Usuario: {1}'.format(self.post.product.name, self.user.email)

class Featured(models.Model):
    TYPES = (
        ('C', 'Carousel'),
    )
    feature = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, default=None)
    type = models.CharField(max_length=1, choices=TYPES)# C - carousel
    def __str__(self):
        if self.feature.type == 'D':
            return 'Feature {0} -> {1}'.format(self.type, self.feature.dog.name)
        if self.feature.type == 'P':
            return 'Feature {0} -> {1}'.format(self.type, self.feature.product.name)
    pass
