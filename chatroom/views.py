from rest_framework .viewsets import ModelViewSet
from django.shortcuts import render ,get_object_or_404
from django.utils import timezone
from .serializers import MessageSerializers,InboxSerializers, InboxSerializer
from users.api.serializers import UserSerializer
from users.models import User
from django.http import JsonResponse
from .models import Message,Inbox
from rest_framework.response import Response
from rest_framework.decorators import action,api_view
from django.http import HttpResponse
from rest_framework.parsers import JSONParser
from django.core import serializers
from rest_framework import filters
from django.db.models import Q
from django.http import Http404,HttpResponseRedirect


class MessageView(ModelViewSet):
    # search_fields = ['receiver']
    # filter_backends = (filters.SearchFilter,)
    queryset = Message.objects.filter()
    serializer_class = MessageSerializers
    # permission_classes = (IsAuthenticated,)

    @action(detail = False, methods=['POST'])
    def compose(self , request ):
        sender =   request.data.get('sender')
        print(sender)
        receiverName = request.data.get('receiverName')
        print(receiverName)
        senderName =   request.data.get('senderName')
        print(senderName)
        receiver = request.data.get('receiver')
        print(receiver)
        message = request.data.get('message')
        print (message)

        msg = Message(
              sender = sender,
              receiver= receiver,
              message=message,
              senderName=senderName,
              receiverName=receiverName
        )
        msg.save()
        ibx = Inbox(
              sender = sender,
              receiver= receiver,
              message=message,
              senderName=senderName,
              receiverName=receiverName
        )
        ibx.save()
        serializer = MessageSerializers(msg, many=False)
        return Response(serializer.data)
        

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllInboxInfo(request,pk,pk2):
    inbox = Inbox.objects.filter(sender= pk2,receiver=pk).values().reverse()
    inbox.is_read =True
    # inbox.save()
    serializer = InboxSerializers(inbox, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllMessageInfo(request,pk,pk2):
    msg = Message.objects.filter(sender=pk,receiver=pk2).values().reverse()
    serializer = MessageSerializers(msg, many=True)
    return Response(serializer.data)

@api_view(['GET'])
# @permission_classes([IsAuthenticated&IsVendorUser])
def getAllInboxContact(request,pk):
    inbox = Inbox.objects.filter(receiver=pk).values().reverse()
    serializer = InboxSerializer(inbox, many=True)
    return Response(serializer.data)