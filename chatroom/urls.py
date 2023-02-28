from django.urls import path,include
from chatroom.views import MessageView,getAllInboxInfo,getAllMessageInfo, getAllInboxContact
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'message', MessageView,)# save my own news
# router.register(r'inbox', InboxView,)# save my own news

urlpatterns = [
    
	# path('chats', ChatRoomView.as_view(), name='chatRoom'),
	# path('chats/<str:roomId>/messages', MessagesView.as_view(), name='messageList'),
	# path('users/<int:userId>/chats', ChatRoomView.as_view(), name='chatRoomList'),
	path('sentmessage/<str:pk>/<str:pk2>/', getAllMessageInfo, name ="getmessage"),# get one mesage for a communication message
    path('inboxmessage/<str:pk>/<str:pk2>/',getAllInboxInfo, name ="getinbox"),# get inbox messages
	path('inboxcontact/<str:pk>/',getAllInboxContact, name ="getinboxcontact"),# get inbox messages
    path('', include(router.urls)),
	
]