# <center> 🛒 DJANGO-STOCK-MANAGAMENT-API 🛒 </center>

## <center> ************************************** </center>

# <center> 🚀 INITIAL SETUP </center>

```bash
# CREATING VIRTUAL ENVIRONMENT
# windows 👇
python -m venv env
# linux / Mac OS 👇
vitualenv env

# ACTIVATING ENVIRONMENT
# windows 👇
source env/Scripts/activate
# linux / Mac OS 👇
source env/bin/activate

# PACKAGE INSTALLATION
# if pip does not work try pip3 in linux/Mac OS
pip install djangorestframework
pip freeze > requirements.txt
django-admin startproject main .
# alternatively python -m pip install django
pip install python-decouple
django-admin --version
```

```bash
# 💨 If you already have a requirement.txt file, you can install the packages in the file
# 💨 by entering the following commands respectively in the terminal 👇
1-python -m venv env
2-source env/Scripts/activate
3-pip install -r requirements.txt 🚀
4-python.exe -m pip install --upgrade pip
5-python manage.py migrate
6-python manage.py createsuperuser
7-python manage.py runserver
```

## 🛑 Secure your project

## 🚩 .gitignore

✔ Add a ".gitignore" file at same level as env folder, and check that it includes ".env" and /env lines.

🔹 Do that before adding your files to staging area, else you will need extra work to unstage files to be able to ignore them.

