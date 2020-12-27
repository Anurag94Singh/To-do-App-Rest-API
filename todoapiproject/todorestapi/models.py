# models.py
from django.db import models

from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'), reset_password_token.key)

    send_mail(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )


class Users(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,unique=True)
    role = models.CharField(max_length=60)
    def __str__(self):
        return self.name

class Status(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,unique=True)
    def __str__(self):
        return self.name

class TaskStatus(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60)

    def __str__(self):
        return self.name

class Tasks(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=60,unique=True)
    description = models.CharField(max_length=200)
    createdby = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='createdby')
    status = models.ForeignKey(TaskStatus, on_delete=models.CASCADE, related_name='status')

    def __str__(self):
        return self.name

class TaskMapping(models.Model):
    status = models.CharField(max_length=60)
    task = models.ForeignKey(Tasks, on_delete=models.CASCADE, related_name='task')
    student = models.ForeignKey(Users, on_delete=models.CASCADE, related_name='student')


class UserTaskMapping(models.Model):
    username = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='name',default=1, related_name='username')
    status = models.CharField(max_length=60)
    taskid = models.ForeignKey(Tasks, on_delete=models.CASCADE, to_field='id',default=1, related_name='taskid')
    taskname = models.ForeignKey(Tasks, on_delete=models.CASCADE, to_field='name',default=1, related_name='taskname')
    userid = models.ForeignKey(Users, on_delete=models.CASCADE, to_field='id',default=1, related_name='userid')

    class Meta:
       managed = False
