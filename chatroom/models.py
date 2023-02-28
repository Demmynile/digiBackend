from users.models import User
from django.db import models
from django.conf import settings
import datetime

from django.core.cache import cache



# class UserProfile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)

#     def __str__(self):
#         return self.user.username
    
#     def last_seen(self):
#         return cache.get('last_seen_%s' % self.user.username)
    
#     def online(self):
#         if self.last_seen():
#             now = datetime.datetime.now()
#             if now > (self.last_seen() + datetime.timedelta(seconds=settings.USER_ONLINE_TIMEOUT)):
#                 return False
#             else:
#                 return True
#         else: 
#             return False
class Message(models.Model):
    STATUS = (
        ('0', 'New'),
        ('1', 'In Progress'),
        ('2', 'On Hold'),
        ('3' , 'Completed')
    )
    sender = models.CharField( max_length = 200 , blank = True , null = True)        
    receiver = models.CharField( max_length = 200 ,blank = True , null = True)        
    message = models.CharField(max_length=1200, blank=True, null= True)
    senderName = models.CharField(max_length = 200 , blank = True , null = True)
    receiverName = models.CharField(max_length = 200 , blank = True , null = True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null= True)
    isSenderShow = models.BooleanField(default = True, blank=True, null= True)
    isReceiverShow = models.BooleanField(default = True, blank=True, null= True)
    sender_deleted_at = models.DateTimeField(("Sender deleted at"), null=True, blank=True)
    receiver_deleted_at = models.DateTimeField(("Recipient deleted at"), null=True, blank=True)
    status = models.CharField(max_length = 3 , choices = STATUS, default = "0", blank=True, null= True)

    class Meta:
           ordering = ('-created_at',)

class Inbox(models.Model):
      senderName = models.CharField(max_length = 200 , blank = True , null = True)
      receiverName = models.CharField(max_length = 200 , blank = True , null = True)
      sender = models.CharField( max_length = 200 , blank = True , null = True)        
      receiver = models.CharField( max_length = 200 ,blank = True , null = True)    
      is_read = models.BooleanField(default = False, blank=True, null= True)
      created_at = models.DateTimeField(auto_now_add = True, blank=True, null= True)
      isSenderShow = models.BooleanField(default = True, blank=True, null= True)
      isReceiverShow = models.BooleanField(default = True, blank=True, null= True)
      message = models.CharField(max_length = 200, blank=True, null= True)


      class Meta:
           ordering = ('-created_at',)