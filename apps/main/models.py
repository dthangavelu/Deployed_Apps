from __future__ import unicode_literals

from django.db import models
from datetime import datetime
import bcrypt


# Create your models here.

class UserManager(models.Manager):
	def login_validator(self, postData):
		errors = {}		
		form_email = postData['email']	
		form_email = form_email.lower()
		form_pwd = postData['password']
		
		users = User.objects.filter(email = form_email)
		
		if not users:
			errors['email'] = "Email not found in system. Please register!"			
		else:
			isCorrectPwd = bcrypt.checkpw( form_pwd.encode(), users[0].password.encode())			
			if isCorrectPwd == False:
				errors['password'] = "Invalid password. Please try again!"
		return errors		
		
class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)	
	password = models.CharField(max_length=255)	
	dob = models.DateTimeField()	
	created_at = models.DateTimeField(auto_now_add=True)	
	updated_at = models.DateTimeField(default=datetime.now)		
	objects = UserManager()
	
	def __repr__(self):
		return "\nname: {} | alias: {} | email: {} | password: {} | dob: {}\n".format(self.name, self.alias, self.email, self.password, self.dob)
		
class Poke(models.Model):
	poker = models.ForeignKey(User, related_name = "poked_by")
	user_who_is_poked = models.ForeignKey(User, related_name = "user_who_pokes")
	
	def __repr__(self):
		return "\poker: {} | whois poked: \n".format(self.poker, self.user_who_is_poked)
	