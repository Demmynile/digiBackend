from tkinter.ttk import Style
from rest_framework import serializers
from django.db import transaction
from users.models import Category, Items,Product, Order, OrderItem, ShippingAddress, Review, SubCategory, SuperCategory,Vendor,Buyer,User,PermanentAddress , PaymentOrder
from rest_framework.validators import UniqueValidator
import uuid



class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class POrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentOrder
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    reviews = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer( reviews ,many=True)
        return serializer.data

class ProductListSerializer(serializers.ListSerializer):
      class Meta:
        model = Product
        fields = '__all__'

class ItemzSerializer(serializers.ModelSerializer):
      class Meta:
        model = OrderItem
        fields = [ 'userid','name',]


class VendorSerializer(serializers.ModelSerializer):
      class Meta:
        model = Vendor
        fields = '__all__'

class ProdSerializer(serializers.Serializer):
    class Meta:
        list_serializer_class = ProductListSerializer
    reviews = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
    
    def get_reviews(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer( reviews ,many=True)
        return serializer.data

class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = '__all__'
class PermanentAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = PermanentAddress
        # user = serializers.CharField(max_length=50, validators=[UniqueValidator(queryset=PermanentAddress.objects.all())])
        fields = '__all__'

class OrdersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'

class UserSerialize(serializers.ModelSerializer):
    
    # profile= ProfileSerializer(required=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model = User

        fields = [ 'username','password','password2']
  
class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField(read_only=True)
    order = serializers.SerializerMethodField(read_only=True)
    shipping = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = OrderItem
        fields = '__all__'

    def get_product(self, obj):
        products = obj.product
        serializer = ProductSerializer(products, many=False)
        return serializer.data
    def get_order(self, obj):
        products = obj.order
        serializer = OrdersSerializer(products, many=False)
        return serializer.data

    def get_shipping(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shipping, many=False).data
        except:
            address = False
        return address
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data

class UserSerializer(serializers.ModelSerializer):
    
    # profile= ProfileSerializer(required=True)
    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model = User

        fields = [ 'id','username', 'email','shopName','Vendid','Country','digiNumber','password','password2','phone','State','gender','City','Vendlogo' ,'first_name','last_name', 'is_buyer','is_staff','is_vendor','VendorNumber','BusinessType','is_verified','Vendaddress']

class OrderSerialized(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = [ 'agentid']
class OrderSerial(serializers.ModelSerializer):
	
    class Meta:
        model = Order
        fields = '__all__'
class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(read_only=True)
    product = serializers.SerializerMethodField(read_only=True)
    shipping = serializers.SerializerMethodField(read_only=True)
    # permanent = serializers.SerializerMethodField(read_only=True)
    user = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

    def get_orderItems(self, obj):
        items = obj.orderitem_set.all()
        serializer = OrderItemSerializer(items, many=True)
        return serializer.data

    def get_shipping(self, obj):
        try:
            address = ShippingAddressSerializer(
                obj.shipping, many=False).data
        except:
            address = False
    def get_product(self, obj):
        products = obj.products
        serializer = ProductSerializer(products, many=False)
        return serializer.data

    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
    def get_user(self, obj):
        user = obj.user
        serializer = UserSerializer(user, many=False)
        return serializer.data
    # def get_permanent(self, obj):
    #     permanent = obj.permanent
    #     serializer = PermanentAddressSerializer(permanent, many=False)
    #     return serializer.data


  

class VendorSignupSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password','is_signed', 'password2','BusinessType','VendorType', 'first_name', 'last_name', 'shopName', 'Vendaddress', 'phone']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email'],
            BusinessType=self.validated_data['BusinessType'],
            VendorType=self.validated_data['VendorType'],
            first_name=self.validated_data['first_name'],
            last_name=self.validated_data['last_name'],
            shopName=self.validated_data['shopName'],
            Vendaddress=self.validated_data['Vendaddress'],
            phone=self.validated_data['phone'],
            # altPhone=self.validated_data['altPhone'],          
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_vendor=True
        x = uuid.uuid4().hex.upper()
        genid=x[10:20]
        user.VendorNumber="DIGI" + genid
        user.save()
        Vendor.objects.create(user=user)
        return user
class AdminSignupSerializer(serializers.ModelSerializer):

    password2=serializers.CharField(style={"input_type":"password"}, write_only=True)
    class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
    def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_staff=True
        user.is_superuser=True
        user.save()
        # Vendor.objects.create(user=user)
        return user




    # def get__id(self, obj):
    #     return obj.id

class BuyerSignupSerializer(serializers.ModelSerializer):
  password2=serializers.CharField(style={"input_type":"password"}, write_only=True)

  class Meta:
        model=User
        fields=['username','email','password', 'password2']
        extra_kwargs={
            'password':{'write_only':True}
        }
    
  def save(self, **kwargs):
        user=User(
            username=self.validated_data['username'],
            email=self.validated_data['email']
        )
        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password !=password2:
            raise serializers.ValidationError({"error":"password do not match"})
        user.set_password(password)
        user.is_buyer=True
        user.save()
        Buyer.objects.create(user=user)
        return user

    # def get__id(self, obj):
    #     return obj.id

class SuperCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SuperCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'
    # lookup_field = 'id_superparent'

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = '__all__'
    # lookup_field = 'id_parent'


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Items
        fields = '__all__'
    # lookup_field = 'id_child'

