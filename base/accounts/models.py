# import os
# os.environ["DJANGO_SETTINGS_MODULE"] = "customusermodel.settings"

from django.shortcuts import get_object_or_404
from django.db import models
import uuid
from django.core.validators import RegexValidator
from django.contrib.auth.models import ( BaseUserManager, AbstractBaseUser)
from datetime import datetime, time
from datetime import datetime
import schedule
import time
USERNAME_REGEX = '^[a-zA-Z0-9.+-]*$'

#
# from ..celery123 import *


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, category, date_of_joining, dirtybit, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            username=username,
            email=self.normalize_email(email),
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

    def create_superuser(self, username, email, first_name, last_name, category, date_of_joining, dirtybit,
                         password=None):
        user = self.create_user(
            username, email, first_name, last_name, category, date_of_joining, dirtybit, password=password
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
        validators=[
            RegexValidator(regex=USERNAME_REGEX,
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
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name', 'category', 'date_of_joining', 'dirtybit']

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
            obj = MyUser.objects.get(dirtybit=self.dirtybit)
            creator_profile_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit,
                                                       package_selected=available_package.objects.get(
                                                           package_name='L1'))
            super().save(*args, **kwargs)
        elif self.category == 'Business':
            super().save(*args, **kwargs)
            obj = MyUser.objects.get(dirtybit=self.dirtybit)
            business_profile_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit,
                                                       package_selected=available_package.objects.get(
                                                           package_name='L1'))
            super().save(*args, **kwargs)
        else:
            pass


class business_profile_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    founded = models.DateField(max_length=255, blank=True, null=True)
    company_category = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    # email = models.EmailField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    overview = models.CharField(max_length=500, blank=True, null=True)
    company_size = models.IntegerField(blank=True, null=True)
    field_of_interest = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    cache_hit = models.BooleanField(default=False, blank=True, null=True)


class creator_profile_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(unique=True, blank=True, null=True)
    skills = models.CharField(max_length=500, blank=True, null=True)
    artist_category = models.CharField(max_length=255, blank=True, null=True)
    website = models.CharField(max_length=255, blank=True, null=True)
    # email = models.EmailField(max_length=255,blank=True,null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    gender = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)
    cache_hit = models.BooleanField(default=False, blank=True, null=True)


class connections(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    connection_dirtybit = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    provider = models.CharField(blank=False, null=False, max_length=50)
    account_token = models.CharField(blank=True, null=True, max_length=1000)
    access_token = models.CharField(blank=False, null=False, max_length=1000)
    extra_data = models.TextField(blank=True, null=True, max_length=10000)
    access_expiry = models.DateTimeField(blank=True, null=True)
    long_token = models.CharField(blank=True, null=True, max_length=1000)
    long_expiry = models.DateTimeField(blank=True, null=True)
    account_name = models.CharField(max_length=500, blank=True, null=True)
    account_uid = models.CharField(max_length=500, unique=True, blank=True, null=True)

    def __str__(self):
        return str(self.account_uid)



class available_package(models.Model):
    package_name = models.CharField(max_length=20, blank=False, null=False)
    amount = models.IntegerField(blank=False, null=False)
    queue_size = models.IntegerField(blank=False, null=False)
    account_connection_size = models.IntegerField(blank=False, null=False)
    team_member_size = models.IntegerField(blank=False, null=False)
    package_dirtybit = models.UUIDField(default=uuid.uuid4, blank=False, unique=True, null=True)

    def __str__(self):
        return self.package_name


class current_package_user(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(unique=True, blank=True, null=True)
    package_selected = models.ForeignKey(available_package, on_delete=models.CASCADE, blank=False, null=False)
    queue_size = models.IntegerField(blank=True, null=True)
    account_connection_size = models.IntegerField(blank=True, null=True)
    team_member_size = models.IntegerField(blank=True, null=True)

    def save(self, *args, **kwargs):
        self.queue_size = self.package_selected.queue_size
        self.account_connection_size = self.package_selected.account_connection_size
        self.team_member_size = self.package_selected.team_member_size
        super().save(*args, **kwargs)





class init_schedule(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    self_dirtybit = models.UUIDField(unique=True, default=uuid.uuid4, blank=True, null=True)
    providers = models.CharField(max_length=500, blank=False, null=False)
    content = models.TextField(max_length=63000, blank=True, null=True)
    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    upload_datetime = models.DateTimeField(default=datetime.now, blank=False, null=False)
    image = models.ImageField(upload_to='scheduled_images', blank=True)
    video = models.FileField(upload_to='scheduled_videos', blank=True)

    def __str__(self):
        return str(self.self_dirtybit)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        provider = self.providers.split(',')
        for x in range(len(provider)):
            # print(connections.objects.get(account_uid=provider[x]))
            obj = scheduler_model()
            obj.username = self.username
            obj.dirtybit = self.dirtybit
            obj.provider = connections.objects.get(account_uid=provider[x])
            obj.content = self.content
            obj.scheduled_datetime = self.scheduled_datetime
            obj.upload_datetime = self.upload_datetime
            obj.image = self.image
            obj.video = self.video
            obj.init_schedule_fk = init_schedule.objects.get(self_dirtybit=self.self_dirtybit)
            obj.save()

        super().save(*args, **kwargs)

from datetime import datetime

class scheduler_model(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    init_schedule_fk = models.ForeignKey(init_schedule, on_delete=models.CASCADE, blank=True, null=True)
    schedule_dirtybit = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    provider = models.ForeignKey(connections, on_delete=models.CASCADE)
    content = models.TextField(max_length=63000, blank=True, null=True)
    scheduled_datetime = models.DateTimeField(blank=False, null=False)
    upload_datetime = models.DateTimeField(default=datetime.now, blank=False, null=False)
    image = models.ImageField(upload_to='scheduled_images', blank=True)
    video = models.FileField(upload_to='scheduled_videos', blank=True)
    timestamp = models.BigIntegerField(null=True,blank=True)
    hit = models.BooleanField(default=False)

    def __str__(self):
        return str(self.schedule_dirtybit)


    def save(self, *args, **kwargs):
        import datetime
        import time
        d = datetime.datetime(self.scheduled_datetime.year, self.scheduled_datetime.month, self.scheduled_datetime.day, self.scheduled_datetime.hour,self.scheduled_datetime.minute,self.scheduled_datetime.second)
        epoch = time.mktime(d.timetuple())
        self.timestamp = int(epoch)

        super().save(*args, **kwargs)

class upcomming_queue(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    init_schedule_fk = models.ForeignKey(init_schedule, on_delete=models.CASCADE, blank=True, null=True)
    schedule_dirtybit = models.ForeignKey(scheduler_model, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.BigIntegerField(null=True, blank=True)
    provider = models.ForeignKey(connections, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.timestamp)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.timestamp - datetime.timestamp(datetime.now()))
        # reverse.delay(self.provider.provider,self.timestamp - datetime.timestamp(datetime.now()))