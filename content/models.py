from django.db import models
from django.contrib.auth.models import AbstractUser
from fernet_fields import EncryptedTextField
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed

#Correct sensitive data handling
class OurUsers(models.Model):
    name = models.CharField(max_length=100)
    social_security =EncryptedTextField(max_length=11)
    my_issue = models.TextField()

    class Meta:
        db_table = 'OURUSERS'            

#Non existing handling of sensitive data
class UserData(models.Model):
    name = models.CharField(max_length=100)
    social_security = models.CharField(max_length=11)
    my_issue = models.TextField()

    def __str__(self):
        return self.name
    class Meta:
        db_table = 'USERDATA'     

class Cities(models.Model):
    city_name = models.CharField(max_length=50)
    description = models.TextField()
    pub_date = models.DateTimeField('date published')

    class Meta:
        db_table = 'CITIES'

    def __str__(self):
        return self.city_name

""" class AuditEntry(models.Model):
    action = models.CharField(max_length=64)
    ip = models.GenericIPAddressField(null=True)
    username = models.CharField(max_length=256, null=True)

    def __unicode__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.action, self.username, self.ip)


@receiver(user_logged_in)
def user_logged_in_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_in', ip=ip, username=user.username)


@receiver(user_logged_out)
def user_logged_out_callback(sender, request, user, **kwargs):  
    ip = request.META.get('REMOTE_ADDR')
    AuditEntry.objects.create(action='user_logged_out', ip=ip, username=user.username)


@receiver(user_login_failed)
def user_login_failed_callback(sender, credentials, **kwargs):
    AuditEntry.objects.create(action='user_login_failed', username=credentials.get('username', None)) """