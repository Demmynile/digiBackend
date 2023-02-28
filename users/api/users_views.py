from multiprocessing import context
from webbrowser import get
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view, permission_classes
from django.http import request
from rest_framework.parsers import JSONParser
from django.db.models  import F
from rest_framework import status,generics,viewsets,permissions
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from rest_framework.views import APIView
from users.models import User, Vendor
from django.db.models import Sum
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from .permissions import IsVendorUser, IsBuyerUser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, UserSerialize, VendorSerializer, VendorSignupSerializer,BuyerSignupSerializer,ProductSerializer,AdminSignupSerializer

class VendorSignupView(generics.GenericAPIView):
    serializer_class=VendorSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })

class AdminSignupView(generics.GenericAPIView):
    serializer_class=AdminSignupSerializer
    def post(self, request, *args, **kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "message":"account created successfully"
        })
class BuyerSignupView(generics.GenericAPIView):
    serializer_class=BuyerSignupSerializer
    def post(self,request,*args,**kwargs):
        serializer=self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user=serializer.save()
        return Response({    
            "user":UserSerializer(user, context=self.get_serializer_context()).data,
            "token":Token.objects.get(user=user).key,
            "Message":"Account Sucessfully created" })

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer=self.serializer_class(data=request.data, context={'request':request})
        serializer.is_valid(raise_exception=True)
        user=serializer.validated_data['user']
        # product=serializer.validated_data['product']
        token, created=Token.objects.get_or_create(user=user)
        return Response({
            'token':token.key,
            'user_id':user.pk,
            'is_buyer':user.is_buyer,
            'username': user.username,
            'BusinessType': user.BusinessType,
            'VendorType': user.VendorType,
            'is_verified': user.is_verified,
            'notify': user.notify,
            # 'product':product.user.username,
        })
class LogoutView(APIView):
    def post(self, request, format=None):
        request.auth.delete()
        return Response(status=status.HTTP_200_OK)


class BuyerOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsBuyerUser]
    
    

    def get_object(self):
        return self.request.user

class AdminbOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAdminUser]
    
    

    def get_object(self):
        return self.request.user

class VendorOnlyView(generics.RetrieveAPIView):
    permission_classes=[permissions.IsAuthenticated&IsVendorUser]
    serializer_class=UserSerializer

    def get_object(self):
        return self.request.user

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)

@api_view(['GET'])
def getShopViews(request, pk):
    user = User.objects.get(id=pk)
    user.notify+=1
    user.save()
    serializer = UserSerializer(user, many=False)
    return Response({"status": "success","data":serializer.data,'viewed': user.notify}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getVendorUserById(request, pk):
    user = User.objects.get(id=pk)
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)
# @api_view(['GET'])
# # @permission_classes([IsAuthenticated&IsVendorUser])
# def getVendorProfile(request):
#     user = request.user
#     vendor = user.vendor_set.all()
#     serializer = ProductSerializer(vendor, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getVendorProfile(request,pk):
 
    vendor = Vendor.objects.filter(user_id=pk)
    serializer = VendorSerializer(vendor, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
# @permission_classes([IsAdminUser])
def updateUser(request, pk):
    user = User.objects.get(id=pk)
    # user = User.objects.get(id=pk).update(City=F('City') +1)
   

    data = request.data

    # user.first_name = data['name']
    # user.username = data['username']
    user.email = data['email']

    user.notify += 1

    
    # user.is_staff = data['isAdmin']
    user.is_verified = data['is_verified']
    # if data['password'] != '':
    #     user.password = make_password(data['password'])
    # send_mail(
    #     'Vendor verifed',
    #     ' Congratulations You can now login as a vendor at.'+ 'http://157.230.87.8:8020/vendor/signin',
    #     'aakindele@sterlingtech.com.ng',
    #     [user.email],
    #     fail_silently=False,
    #    )


    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)




