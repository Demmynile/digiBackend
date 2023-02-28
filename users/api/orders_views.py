from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from .permissions import IsVendorUser, IsBuyerUser

from users.models import Product, Order, OrderItem, ShippingAddress,PermanentAddress ,PaymentOrder
from django.db.models import Sum
from .serializers import ProductSerializer, OrderSerializer,OrderItemSerializer,OrderSerial,PermanentAddressSerializer,POrderSerializer,ItemzSerializer

from rest_framework import status
import datetime
import uuid




@api_view(['POST'])
@permission_classes([IsAuthenticated&IsBuyerUser])
def addOrderItemsDeliver(request):
    user = request.user
    data = request.data
    x=uuid.uuid4().hex.upper()
    genid=x[15:20]
    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:


        shipping = ShippingAddress.objects.create(
            # order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )


        # (1) Create order

        order = Order.objects.create(
            agentid = genid,
            shipping = shipping,
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
   # (2) Create shipping address

        


        # (3) Create order items adn set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                product=product,
                user=user,
                soldat=datetime.date.today(),
                order=order,
                name=product.name,
                userid=product.user.id,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )

            # (4) Update stock

            product.countInStock -= item.qty
            permanent = PermanentAddress(
            user=user.id,
            address=data['PermanentAddress']['address'],
            city=data['PermanentAddress']['city'],
            postalCode=data['PermanentAddress']['postalCode'],
            country=data['PermanentAddress']['country'],
            )
            permanent.save()
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)
@api_view(['POST'])
@permission_classes([IsAuthenticated&IsBuyerUser])
def addOrderItems(request):
    user = request.user
    data = request.data

    orderItems = data['orderItems']

    if orderItems and len(orderItems) == 0:
        return Response({'detail': 'No Order Items'}, status=status.HTTP_400_BAD_REQUEST)
    else:


        shipping = ShippingAddress.objects.create(
            # order=order,
            address=data['shippingAddress']['address'],
            city=data['shippingAddress']['city'],
            postalCode=data['shippingAddress']['postalCode'],
            country=data['shippingAddress']['country'],
        )

       



        # (1) Create order

        order = Order.objects.create(
            # agentid = "xxxxx",
            shipping = shipping,
            user=user,
            paymentMethod=data['paymentMethod'],
            taxPrice=data['taxPrice'],
            shippingPrice=data['shippingPrice'],
            totalPrice=data['totalPrice']
        )
   # (2) Create shipping address

        


        # (3) Create order items adn set order to orderItem relationship
        for i in orderItems:
            product = Product.objects.get(_id=i['_id'])

            item = OrderItem.objects.create(
                product=product,  
                shipping = shipping,
                user=user,
                soldat=datetime.date.today(),
                order=order,
                name=product.name,
                userid=product.user.id,
                qty=i['qty'],
                price=i['price'],
                image=product.image.url,
            )
            
            # (4) Update stock

            product.countInStock -= item.qty

            permanent = PermanentAddress(
            user=user.id,
            address=data['PermanentAddress']['address'],
            city=data['PermanentAddress']['city'],
            postalCode=data['PermanentAddress']['postalCode'],
            country=data['PermanentAddress']['country'],
            )
            permanent.save()
            product.save()

        serializer = OrderSerializer(order, many=False)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated&IsBuyerUser])
