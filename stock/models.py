from random import choices
from django.db import models
from django.contrib.auth.models import User


class UpdateCreate(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=25)

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Product(UpdateCreate):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(
        Brand, on_delete=models.CASCADE, related_name='b_products')
    stock = models.SmallIntegerField(blank=True, null=True)

    def __str__(self):
        return self.name


class Firm(UpdateCreate):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class Transaction(UpdateCreate):
    TRANSACTION = (
        (1, 'IN'),
        (0, 'OUT')
    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    firm = models.ForeignKey(
        Firm, on_delete=models.SET_NULL, null=True, related_name='transactions')
    transaction = models.SmallIntegerField(choices=TRANSACTION)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='transaction')
    quantity = models.SmallIntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_total = models.DecimalField(max_digits=8, decimal_places=2, blank=True)

    def __str__(self):
        return f'{self.transaction} - {self.product} - {self.quantity}'

# Modelimize ürün fiyatını belirlemek için price alanını düşünelim. Fiyatlar ondalık sayılardan oluşmaktadır. 10 lira 25 kuruş gibi. Ondalık sayılar için Float Field ve Decimal Field kullanılan alan tipleridir. Bunların ana farkı Float Field küçük sayıları ile Decimal Fieldin daha büyük sayıları kabul etmesidir.Float Fieldin en fazla alabileceği basamak adedi 7 dir ve veritabanında 4 byte yer kaplar.Decimal Fieldin ise alabileceği en fazla basamak 29 dur. Veritabanında 16 byte yer kaplar. Decimal Fieldın diğer bir farkıda basamak sayısının ve ondalık kısımın sırlandırılabilir olmasıdır. Decimal Field max_digits ve decimal_places argümanlarını alır. max_digits maksimum izin verilen basamak sayısıdır. decimal_places ise kullanılacak ondalık basamak sayısıdır. decimal_places, max_digits'den büyük olamaz.