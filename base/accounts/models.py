from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)
USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'
from datetime import datetime

class MyUserManager(BaseUserManager):
	def create_user(self, username, email,first_name,last_name,category,date_of_joining,dirtybit,password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					username = username,
					email = self.normalize_email(email),
				)
		user.first_name = first_name
		user.last_name = last_name
		user.category = category
		user.date_of_joining = date_of_joining
		user.dirtybit = dirtybit
		user.set_password(password)
		user.save(using=self._db)

		return user
		# user.password = password # bad - do not do this

	def create_superuser(self, username, email,first_name,last_name,category,date_of_joining,dirtybit,password=None):
		user = self.create_user(
				username, email,first_name,last_name,category,date_of_joining,dirtybit,password=password
			)
		user.first_name = first_name
		user.last_name = last_name
		user.date_of_joining = date_of_joining
		user.dirtybit = dirtybit
		user.is_admin = True
		user.cache_hit = False
		user.email_verified = True
		user.phone_verified = True
		user.is_staff = True
		user.save(using=self._db)
		return user



class MyUser(AbstractBaseUser):
	username = models.CharField(
					max_length=300,
					validators = [
						RegexValidator(regex = USERNAME_REGEX,
										message='Username must be alphanumeric or contain numbers',
										code='invalid_username'
							)],
					unique=True
				)
	email = models.EmailField(
			max_length=255,
			unique=True,
			verbose_name='email address'
		)
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	category = models.CharField(max_length=10, default='creator')
	is_admin = models.BooleanField(default=False)
	cache_hit = models.BooleanField(default=False)
	email_verified = models.BooleanField(default=False)
	phone_verified = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)
	date_of_joining = models.DateTimeField(default=datetime.now)
	dirtybit = models.UUIDField(default=uuid.uuid4, unique=True)
	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','first_name','last_name','category','date_of_joining','dirtybit']

	def __str__(self):
		return self.email

	def get_short_name(self):
		# The user is identified by their email address
		return self.email


	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		# Simplest possible answer: Yes, always
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		# Simplest possible answer: Yes, always
		return True

	def save(self, *args, **kwargs):
		if self.category == 'Creator':
			super().save(*args, **kwargs)
			obj = MyUser.objects.get(dirtybit = self.dirtybit)
			creator_profile_data.objects.get_or_create(username = obj,dirtybit=self.dirtybit)
			super().save(*args, **kwargs)
		elif self.category == 'Business':
			super().save(*args, **kwargs)
			obj = MyUser.objects.get(dirtybit=self.dirtybit)
			business_profile_data.objects.get_or_create(username = obj, dirtybit=self.dirtybit)
			super().save(*args, **kwargs)
		else:
			pass




class business_profile_data(models.Model):

	username = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	dirtybit = models.UUIDField(unique=True, blank=True,null=True)
	first_name = models.CharField(max_length=255,blank=True,null=True)
	founded = models.DateField(max_length=255,blank=True,null=True)
	company_category = models.CharField(max_length=255,blank=True,null=True)
	website = models.CharField(max_length=255,blank=True,null=True)
	# email = models.EmailField(max_length=255,blank=True,null=True)
	location = models.CharField(max_length=255,blank=True,null=True)
	overview = models.CharField(max_length=500,blank=True,null=True)
	company_size = models.IntegerField(blank=True,null=True)
	field_of_interest = models.CharField(max_length=1000,blank=True,null=True)
	address = models.CharField(max_length=255,blank=True,null=True)
	number = models.IntegerField(blank=True,null=True)
	cache_hit = models.BooleanField(default=False,blank=True,null=True)

class creator_profile_data(models.Model):

	username = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	dirtybit = models.UUIDField(unique=True,blank=True,null=True)
	skills = models.CharField(max_length=500,blank=True,null=True)
	artist_category = models.CharField(max_length=255,blank=True,null=True)
	website = models.CharField(max_length=255,blank=True,null=True)
	# email = models.EmailField(max_length=255,blank=True,null=True)
	location = models.CharField(max_length=255,blank=True,null=True)
	gender = models.CharField(max_length=500,blank=True,null=True)
	description = models.CharField(max_length=1000,blank=True,null=True)
	address = models.CharField(max_length=255,blank=True,null=True)
	number = models.IntegerField(blank=True,null=True)
	cache_hit = models.BooleanField(default=False,blank=True,null=True)
