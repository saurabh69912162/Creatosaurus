from django.db import models

# Create your models here.
from django.core.validators import RegexValidator

from django.contrib.auth.models import (
		BaseUserManager, AbstractBaseUser
	)

USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'


class MyUserManager(BaseUserManager):
	def create_user(self, username, email,first_name,last_name,category,password=None):
		if not email:
			raise ValueError('Users must have an email address')

		user = self.model(
					username = username,
					email = self.normalize_email(email),
				)
		first_name = first_name
		last_name = last_name
		category = category
		user.set_password(password)
		user.save(using=self._db)
		return user
		# user.password = password # bad - do not do this

	def create_superuser(self, username, email,first_name,last_name,category,password=None):
		user = self.create_user(
				username, email,first_name,last_name,category,password=password
			)
		user.is_admin = True
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
	is_staff = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email','first_name','last_name','category']

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





class business_profile_data(models.Model):

	username = models.CharField(max_length=255)
	#username = models.ForeignKey(MyUser,on_delete=models.CASCADE)
	first_name = models.CharField(max_length=255)
	founded = models.DateField(max_length=255)
	company_category = models.CharField(max_length=255)
	website = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	location = models.CharField(max_length=255)
	overview = models.CharField(max_length=500)
	company_size = models.IntegerField()
	field_of_interest = models.CharField(max_length=1000)
	address = models.CharField(max_length=255)
	number = models.IntegerField()
	verified = models.BooleanField(default=False)


	def __str__(self):
		return self.username+'	'+self.email+'	'+self.location

class creator_profile_data(models.Model):

	username = models.CharField(max_length=255)
	skills = models.CharField(max_length=500)
	artist_category = models.CharField(max_length=255)
	website = models.CharField(max_length=255)
	email = models.EmailField(max_length=255)
	location = models.CharField(max_length=255)
	gender = models.CharField(max_length=500)
	description = models.CharField(max_length=1000)
	address = models.CharField(max_length=255)
	number = models.IntegerField()
	verified = models.BooleanField(default=False)

	def __str__(self):
		return self.username+'	'+self.email+'	'+self.location+'	'+self.artist_category
