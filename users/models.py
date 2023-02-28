from email.headerregistry import Address
from django.conf import settings
from django.contrib.auth.models import User
from django.db import IntegrityError
import http.client
# from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin,AbstractUser)
from rest_framework.authtoken.models import Token
from django_extensions.db.fields import ShortUUIDField
import shortuuid

# from api.documents.models import Document, OtherDocument
# from api.industry.models import Industry
# from api.user.models import Supplier
# from api.user.models import ProcurementManager
from django.core.mail import send_mail
from django.db.models.signals import post_save
from re import S
# from users.models import Vendor,Buyer
from django.dispatch import receiver
from django.db import models


class User(AbstractUser):
    is_buyer = models.BooleanField(default=False, null=True, blank=True)
    is_vendor = models.BooleanField(default=False, null=True, blank=True)
    # vendoruser = models.OneToOneField(Vendor,related_name="VendorsProfiles" ,on_delete=models.CASCADE)
    # buyeruser = models.OneToOneField(Buyer,related_name="BuyersProfiles" ,on_delete=models.CASCADE)
    email = models.EmailField(
        max_length=254, unique=True, null=True, blank=True)
    # username = None
    Businesschoice = (
        ('0', 'Artisans'),
        ('1', 'Professionals'),
        ('2', 'General Trading'),
        ('3', 'Service Provider'),
        ('4', 'Home Markers')
    )
    Vendorchoice = (
        ('0', 'Merchant'),
        ('1', 'Service Provider') 
    )
    uuid = models.CharField(max_length=500, blank=True , null = True)
    digiNumber = models.CharField(max_length=100, null=True, blank=True)
    BusinessType = models.CharField(max_length=100, choices=Businesschoice, null=True, default=1, blank=True)
    VendorType = models.CharField(max_length=100, choices=Vendorchoice, null=True, default=1, blank=True)
    Vendaddress = models.CharField(max_length=500, null=True, blank=True)
    shopName = models.CharField(max_length=500, null=True, blank=True)
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    Country = models.CharField(max_length=225, null=True, blank=True)
    State = models.CharField(max_length=225, null=True, blank=True)
    City = models.CharField(max_length=225, null=True, blank=True)
    notify = models.IntegerField(null=True, blank=True, default=0)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    last_login = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    is_signed = models.BooleanField(default=False)
    Vendid = models.ImageField(null=True, blank=True, default='placeholder.png' )
    Vendlogo = models.ImageField(null=True, blank=True , default='placeholder.png')
    imagess = models.ImageField(null=True, blank=True , default='placeholder.png')
    imgs = models.ImageField(null=True, blank=True , default='placeholder.png')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    VendorNumber= models.CharField(max_length=20, null=True, blank=True)

    def _str_(self):
        return f"{self.username}"
    def save(self,*args,**kwargs):
    #    send_mail(
    #     'Vendor Registration',
    #     'Vendor Registration Successfull.',
    #     'aakindele@sterlingtech.com.ng',
    #     [self.email],
    #     fail_silently=False,
    #    )
       
       return super(User,self).save(*args,**kwargs)
class Vendor(models.Model):
    email = models.EmailField(
        max_length=254, unique=True, null=True, blank=True)
    user = models.OneToOneField(User,related_name="vendorsprofile", on_delete=models.CASCADE, null=True)
    digiNumber = models.CharField(max_length=100, null=True, blank=True)
    Vendpic = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    Vendlogo = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    firstNname = models.CharField(max_length=100, null=True, blank=True)
    lastNname = models.CharField(max_length=100, null=True, blank=True)
    companyName = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    last_login = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
 

    def _str_(self):
        return f"{self.user.username}"
        