🔹 [On this page](https://www.toptal.com/developers/gitignore) you can create "gitignore files" for your projects.

## 🚩 Python Decouple

💻 To use python decouple in this project, first install it 👇

```bash
pip install python-decouple
```

💻 Go to terminal to update "requirements.txt"  👇

```bash
pip freeze > requirements.txt
```

✔ Create a new file and name as ".env" at same level as env folder

✔ Copy your SECRET_KEY from settings.py into this .env file. Don't forget to remove quotation marks and blanks from SECRET_KEY

```python
SECRET_KEY=-)=b-%-w+0_^slb(exmy*mfiaj&wz6_fb4m&s=az-zs!#1^ui7j
```

✔ Go to "settings.py", make amendments below 👇

```python
from decouple import config

SECRET_KEY = config('SECRET_KEY')
```

## 💻 INSTALLING DJANGO REST

💻 Go to terminal 👇

```bash
python manage.py makemigrations
python manage.py migrate
pip install djangorestframework
```

✔ Go to "settings.py" and add 'rest_framework' app to INSTALLED_APPS

## 💻 PostgreSQL Setup

💻 To get Python working with Postgres, you will need to install the “psycopg2” module👇

```bash
pip install psycopg2
```

💻 Go to terminal to update requirements.txt  👇

```bash
pip freeze > requirements.txt
```

✔ Go to settings.py and add '' app to INSTALLED_APPS

## 💻 MIGRATE 👇

```bash
python manage.py migrate
```

## 🚀 RUNSERVER 👇

```bash
python manage.py runserver
```

# <center> ✏ This is the end of initial setup ✏ </center>

## <center> ****************************************************** </center>

# <center> 🚀 AUTHENTICATION </center>

## 🚩 ADDING AN APP

💻 Go to terminal 👇

```bash
python manage.py startapp account
```

✔ Go to "settings.py" and add 'account' App to "INSTALLED_APPS"

## 💻 INSTALL [DJ-REST-AUTH](https://dj-rest-auth.readthedocs.io/en/latest/)

```bash
pip install dj-rest-auth
```

💻 Go to terminal to update "requirements.txt"  👇

```bash
pip freeze > requirements.txt
```

## 🚩 Add "dj_rest_auth" app to "INSTALLED_APPS" in your django "settings.py" 👇

```python
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
```

## 🚩 Go to "main/urls.py" and add the path 👇

```python
path('account/', include('account.urls'))
```

## ✔ Create "urls.py" file under "account" App 👇

## 🚩 Go to "account/urls.py" and add 👇

```python
from django.urls import path, include

urlpatterns = [
    path('auth/', include('dj_rest_auth.urls')),
]
```

## 💻 Migrate your database

```bash
python manage.py migrate
```

## ✔ Create "serializers.py" file under "account" App and add 👇

```python
from rest_framework import serializers, validators
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from dj_rest_auth.serializers import TokenSerializer


class RegisterSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(
        required=True,
        validators=[validators.UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={"input_type": "password"}
    )

    password2 = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        ]

        extra_kwargs = {
            "password": {"write_only": True},
            "password2": {"write_only": True}
        }
    #! To create a user when the user is registered 👇
    def create(self, validated_data):
        password = validated_data.get("password")
        validated_data.pop("password2")

        user = User.objects.create(**validated_data)
        user.password = make_password(password)
        user.save()
        return user

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError(
                {"password": "Password fields didn't match."})
        return data
```

## 🚩 Go to "views.py" and write RegisterVİew() 👇

```python
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import RegisterSerializer


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User dont have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

```

## 🚩 Go to "urls.py" and add the path 👇

```python
from .views import RegisterView

path('register/', RegisterView.as_view()),
```

## 🚩 Create "signals.py" under "account" App and add 👇

```python
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
```

## 🚩 For the "signal.py" file to work, we need to add the "ready" method to the "apps.py" file 👇

```python
def ready(self) -> None:
    import users.signals
```

## 🚩 Go to "views.py" and customize RegisterView()👇

```python
from django.contrib.auth.models import User
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status

from .serializers import RegisterSerializer

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    #! When user register 👉 "username", "email","first_name","last_name" and "token" will be returned. 👇
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = serializer.data
        if Token.objects.filter(user=user).exists():
            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data['error'] = 'User dont have token. Please login'
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)
```

## 🚩 Override TokenSerializer() 👇

```python
from dj_rest_auth.serializers import TokenSerializer

#! We need to override the TokenSerializer to return all user data in a single request.
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name')


class CustomTokenSerializer(TokenSerializer):

    user = UserTokenSerializer(read_only=True)

    class Meta(TokenSerializer.Meta):
        fields = ('key', 'user')
```

## 🚩 Go to "settings.py" and add 👇

```python
REST_AUTH_SERIALIZERS = {
    'TOKEN_SERIALIZER': 'account.serializers.CustomTokenSerializer',
}
```

## <center> ****************************************************** </center>

## 🚩 ADDING APP

💻 Go to terminal 👇

```bash
python manage.py startapp stock
```

✔ Go to "settings.py" and add 'stock' App to "INSTALLED_APPS"

## 🚩 Go to "main/urls.py" and add path 👇

```python
 path('stock/', include('stock.urls')),
```

## 🚩 Go to "models.py" under "stock" App and create models 👇

```python
from itertools import product
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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='b_products')
    stock = models.SmallIntegerField(blank=True, null=True)
    #! We used SmallIntegerField to take up less space in the database 👆

    def __str__(self):
        return self.name

class Firm(UpdateCreate):
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Transaction(UpdateCreate):
    TRANSACTIONS = (
        ("1", "IN"),
        ("0", "OUT"),
    )
    #! When you say SET_NULL, it is necessary to write "null=True". When the user is deleted, that field in db will remain null 👇
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    firm = models.ForeignKey(Firm, on_delete=models.SET_NULL, null=True, related_name='transactions')
    #! SmallntegerField accepts numbers from -32768 to 32767 👇
    transaction = models.SmallIntegerField(choices=TRANSACTIONS)
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='transaction')
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_total = models.DecimalField(max_digits=6, decimal_places=2, blank=True)

    #? 👆 Let's consider the price field to determine the product price for our model. Prices are in decimals. 10 lira is like 25 cents. "Float Field" and "Decimal Field" are the field types used for decimal numbers. The main difference of these is that Float Field accepts small numbers and "Decimal Field" accepts larger numbers. The maximum number of digits that Float Field can take is 7 and it occupies 4 bytes in the database. The maximum digit that Decimal Field can take is 29. It takes 16 bytes of space in the database. Another difference of Decimal Field is that the number of digits and the decimal part can be glazed. Decimal Field takes the max_digits and decimal_places arguments. max_digits is the maximum number of digits allowed. decimal_places is the number of decimal places to use. decimal_places cannot be greater than max_digits.
    def __str__(self):
        return f'{self.transaction} - {self.product} - {self.quantity}'
```

## 💻 Migrate your database 👇

```bash
python manage.py migrate
```

## 🚩 Go to "admin.py" and register the models 👇

```python
from django.contrib import admin

from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

admin.site.register(Category)
admin.site.register(Brand)
admin.site.register(Product)
admin.site.register(Firm)
admin.site.register(Transaction)
```

## 🚩 Create  "signals.py" file under "stock" App and add 👇

```python
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from .models import Transaction, Product

#! We are doing database related operations here, so we can return the warning message from serializers.

@receiver(pre_save, sender=Transaction)
def calculate_total_price(sender, instance, **kwargs):
    if not instance.price_total:
        instance.price_total = instance.quantity * instance.price

@receiver(post_save, sender=Transaction)
def update_stock(sender, instance, **kwargs):
    product = Product.objects.get(id=instance.product_id)
    if instance.transaction == 1:
        if not product.stock:
            #! first came as null so we did it like this 👆
            product.stock = instance.quantity
        else:
           product.stock += instance.quantity
    else:
        product.stock -= instance.quantity

    product.save()
```

## 🚩 For the "signal.py" file to work, we need to add the "ready" method to the "apps.py" file 👇

```python
    def ready(self):
        import stock.signals
```

## 🚩 Go to "views.py" and start to write views 👇

```python
from rest_framework import viewsets, filters
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = ''
    filter_fields = [filters.SearchFilter]
    search_fields = ['name']
```

## 🚩 Create "serializers.py" under "stock" App 👇

```python
from rest_framework import serializers
from .models import (
    Category,
    Brand,
    Product,
    Firm,
    Transaction
)

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name"
        )
```

## 🚩 Go back "views.py" and improt that serializer 👇

```python
from .serializers import(
    CategorySerializers,
)
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializers
```

## 🚩 Create "urls.py" file under "stock" App and add 👇

```python
from django import urls
from django.urls import path
from .views import(
    CategoryView
)
from rest_framework import routers

router = routers.DefaultRouter()
router.register('Category', CategoryView)

urlpatterns = [

] + router.urls
```

## 🚩 Go to "views.py" and create BrandView() 👇

```python
class BrandView(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
```

```python
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = (
            "id",
            "name"
        )
```

## 🚩 Go to "stock/urls.py" and add the path 👇

```python
router.register('Brand', BrandView)
```

## 🚩 Go to "views.py" and create ProductView() 👇

```python
from django_filters.rest_framework import DjangoFilterBackend

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'brand']
    search_fields = ['name']
```

## ✔ Add 'django_filters' to the INSTALLED_APP in "settings.py" 👇

## 🚩 Go to "serializers.py" and create ProductSerializer() 👇

```python
class ProductSerializer(serializers.ModelSerializer):
    #! We use "stringRelated" to get the string equivalent of those connected with foreign key 👇

    category = serializers.StringRelatedField()
    category_id = serializers.IntegerField(write_only=True)
    brand = serializers.StringRelatedField()
    brand_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "category",
            "category_id",
            "brand",
            "brand_id",
            "stock"
        )
        #! 👇 "We added it as a read only field because we don't want the stock to be created in the post action.
        read_only_fields = ('stock',)
```

## 🚩 Go to "stock/urls.py" and add the path 👇

```python
router.register('product', ProductView)
```

## 🚩 Go to "views.py" and create FirmView() 👇

```python
class FirmView(viewsets.ModelViewSet):
    queryset = Firm.objects.all()
    serializer_class = FirmSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']
```

## 🚩 Go to "serializers.py" and create FirmSerializer() 👇

```python
class FirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = Firm
        fields = (
            "id",
            "name",
            "phone",
            "address"
        )
```

## 🚩 Go to "stock/urls.py" and add the path 👇

```python
router.register('firm', FirmView)
```

## 🚩 Go to "views.py" and create TransactionView() 👇

```python
class TransactionView(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['firm', 'transaction', 'product']
    search_fields = ['firm']

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
```

## 🚩 Go to "serializers.py" and create TransactionSerializer() 👇

```python
class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    firm = serializers.StringRelatedField()
    firm_id = serializers.IntegerField()
    product = serializers.StringRelatedField()
    product_id = serializers.IntegerField()

    class Meta:
        model = Transaction
        fields = (
            "id",
            "user",
            "firm",
            "firm_id",
            "transaction",
            "product",
            "product_id",
            "quantity",
            "price",
            "price_total",
        )

        read_only_fields = ('price_total',)

    def validate(self, data):
        #! data, actually all of the above fields 👆
        if data.get('transaction') == 0:
            product = Product.objects.get(id=data.get('product_id'))
            if data.get('quantity') > product.stock:
                raise serializers.ValidationError(
                    f'Not enough stock! Current stock is {product.stock}'
                )
        return data
```

## 🚩 Go to "stock/urls.py" and add the path 👇

```python
router.register('transaction', TransactionView)
```

## 🚩 #! While on the Category page, we want to query the products of that category. For this, we need to write a serializer (CategoryProductsSerializer()) in a nested structure. 👇

```python
class CategoryProductsSerializer(serializers.ModelSerializer):
    #! We used "many=True" because there can be more than one product belonging to the category. 👇
    products = ProductSerializer(many=True)

    class Meta:
        model = Category
        fields = (
            "name",
            "products"
        )
```

## 🚩 Then customize the CategoryView() 👇

```python
class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_fields = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name']
    filterset_fields = ["name"]

    def get_serializer_class(self):
        if self.request.query_params.get('name'):
        #! 👆 According to which field it will search. It comes to the url as "?name=". "query_params ?name..&id=" We can write the query_params here as nested.
            return CategoryProductsSerializer
        else:
            return super().get_serializer_class
```

#  <center> 🛑 ADDING PERMISSIONS 🛑 </center>

## 🚩 Go to "stock/views.py ", import DjangoModelPermissions and customize all views by adding 👇

```python
from rest_framework.permissions import DjangoModelPermissions
#! Get methods can be overridden to limit public requests. 👆

    permission_classes = [DjangoModelPermissions]
```

## 🚩 Go to "settings.py" and add 👇

```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ]
}
```

## 🚩 To show groups of users in admin panel; go to "account/admin.py" and add 👇

```python
from django.contrib.auth.admin import UserAdmin
from django.contrib import admin
from django.contrib.auth.models import User

class UserAdminWithGroup(UserAdmin):
    def group_name(self, obj):
        queryset = obj.groups.values_list('name', flat=True)
        groups = []
        for group in queryset:
            groups.append(group)

        return ' '.join(groups)

    list_display = UserAdmin.list_display + ('group_name',)


admin.site.unregister(User)
admin.site.register(User, UserAdminWithGroup)
```

## 🚩 Create "permissions.py" file under "stock" App 👇

```python
from rest_framework.permissions import DjangoModelPermissions

class CustomModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': ['%(app_label)s.view_%(model_name)s'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }
```

## 🚩 Since we wrote Custom Permissions, we need to update the permissions in the views. So import the CustomPermissionModel() in "views.py" 👇

```python
from .permissions import CustomModelPermission

    permission_classes = [CustomModelPermission]
```

## 📢 Do not forget to check the endpoints you wrote in [Postman](https://www.postman.com/).

## <center>🥳 END OF THE  PROJECT 🥳</center>