@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateVendorLogin(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    
    
    user.username = data['username']
    user.email = data['email']
    user.gender = data['gender']
    user.phone = data['phone']
    user.shopName = data["shopName"]
    user.first_name = data["first_name"]
    user.last_name = data["last_name"]
    user.Vendaddress = data['Vendaddress']
    user.Country = data['Country']
    user.State = data['State']
    user.City = data['City']
    if data['password'] != '':
        user.password = make_password(data['password'])



    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)



@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateVendid(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    
    
 
    user.Vendid = data['Vendid']
    # user.Vendlogo = data['Vendlogo']
    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsAdminUser])
def updateVendorsLoginDetails(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    
    
    user.username = data['username']
    if data['password'] != '':
        user.password = make_password(data['password'])



    user.save()

    serializer = UserSerialize(user, many=False)

    return Response(serializer.data)


@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateVendlogo(request, pk):
    user = User.objects.get(id=pk)

    data = request.data
    
    
 
    user.Vendlogo = data['Vendlogo']
    user.save()

    serializer = UserSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
@permission_classes([IsAuthenticated&IsVendorUser])
def updateVendorProfile(request, pk):
    user = Vendor.objects.get(user_id=pk)

    data = request.data

    user.email = data['email']
    user.gender = data['gender']
    user.phone = data['phone']
    user.companyName = data['companyName']
    user.firstNname = data['firstNname']
    user.lastNname = data['lastNname']
    # user.Vendpic = request.FILES.get('Vendpic')
    # user.Vendlogo = request.FILES.get('Vendlogo')

    # user.is_staff = data['isAdmin']
    # user.is_verified = data['is_verified']
    # if data['password'] != '':
    #     user.password = make_password(data['password'])


    user.save()

    serializer = VendorSerializer(user, many=False)

    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated&IsVendorUser])
def uploadImage(request):
    data = request.data

    user_id = data['user_id']
    vendor = Vendor.objects.get(user_id=user_id)

    vendor.Vendpic = request.FILES.get('Vendpic')
    vendor.Vendlogo = request.FILES.get('Vendlogo')
    vendor.save()

    return Response('Image was uploaded')
# Users View
@csrf_exempt
@api_view(['POST','GET'])                                                           # Decorator to make the view csrf excempt.
def user_list(request, pk=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        if pk:                                                                      # If PrimaryKey (id) of the user is specified in the url
            users = User.objects.filter(id=pk)              # Select only that particular user
        else:
            users = User.objects.all()                             # Else get all user list
        serializer = UserSerializer(users, many=True, context={'request': request}) 
        return Response(serializer.data)               # Return serialized data
    elif request.method == 'POST':
        data = JSONParser().parse(request)           # On POST, parse the request object to obtain the data in json
        serializer = UserSerializer(data=data)        # Seraialize the data
        if serializer.is_valid():
            serializer.save()                                            # Save it if valid
            return Response(serializer.data, status=201)     # Return back the data on success
        return Response(serializer.errors, status=400)     # Return back the errors  if not valid

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getApprovedUsers(request,pk):
 
    user = User.objects.filter(is_verified=pk)
    serializer = UserSerializer(user, many=True)
    return Response({"status": "success","data":serializer.data,"count":len(user)}, status=status.HTTP_200_OK)
    # return Response({"status": "success","data":serializer.data,'viewed': user.notify}, status=status.HTTP_200_OK)
@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getVendoInfo(request):
    user = User.objects.filter(is_vendor=1)
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)
@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getBuyerInfo(request):
    user = User.objects.filter(is_buyer=1)
    serializer = UserSerializer(user, many=True)
    return Response(serializer.data)


@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllVisits(request):
    useritems = User.objects.all()
    totals =  User.objects.all().aggregate(TOTAL =Sum('notify'))['TOTAL']
    serializer =UserSerializer(useritems, many=True)
    return Response({"status": "success","data":serializer.data,"visits": totals}, status=status.HTTP_200_OK)