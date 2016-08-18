from __future__ import unicode_literals

from django.db import models
import re
from django.contrib import messages


# Create your models here.

# class userManager(models.Manager):
#     def validateEmail(self, request, email):
#         EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+.[a-zA-Z]*$')
#         if not EMAIL_REGEX.match(email):
#                 messages.error(request, "Email is not valid")
#                 return False
#             return True
#
# class User(models.Model):
#     first_name = models.CharField(max_length=255)
#     last_name = models.CharField(max_length=255)
#     email = models.EmailField(max_length=255)
#     password = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#
#     objects = userManager()

#models.TextField()
#user_id = models.ForeignKey(User)
