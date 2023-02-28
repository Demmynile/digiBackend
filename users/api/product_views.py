from unittest import result
from django.http import HttpResponse
from django.shortcuts import render
from django.core import serializers
from numpy import integer, product
from django.db.models  import F
from requests import Response

from rest_framework.decorators import api_view, permission_classes
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from yaml import serialize
from .permissions import IsVendorUser, IsBuyerUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from users.models import Category, Items, Product,Review, SubCategory, SuperCategory,Vendor
from .serializers import ItemSerializer, ProductSerializer, SubCategorySerializer, SuperCategorySerializer,UserSerializer,CategorySerializer,SubCategorySerializer,SuperCategorySerializer,ItemSerializer

from rest_framework import status,generics,viewsets,permissions

@api_view(['POST'])
@permission_classes([IsAuthenticated&IsVendorUser])
def createProduct( request):
  
    user=request.user
    # venues = Task.objects.get(pk=db_id)
    # pk = self.kwargs.get('pk')
    # Product.vendors = Vendor.objects.get(id)
    # print(Product.vendors)
    
    # print(vendors)
    
    # print(vendors)
    
    data = request.data
   
    # vendors = request.data.vendorsy7u.id
    product = Product.objects.create(
        user=user,
        # vendors=Product.vendors,
        name=data['name'],
        # notify +=1
        # isabled=data['isabled'],
        price = data['price'],
        brand = data['brand'],
        countInStock = data['countInStock'],
        supcategory = data["supcategory"],
        category = data['category'],
        subcategory = data["subcategory"],
        description = data['description'],
        image = data["image"],
        location = data["location"],
        
    )

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated&IsVendorUser])
def uploadImage(request):
    data = request.data

    product_id = data['product_id']
    product = Product.objects.get(_id=product_id)

    product.image = request.FILES.get('image')
    product.save()

    return Response('Image was uploaded')
class VendorOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsVendorUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getProductById(request, pk):

    user = request.user

    try:
        product = Product.objects.get(_id=pk)
        if user.is_vendor or product.user == user:
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this Product'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAdminProductById(request, pk):

    user = request.user

    try:
        product = Product.objects.get(_id=pk)
        if user.is_staff or product.user == user:
            serializer = ProductSerializer(product, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this Product'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Product does not exist'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getMyProducts(request):
    user = request.user
    products = user.product_set.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getMyProductsCounts(request):
    user = request.user
    products = user.product_set.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success","data":serializer.data,"count":len(products)}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getMyTotalSales(request):
    user = request.user
    products = user.product_set.all()
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success","data":serializer.data,"vendorearnings": (sum(product.totalPrice))}, status=status.HTTP_200_OK)





@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getShopProducts(request,pk):
 
    products = Product.objects.filter(user_id=pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def getBuyerProduct(request, pk):
    product = Product.objects.get(_id=pk)
    product.viewed+=1
    product.save()
    serializer = ProductSerializer(product, many=False)
    return Response({"status": "success","data":serializer.data,'viewed': product.viewed}, status=status.HTTP_200_OK)

    

@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getallProducts(request):
   
    products=Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

@api_view(['GET','PUT'])
@permission_classes([IsAdminUser])
def getProducts(request):
   
    products=Product.objects.all()
    serializer = ProductSerializer(products,many=True)
    return Response(serializer.data)

# to update and upload image    

@api_view(['PUT'])
@permission_classes([IsAdminUser])
def updateProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)


    # product.name = data['name']
    # product.price = data['price']
    # product.brand = data['brand']
    # product.countInStock = data['countInStock']
    # product.category = data['category']
    # product.description = data['description']


    product.complaintField = data['complaintField']
    product.notify +=1
    product.isabled = data['isabled']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateVendorProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)


    # product.name = data['name']
    # product.price = data['price']
    # product.brand = data['brand']
    # product.image = data['image']
    # product.countInStock = data['countInStock']
    # product.category = data['category']
    # product.description = data['description']
    product.notify=0
    product.complaintField = data['complaintField']



    # product.isabled = data['isabled']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateImageProduct(request, pk):
    data = request.data
    product = Product.objects.get(_id=pk)


    product.name = data['name']
    product.price = data['price']
    product.brand = data['brand']
    product.notify=0
    # product.image = request.FILES.get('image')
    # product.image = data['image']
    product.discount = data['discount']
    product.countInStock = data['countInStock']
    product.category = data['category']
    product.description = data['description']
    product.complaintField = data['complaintField']



    # product.isabled = data['isabled']

    product.save()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getApprovedProducts(request,pk):
    products = Product.objects.filter(isabled=pk)
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)
    # return Response({"status": "success","data":serializer.data,'viewed': user.notify}, status=status.HTTP_200_OK)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAdminApprovedProducts(request,pk):
 
    products = Product.objects.filter(isabled=pk)
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success","data":serializer.data,"count":len(products)}, status=status.HTTP_200_OK)
    # return Response({"status": "success","data":serializer.data,'viewed': user.notify}, status=status.HTTP_200_OK)
