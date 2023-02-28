
from django.urls import path,include
from users.api import users_views as views
from users.api import product_views as viewss
from users.api import orders_views as vie
from django.views.decorators.csrf import csrf_exempt
# from base.views.user_views import UserList 
from rest_framework import routers

router = routers.DefaultRouter()
urlpatterns = [
    path('registerv/', views.VendorSignupView.as_view(), name ="registervendor"),# vendor registration
    path('updatev/<str:pk>/', views.updateVendorLogin, name ="updatevendor"),# update vendor login details
    path('updatevendid/<str:pk>/', views.updateVendid, name ="updatevendorid"),# update vendorid 
    path('updatevendlogo/<str:pk>/', views.updateVendlogo, name ="updatevendorid"),# update vendor logo
    path('registera/', csrf_exempt(views.AdminSignupView.as_view()), name ="registeradmin"),# Admin registration
    path('approvedproducts/<str:pk>/', viewss.getAdminApprovedProducts, name="ApprovedAdminProducts"), #Filter out all unapproved products for admin
    path('approvedproductscount/', viewss.getAdminApprovedProductsCount, name="ApprovedAdminProductsCount"), #Filter out all unapproved products for admin
    path('approvedusers/<str:pk>/', views.getApprovedUsers, name="ApprovedAdminUsers"), #Filter out all unapproved users for admin
    path('vendorders/<str:pk>/', csrf_exempt(vie.getShopOrderItems), name ="getordersiTEMS"),
    path('adminsordered/<str:pk>/', csrf_exempt(vie.getMyAdminOrders2), name ="geteachadminorder"),
    path('buyerorder/payment/<str:pk>/', csrf_exempt(vie.updatePayment), name ="getBuyerOrder"),
    path('buyerorderagent/payment/', csrf_exempt(vie.addOrderItemsDeliver), name ="getBuyerOrderAgent"),
    path('allvendorders/<str:pk>/', csrf_exempt(vie.getAllVendorItems), name ="getvenditems"),
    path('allordersdetails/<str:pk>/', csrf_exempt(vie.getAllVendorItemsdetails), name ="getvenditemsdetails"),
    path('vendordersorders/<str:pk>/', csrf_exempt(vie.getShopOrders), name ="getorders"),
    path('getagentcode/<str:pk>/', csrf_exempt(vie.GetAgentCode), name ="agentcode"),
    path('agentpay/<str:pk>/', csrf_exempt(vie.ConpleteTransactionAgent), name ="complete agent transaction"),
    path('solditems/<str:pk>/', csrf_exempt(vie.getAllSoldItems), name ="getorders"),
    path('soldtoday/<str:pk>/', csrf_exempt(vie.getAllSoldItemsToday), name ="getorders"),
    path('summarysold/<str:pk>/', csrf_exempt(vie.getSummaryOfSoldItems), name ="getorders"),
    path('amountsold/<str:pk>/', csrf_exempt(vie.getAmountOfSoldItems), name ="getamountorders"),
    path('recitsold/<str:pk>/<str:pk2>/', csrf_exempt(vie.getRecitOfSoldItems), name ="getrecitorders"),
    path('alitemsold/', csrf_exempt(vie.getAllItemsdetails), name ="getitemsold"),
     path('payorderitems/', csrf_exempt(vie.getAllPaymentOrders), name ="getitemsold"),
    path('ord/', csrf_exempt(vie.getMyAdminOrder), name ="agetorders"),
    path('getorders/', csrf_exempt(vie.getMyOrders), name ="getmyorders"),
    path('getAlllorders/', csrf_exempt(vie.getOrders), name ="getallorders"),
    path('additems/', csrf_exempt(vie.addOrderItems), name ="addorderiems"),
    path('orderid/', csrf_exempt(vie.getOrderById), name ="orderid"),
    path('registerb/', views.BuyerSignupView.as_view(), name ="registerbuyer"),
    path('update/<str:pk>/', viewss.updateProduct, name="product-update"),
    path('updateusers/<str:pk>/', views.updateUser, name ="updateusers"),
    path('create/', viewss.createProduct, name="product-create"),
    path('updatevendorproduct/<str:pk>/', viewss.updateVendorProduct, name="product-vendor-update"),
    path('updateimageproduct/<str:pk>/', viewss.updateImageProduct, name="product-vendor-update"),# Thi is the API to use to update the vendors product
    path('getallusers/', views.getUsers, name="getallUsers"),
    path('getuserbyid/<str:pk>/', views.getUserById, name="getallUsersid"),
    path('vendorbyid/<str:pk>/', views.getVendorUserById, name="vendorUsersid"),
    path('updateprofile/<str:pk>/', views.updateVendorProfile, name="updateprofile"),
    path('getprodid/<str:pk>/', viewss.getAdminProductByIds, name="getAdminuserid"),
    path('upload/', viewss.uploadImage, name="image-upload"),
    path('approved/<str:pk>/', viewss.getApprovedProducts, name="ApprovedProducts"),
    path('myproduct/<str:pk>/', viewss.getProductById, name="myproduct"),
    path('adminproduct/<str:pk>/', viewss.getAdminProductById, name="myproduct"),
    path('supercat/', viewss.SuperCategoryViewSet.as_view({'get': 'list'}), name="supercategory"),
    path('category/<str:pk>/', viewss.getCategory, name="category"),
    path('subcat/<str:pk>/', viewss.getSubcategory, name="subcategory"),
    path('items/<str:pk>/', viewss.getItems, name="myitems"),
    path('productcount/', viewss.getMyProductsCounts, name="Product Counts"), #get my product count
    path('productcategory/<str:pk>/', viewss.getProductCategory, name="prodcategory"),
    path('productsubcat/<str:pk>/', viewss.getProductSubCategory, name="prodsubcategory"),
    path('locations/<str:pk>/', viewss.getProductLocation, name="locations"),
    path('productsupcategory/<str:pk>/', viewss.getProductLocation, name="productsupcategory"),
    path('shop/<str:pk>/', viewss.getShopProducts, name="shop"),
    path('myorderprod/<str:pk>/', viewss.GetOrderdProduct, name="myproductorderd"),
    path('myproducts/', viewss.getMyProducts, name="myproducts"),
    path('vendprofile/<str:pk>/', views.getVendorProfile, name="vendorsprofile"),
    path('proddetails/<str:pk>/', viewss.getBuyerProduct, name="buyerproducts"),
    path('getproducts/', viewss.getProducts, name="getproducts"),
    path('getallproducts/', viewss.getallProducts, name="getallproducts"),
    path('login/',views.CustomAuthToken.as_view(), name='auth-token'),
    path('logout/', views.LogoutView.as_view(), name='logout-view'),
    path('vendor/dashboard/', views.VendorOnlyView.as_view(), name='vendor-dashboard'),
    path('client/dashboard/', views.BuyerOnlyView.as_view(), name='client-dashboard'),
    # URL form "/api/users/1"
    path('userss/<int:pk>', views.user_list, name='user-detail'),      # GET request for user with id
    path('userss/', views.user_list, name='user-list'), #get all users
    path('shopvisit/<int:pk>/', views.getShopViews, name='shopviews'),   # number of shop visits
    path('userbuyer/', views.getBuyerInfo, name='user-list-buyer'), #get buyer info
    path('uservendor/', views.getVendoInfo, name='user-list-vendor'), #get buyer info
    path('orddelivery/<str:pk>/', csrf_exempt(vie.ConpleteTransaction), name ="completed transaction"),# 
    path('allsolditemsadmin/', csrf_exempt(vie.getAllSoldItemsTodayAdmin), name ="getallorderssold"),
    path('summarysoldall/', csrf_exempt(vie.getSummaryOfAllSoldItems), name ="get eeverythingsolsofar in admin"),
    path('uservisits/', views.getAllVisits, name='user-list-visits'), #get visits info
    path('updateaddress/<str:pk>/', csrf_exempt(vie.updatePemanentAddress), name ="code to update buyers address"),
    path('getupdatedaddress/<str:pk>/', csrf_exempt(vie.getPermanentAddress), name ="get buyers address"),
    path('getalladdress/', csrf_exempt(vie.getAllPermanentAddress), name ="get buyers address"),

]