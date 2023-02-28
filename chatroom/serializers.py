from rest_framework import serializers
from . models import Message , Inbox
from users.models import User
from django.http import HttpResponse
from rest_framework.response import Response







class UserSerializer(serializers.ModelSerializer):
    """For Serializing User"""
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password']


class MessageSerializers(serializers.ModelSerializer):
    # sender   = serializers.SlugRelatedField(many=False, slug_field='name', queryset=User.objects.all())
    # receiver = serializers.SlugRelatedField(many=False, slug_field='name', queryset=User.objects.all())
    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'senderName','receiverName','created_at']


class InboxSerializers(serializers.ModelSerializer):

    class Meta:
        model = Inbox
        fields = ['sender', 'receiver', 'message', 'senderName','receiverName','created_at']

class InboxSerializer(serializers.ModelSerializer):
	
    class Meta:
        model = Inbox
        fields = ['sender','senderName','created_at']