@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getAdminApprovedProductsCount(request):
 
    products = Product.objects.filter(isabled=1)
    serializer = ProductSerializer(products, many=True)
    return Response({"status": "success","data":serializer.data,"count":len(products)}, status=status.HTTP_200_OK)
    # return Response({"status": "success","data":serializer.data,'viewed': user.notify}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def GetOrderdProduct(request, pk):
    # data = request.data
    product = Product.objects.get(_id=pk).order_set.all()

    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAdminUser])
def getAdminProductByIds(request, pk):
    product = Product.objects.get(_id=pk)
    serializer = ProductSerializer(product, many=False)
    return Response(serializer.data)

class SuperCategoryViewSet(viewsets.ModelViewSet):
    queryset=SuperCategory.objects.all()
    serializer_class = SuperCategorySerializer

@api_view(['GET'])
def getCategory(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Category.objects.filter(id_superparent_id=pk)
        serializer = CategorySerializer(value, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getProductCategory(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Product.objects.filter(category=pk)
        serializer = ProductSerializer(value, many=True)
        return Response(serializer.data)
        
@api_view(['GET'])
def getSupProductCategory(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Product.objects.filter(supercategory=pk)
        serializer = ProductSerializer(value, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getProductSubCategory(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Product.objects.filter(subcategory=pk)
        serializer = ProductSerializer(value, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def getProductLocation(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Product.objects.filter(location=pk)
        serializer = ProductSerializer(value, many=True)
        return Response(serializer.data)
# class SubCategoryViewSet(viewsets.ModelViewSet):
#     queryset=SubCategory.objects.all()
    
#     serializer_class = SubCategorySerializer
# @action(detail=False, methods=['GET','POST'])
# def getSubcategory(self,request):
#     id_parent = self.request.query_params.get('id_parent',None)
#     value=SubCategory.objects.filter(id_parent_id=id_parent)
#     result=serializers.serialize('json',value)
#     return HttpResponse(result,content_type='application/json')

@api_view(['GET'])
def getSubcategory(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=SubCategory.objects.filter(id_parent_id=pk)
        serializer = SubCategorySerializer(value, many=True)
        return Response(serializer.data)
# class ItemViewSet(viewsets.ModelViewSet):
#     queryset=Items.objects.all()
#     serializer_class = ItemSerializer
@api_view(['GET'])
def getItems(request,pk):
        # id_child = request.query_params.get('pk',None)
        value=Items.objects.filter(id_child_id=pk)
        serializer = ItemSerializer(value, many=True)
        return Response(serializer.data)
# @api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
# def getVendorProfile(request,pk):
 
#     vendor = Vendor.objects.filter(user_id=pk)
#     serializer = VendorSerializer(vendor, many=True)
#     return Response(serializer.data)




   