class Buyer(models.Model):
    user = models.OneToOneField(User,related_name="buyersProfile", on_delete=models.CASCADE, null=True)
    email = models.EmailField(
        max_length=254, unique=True, null=True, blank=True)
    digiNumber = models.CharField(max_length=100, null=True, blank=True)
    Buyername = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    last_login = models.DateTimeField(null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def _str_(self):
        return f"{self.user.username}"



    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_auth_token(sender, instance=None, created=False, **kwargs):
     if created:
        Token.objects.create(user=instance)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #   instance.profile.save()




class Product(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    # vendors = models.ForeignKey(Vendor, related_name='products', on_delete=models.CASCADE , default=3)
    # vendors = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    image = models.ImageField(null=True, blank=True,
                               default='/placeholder.png')
    image1 = models.ImageField(null=True, blank=True, default='/placeholder.png')

    image2 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image3 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image4 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image5 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image6 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image7 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image8 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image9 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image10 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image11 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image12 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image13 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image14 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image15 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image16 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image17 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image18 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    image19 = models.ImageField(null=True, blank=True,
                               default='placeholder.png')
    thumbnail = models.ImageField(null=True, blank=True, default='/images/placeholder.png')
    notify = models.IntegerField(null=True, blank=True, default=0)

    viewed = models.IntegerField(null=True, blank=True, default=0)


    createdAt = models.DateTimeField(auto_now_add=True)

    isabled= models.BooleanField(default=False, null=True, blank=True)
    brand = models.CharField(max_length=200, null=True, blank=True)
    category = models.CharField(max_length=200, null=True, blank=True)
    subcategory = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    descriptions = models.TextField(null=True, blank=True)
    rating = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    numReviews = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    discount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    countInStock = models.IntegerField(null=True, blank=True, default=0)
    # createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)
    country = models.CharField(max_length=100, null=True, blank = True)

    supcategory = models.CharField(max_length=100, null=True, blank = True)


    supercategory = models.CharField(max_length=100, null=True, blank = True)


    state = models.CharField(max_length=100, null=True, blank = True)
    city = models.CharField(max_length=100, null=True, blank = True)
    complaintField = models.CharField(max_length=100, null=True, blank = True)
    streetAddress = models.CharField(max_length=200, null=True, blank = True)

    def get_createdAt(self, obj):
        return obj.createdAt.strftime("%Y-%m-%d %H:%M:%S")

    def __str__(self):
        return self.name

    class Meta:
      ordering = ['-createdAt']



# class Vendor(models.Model):

#     STATUS = (
#         ('0', 'Rejected'),
#         ('1', 'Approved'),
#         ('2', 'Pending')
#     )
#     vendorManager = models.OneToOneField(User, on_delete=models.CASCADE,
#                                               related_name='vendor_profile', null = True, blank= True)
#     companyName = models.CharField(max_length=100, default='Anonymous', null = True, blank= True)
#     email = models.EmailField(max_length = 200, null=True, blank = True)
#     RegistrationNo = models.CharField(max_length=100, null=True, blank = True)
#     updated_at = models.DateTimeField(auto_now=True, null = True, blank= True)
#     RegistrationDate = models.DateField(auto_now_add = True, null = True, blank= True)
#     firstName = models.CharField(max_length = 100 , null = True, blank = True)
#     LastName = models.CharField(max_length = 100  , null = True, blank = True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     companyPhone = models.CharField(max_length=100, null=True, blank = True)
#     companyEmail = models.EmailField(max_length = 200,null=True, blank = True)
#     siteVisitCheckStatus = models.CharField(max_length=100, choices=STATUS, null=True, default=1, blank=True)
   

# class Buyer(models.Model):
#     buyerManager = models.OneToOneField(User, on_delete=models.CASCADE,
#                                               related_name='buyer_profile', null = True, blank= True)
    
#     email = models.EmailField(max_length = 200, null=True, blank = True)
#     firstName = models.CharField(max_length = 100 , null = True, blank = True)
#     LastName = models.CharField(max_length = 100  , null = True, blank = True)
#     contactDept = models.CharField(max_length=100, null=True, blank = True)
#     contactPhone = models.CharField(max_length=100, null=True, blank = True)
#     companyPhone = models.CharField(max_length=100, null=True, blank = True)
#     companyEmail = models.EmailField(max_length = 200,null=True, blank = True)
#     country = models.CharField(max_length=100, null=True, blank = True)
#     createdAt = models.DateTimeField(auto_now_add=True)
#     state = models.CharField(max_length=100, null=True, blank = True)
#     city = models.CharField(max_length=100, null=True, blank = True)
#     companyWeb = models.CharField(max_length=100, null=True, blank = True)
#     streetAddress = models.CharField(max_length=200, null=True, blank = True)
#     postalZip = models.CharField(max_length=300, null=True, blank = True)
#     contactJobTitle = models.CharField(max_length=100, null=True, blank = True)
#     companyName = models.CharField(max_length=100, null=True, blank = True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    # buyers = models.ForeignKey(Buyer, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    rating = models.IntegerField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.rating)
class ShippingAddress(models.Model):
    # order = models.OneToOneField(
    #     Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.address)
class PermanentAddress(models.Model):
	    # order = models.OneToOneField(
    #     Order, on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    postalCode = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=200, null=True, blank=True, unique=True)
    
          
    def save(self, *args, **kwargs):
                try:
                    self.user=self.user
                    super(PermanentAddress , self).save(*args, **kwargs)
                except IntegrityError as e :
                    e ="this data already exists in database"
                  

    def __str__(self):
        return str(self.address)
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    vendors = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)
    shipping = models.OneToOneField(ShippingAddress, on_delete=models.SET_NULL, null=True)
    products = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    paymentMethod = models.CharField(max_length=200, null=True, blank=True)
    taxPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    shippingPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    totalPrice = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    isPaid = models.BooleanField(default=True)
    isDelivered = models.BooleanField(default=False)
    paidAt = models.DateTimeField(auto_now_add=True , null=True , blank=True)
    isDelivered = models.BooleanField(default=False)
    vendors = models.ManyToManyField(Vendor, related_name='orders')
    agentid = models.CharField(max_length=200, null=True, blank=True)
    isAgentPaid = models.BooleanField(default=False)
    deliveredAt = models.DateTimeField(
        auto_now_add=False, null=True, blank=True)
    createdAt = models.DateTimeField(auto_now_add=True)
    _id = models.AutoField(primary_key=True, editable=False)

    def __str__(self):
        return str(self.createdAt)