def getOrderById(request, pk):

    user = request.user

    try:
        order = Order.objects.get(_id=pk)
        if user.is_staff or order.user == user:
            serializer = OrderSerializer(order, many=False)
            return Response(serializer.data)
        else:
            Response({'detail': 'Not authorized to view this order'},
                     status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response({'detail': 'Order does not exist'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllVendorItemsdetails(request,pk):
    orderitems = OrderItem.objects.filter(_id=pk)
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllItemsdetails(request):
    orderitems = OrderItem.objects.all()
    serializer = ItemzSerializer(orderitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllPaymentOrders(request):
    PItems = PaymentOrder.objects.all()
    serializer = POrderSerializer(PItems, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated&IsBuyerUser])
def getMyOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getShopOrders(request,pk):
    orders = Order.objects.filter(products_id=pk)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllVendorItems(request,pk):
    orderitems = OrderItem.objects.filter(userid=pk)
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response(serializer.data)

@api_view(['GET','PUT']) 
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAmountOfSoldItems(request,pk):
    orderitems = OrderItem.objects.filter(userid=pk,chek =1)
    totals = OrderItem.objects.filter(userid=pk,chek=1).aggregate(TOTAL =Sum('price'))['TOTAL']
    x=uuid.uuid4().hex.upper()
    genik=x[16:20]
    for tt in orderitems:
            # if tt.order_date < today:
                tt.recitno = genik
                tt.chek = 2
                tt.save()
    x=uuid.uuid4().hex.upper()
    genid=x[15:20]
    porder = PaymentOrder(
              status = "pending",
              paidat=datetime.date.today(),
              creditnoteno =genik,
              NetAmount=totals,
              userids=pk
            #   receiverName=receiverName
    )
    porder.save()
   
    serializersd = OrderItemSerializer(orderitems, many=True)
    serializer = POrderSerializer(porder, many=False)
    return Response({"status": "success","count":totals,"data" :serializer.data}, status=status.HTTP_200_OK)
@api_view(['GET','PUT']) 
# @permission_classes([IsAuthenticated&IsVendorUser])
def getRecitOfSoldItems(request,pk,pk2):
    orderitems = OrderItem.objects.filter(userid=pk,recitno=pk2)  
    payitems = PaymentOrder.objects.filter(userids=pk,creditnoteno=pk2)
    for tt in payitems:
            # if tt.order_date < today:
                tt.status="paid"
                tt.paidat=datetime.date.today(),
                tt.save()
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data" :serializer.data}, status=status.HTTP_200_OK)
@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getPermanentAddress(request,pk):
    # try:
    perm = PermanentAddress.objects.filter(user=pk).first()
    # except ObjectDoesNotExist:
    #  perm = None
    serializer = PermanentAddressSerializer(perm, many=False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllPermanentAddress(request):
    perm = PermanentAddress.objects.all()
    print(perm)
    serializer = PermanentAddressSerializer(perm, many=True)
    return Response(serializer.data)

@api_view(['PUT'])
def updatePemanentAddress(request, pk):
    data = request.data
    perm = PermanentAddress.objects.filter(user=pk).first()
    perm.address = data['address']
    perm.city = data['city']
    perm.postalCode = data['postalCode']
    perm.country = data['country']
    perm.save()
    serializer = PermanentAddressSerializer(perm, many=False)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getSummaryOfSoldItems(request,pk):
    orderitems = OrderItem.objects.filter(userid=pk)
    totals = OrderItem.objects.filter(userid=pk).aggregate(TOTAL =Sum('price'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"count":totals}, status=status.HTTP_200_OK)
@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getSummaryOfAllSoldItems(request):
    orderitems = OrderItem.objects.all()
    totals = OrderItem.objects.all().aggregate(TOTAL =Sum('price'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"count":totals}, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllSoldItems(request,pk):
    orderitems = OrderItem.objects.filter(userid=pk)
    totals = OrderItem.objects.filter(userid=pk).aggregate(TOTAL =Sum('qty'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"soldproducts": totals}, status=status.HTTP_200_OK)
@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllSoldQuantity(request):
    orderitems = OrderItem.objects.all()
    totals = OrderItem.objects.all().aggregate(TOTAL =Sum('qty'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"soldproducts": totals}, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllSoldItemsToday(request,pk):
    orderitems = OrderItem.objects.filter(soldat=datetime.date.today(),userid=pk)
    totals = OrderItem.objects.filter(soldat=datetime.date.today(),userid=pk).aggregate(TOTAL =Sum('qty'))['TOTAL']
    totalprice = OrderItem.objects.filter(soldat=datetime.date.today(),userid=pk).aggregate(TOTAL =Sum('price'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"totalqty":totals,"price": totalprice}, status=status.HTTP_200_OK)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllSoldItemsTodayAdmin(request):
    orderitems = OrderItem.objects.filter(soldat=datetime.date.today())
    totals = OrderItem.objects.filter(soldat=datetime.date.today()).aggregate(TOTAL =Sum('qty'))['TOTAL']
    totalprice = OrderItem.objects.filter(soldat=datetime.date.today()).aggregate(TOTAL =Sum('price'))['TOTAL']
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response({"status": "success","data":serializer.data,"totalqty":totals,"price": totalprice}, status=status.HTTP_200_OK)



@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllVendorItemsdetails(request,pk):
    orderitems = OrderItem.objects.filter(_id=pk)
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getShopOrderItems(request,pk):
    orderitems = OrderItem.objects.filter(product_id=pk)
    serializer = OrderItemSerializer(orderitems, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAdminUser])
def getMyAdminOrders(request):
    user = request.user
    orders = user.order_set.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated&IsAdminUser])
# def getMyAdminOrder(request):
#     # product = request.product
#     user = request.user
#     orders = Order.Objects.all()
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsAdminUser])
def getMyAdminOrder(request):
    user = request.user
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getMyAdminOrders2(request,pk):
    # product = request.product
    orders = Order.objects.get(_id=pk)
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)
@api_view(['GET'])
@permission_classes([IsAuthenticated&IsVendorUser])
def getMyVendorOrders(request):
    user = request.user
    orders = Order.Objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)



@api_view(['GET'])
# @permission_classes([IsAdminUser])
def getOrders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def updatePayment(request, pk):

    order = Order.objects.get(_id=pk)

    

    order.isPaid = True

    order.paidAt = datetime.now()
  
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)

@api_view(['PUT'])
def ConpleteTransaction(request, pk):

    order = Order.objects.get(_id=pk)

    

    order.isDelivered = True

    order.deliveredAt = datetime.datetime.now()
  
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)

@api_view(['GET'])
def GetAgentCode(request, pk):

    order = Order.objects.filter(agentid=pk)

    serializer = OrderSerial(order, many=True)
    return Response(serializer.data)


@api_view(['PUT'])
def ConpleteTransactionAgent(request, pk):

    order = Order.objects.get(agentid=pk)

    

    order.isDelivered = True

    order.deliveredAt = datetime.datetime.now()
  
    order.save()

    serializer = OrderSerializer(order, many=False)

    return Response(serializer.data)