class PaymentOrder(models.Model):
    userids= models.CharField(max_length=200, null=True, blank=True)
    status= models.CharField(max_length=200, null=True, blank=True)
    vendorname= models.CharField(max_length=200, null=True, blank=True)
    creditnoteno = models.CharField(max_length=200, null=True, blank=True)
    NetAmount = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    paidat = models.DateField(
        auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    shipping = models.ForeignKey(ShippingAddress, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    chek= models.CharField(max_length=200, null=True, blank=True)
    recitno=models.CharField(max_length=200, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    userid = models.CharField(max_length=200, null=True, blank=True)
    qty = models.IntegerField(null=True, blank=True, default=0)
    price = models.DecimalField(
        max_digits=7, decimal_places=2, null=True, blank=True)
    image = models.CharField(max_length=200, null=True, blank=True)
    _id = models.AutoField(primary_key=True, editable=False)
    soldat = models.DateField(
        auto_now_add=False, null=True, blank=True)

    def __str__(self):
        return str(self.name)

class SuperCategory(models.Model):
    name = models.CharField(max_length=254, unique=True)
    id = models.CharField(primary_key=True ,max_length=254,editable=False)

   
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name
class Category(models.Model):
    name = models.CharField(max_length=254, unique=True)
    id_superparent= models.ForeignKey(SuperCategory, on_delete=models.SET_NULL, null=True)
    id = models.CharField(primary_key=True ,max_length=254,editable=False)

    
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class SubCategory(models.Model):
    name = models.CharField(max_length=254, unique=True)
    id_parent = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    status = models.BooleanField(default=True)
    id = models.CharField(primary_key=True ,max_length=254,editable=False)
    
    def __str__(self):
        return self.name

class Items(models.Model):
    name = models.CharField(max_length=254, unique=True)
    id_child= models.ForeignKey(SubCategory, on_delete=models.SET_NULL, null=True)
    id = models.CharField(primary_key=True ,max_length=254,editable=False)


    
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class ProductNotification():
    product= models.ForeignKey(Product, on_delete=models.CASCADE)
    msg = models.CharField(max_length=254)
    is_seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)

class UserNotification():
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    msg = models.CharField(max_length=254)
    is_seen = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)