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


def init_noti(username,u_code):
    print(u_code)
    obj = notification_pannel()
    obj.username = username
    obj.u_code = u_code
    obj.save()
    return True


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
            username, email, first_name, last_name,category, date_of_joining, dirtybit, password=password
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
        user.new_user_notify = False
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
    new_user_notify = models.BooleanField(default=False)

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
            try:
                query_set = current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            except:
                query_set = current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit, package_selected = available_package.objects.get(package_name = 'L1'))

            user_connection_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)


            super().save(*args, **kwargs)
        elif self.category == 'Business':
            super().save(*args, **kwargs)
            obj = MyUser.objects.get(dirtybit=self.dirtybit)
            business_profile_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)

            try:
                query_set = current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit)
            except:
                query_set = current_package_user.objects.get_or_create(username=obj, dirtybit=self.dirtybit,
                                                                       package_selected=available_package.objects.get(
                                                                           package_name='L1'))

            user_connection_data.objects.get_or_create(username=obj, dirtybit=self.dirtybit)

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


class selected_connections(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    connection_dirtybit = models.UUIDField(default=uuid.uuid4, unique=True, blank=True, null=True)
    provider = models.CharField(blank=False, null=False, max_length=50)
    account_token = models.TextField(blank=True, null=True, max_length=1000)
    access_token = models.TextField(blank=False, null=False, max_length=1000)
    access_token_secret = models.TextField(blank=True, null=True, max_length=1000)
    extra_data = models.TextField(blank=True, null=True, max_length=10000)
    access_expiry = models.DateTimeField(blank=True, null=True)
    long_token = models.CharField(blank=True, null=True, max_length=1000)
    long_expiry = models.DateTimeField(blank=True, null=True)
    account_name = models.CharField(max_length=500, blank=True, null=True)
    account_uid = models.CharField(max_length=500, unique=True, blank=True, null=True)
    selected = models.BooleanField(default=False)
    within_limit = models.BooleanField(default=True)

    def __str__(self):
        return str(self.account_uid)

    def save(self, *args, **kwargs):

        super().save(*args, **kwargs)




class user_connection_data(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True, unique=True)
    max_connections = models.IntegerField(default=8)
    total_connections = models.IntegerField(default=0)
    max_seleceted_connections = models.IntegerField(default=8)
    total_seleceted_connections = models.IntegerField(default=0)
    max_team_members = models.IntegerField(default=0)
    total_team_members = models.IntegerField(default=0)


class queue_statistics(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    provider = models.CharField(max_length=1000,blank=True, null=True)
    selected_account = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    account_name = models.CharField(max_length=1000,blank=True, null=True)
    account_uid = models.CharField(max_length=500,unique=True,blank=True,null=True)
    limit = models.IntegerField(default=10)
    left = models.IntegerField(default=10)

    def save(self, *args, **kwargs):

        check_lim = current_package_user.objects.get(username= self.username)
        # self.limit = check_lim.queue_size

        if self.left <= 0:
            obj = selected_connections.objects.get(account_uid = self.selected_account)
            obj.within_limit = False
            obj.save()
        elif self.left > 0:
            obj = selected_connections.objects.get(account_uid=self.selected_account)
            obj.within_limit = True
            obj.save()
        else:
            pass


        super().save(*args, **kwargs)





class available_package(models.Model):
    package_name = models.CharField(max_length=20, blank=False, null=False)
    package_id_int = models.IntegerField(blank=False, null=False)
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
    package_selected = models.ForeignKey(available_package, on_delete=models.CASCADE, blank=False, null=False,)
    queue_size = models.IntegerField(blank=True, null=True)
    account_connection_size = models.IntegerField(blank=True, null=True)
    team_member_size = models.IntegerField(blank=True, null=True)
    assigned = models.BooleanField(default=False)
    package_exipry = models.BigIntegerField(default=0,blank=True,null=True)
    last_package = models.CharField(max_length=10,default='L1')


    def save(self, *args, **kwargs):
        pack = available_package.objects.get(package_name='L1')
        if not self.package_selected == pack:
            from datetime import datetime, timedelta
            expiry = datetime.now() + timedelta(days=30)
            import datetime
            d = datetime.datetime(expiry.year, expiry.month, expiry.day,
                                  expiry.hour, expiry.minute,
                                  expiry.second)
            epoch = time.mktime(d.timetuple())
            self.package_exipry = int(epoch)
        else:
            self.package_exipry = -1


        if self.assigned == False:
            self.assigned = True
            self.package_selected = available_package.objects.get(package_name = 'L1')

        self.queue_size = self.package_selected.queue_size
        self.account_connection_size = self.package_selected.account_connection_size
        self.team_member_size = self.package_selected.team_member_size

        change_q = queue_statistics.objects.filter(username=self.username)

        new_pack = available_package.objects.get(package_name = self.package_selected.package_name).package_name

        print('i am the new pack',new_pack)

        for x in change_q:

            if new_pack == 'L2' and self.last_package == 'L1':
                x.limit = 12
                x.left = x.left+2
                x.save()
                self.last_package = 'L1'
                print('l1 -> l2')

            elif new_pack == 'L3' and self.last_package == 'L1':
                x.limit = 14
                x.left = x.left + 4
                x.save()
                self.last_package = 'L1'
                print('l1 -> l3')

            elif new_pack == 'L4' and self.last_package == 'L1':
                x.limit = 16
                x.left = x.left + 6
                x.save()
                self.last_package = 'L1'
                print('l1 -> l4')

            elif new_pack == 'L3' and self.last_package == 'L2':
                x.limit = 14
                x.left = x.left + 2
                x.save()
                self.last_package = 'L2'
                print('l2 -> l3')

            elif new_pack == 'L4' and self.last_package == 'L2':
                x.limit = 16
                x.left = x.left + 4
                x.save()
                self.last_package = 'L2'
                print('l2 -> l4')

            elif new_pack == 'L4' and self.last_package == 'L3':
                x.limit = 16
                x.left = x.left + 2
                x.save()
                self.last_package = 'L3'
                print('l3 -> l4')



            elif new_pack == 'L1' and self.last_package == 'L4':
                x.limit = 10
                if x.left-x.left >= 6:
                    x.left = 0
                else:
                    x.left = x.left - 6

                print('l4 -> l1')
                x.save()
                self.last_package = 'L4'

            elif new_pack == 'L1' and self.last_package == 'L3':
                x.limit = 10
                if x.left-x.left >= 4:
                    x.left = 0
                else:
                    x.left = x.left - 4
                print('l3 -> l1')
                x.save()
                self.last_package = 'L3'

            elif new_pack == 'L1' and self.last_package == 'L2':
                x.limit = 10
                if x.left-x.left >= 2:
                    x.left = 0
                else:
                    x.left = x.left - 2
                print('l2 -> l1')
                x.save()
                self.last_package = 'L2'

            elif new_pack == 'L1' and self.last_package == 'L1':
                pass
                print('l1 -> l1')
                self.last_package = 'L1'

            else:
                pass
                print(self.last_package)
                print(type(new_pack))
                print('i got passed')
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
            obj = scheduler_model()
            obj.username = self.username
            obj.dirtybit = self.dirtybit
            obj.provider = selected_connections.objects.get(account_uid=provider[x])
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
    provider = models.ForeignKey(selected_connections, on_delete=models.CASCADE)
    content = models.TextField(max_length=63000, blank=True, null=True)
    scheduled_datetime = models.DateTimeField(blank=True, null=True)
    upload_datetime = models.DateTimeField(default=datetime.now, blank=False, null=False)
    image = models.ImageField(upload_to='media_uploaded/', blank=True)
    video = models.FileField(upload_to='scheduled_videos', blank=True)
    timestamp = models.BigIntegerField(null=True,blank=True)
    hit = models.BooleanField(default=False)
    calc = models.BooleanField(default=False)
    def __str__(self):
        return str(self.schedule_dirtybit)


    def save(self, *args, **kwargs):
        if not self.scheduled_datetime is None:
            import datetime
            import time
            d = datetime.datetime(self.scheduled_datetime.year, self.scheduled_datetime.month, self.scheduled_datetime.day, self.scheduled_datetime.hour,self.scheduled_datetime.minute,self.scheduled_datetime.second)
            epoch = time.mktime(d.timetuple())
            self.timestamp = int(epoch)

            if self.calc is False :
                self.calc = True
                obj = queue_statistics.objects.get(username = self.username, selected_account = self.provider)
                obj.left  = obj.left - 1
                obj.save()
                init_noti(self.username, 199)

        if self.hit == True:
            obj = queue_statistics.objects.get(username=self.username, selected_account=self.provider)
            obj.left = obj.left + 1
            obj.save()
            init_noti(self.username,200)

        super().save(*args, **kwargs)

class upcomming_queue(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    dirtybit = models.UUIDField(blank=True, null=True)
    init_schedule_fk = models.ForeignKey(init_schedule, on_delete=models.CASCADE, blank=True, null=True)
    schedule_dirtybit = models.ForeignKey(scheduler_model, on_delete=models.CASCADE, blank=True, null=True)
    timestamp = models.BigIntegerField(null=True, blank=True)
    provider = models.ForeignKey(selected_connections, on_delete=models.CASCADE,blank=True,null=True)

    def __str__(self):
        return str(self.timestamp)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        print(self.timestamp - datetime.timestamp(datetime.now()))
        # reverse.delay(self.provider.provider,self.timestamp - datetime.timestamp(datetime.now()))




class temp_data(models.Model):
    rand_save_string = models.CharField(max_length=64, null=True, blank=True)
    date = models.CharField(max_length=12,blank=True, null=True)
    accs = models.CharField(max_length=1000, null=True, blank=True)
    accs_name = models.CharField(max_length=1000, null=True, blank=True)
    accs_provider = models.CharField(max_length=1000, null=True, blank=True)
    cont = models.CharField(max_length=50000, null=True, blank=True)
    img = models.ImageField(upload_to='media_uploaded/',null=True, blank=True)
    uid_zip = models.CharField(max_length=3000, null=True, blank=True)
    def __str__(self):
        return self.rand_save_string

import razorpay
import json
api_key = "rzp_test_fFP191cDNSQADl"
api_secret = "csm3OLcOwNTABuHnu8D0qwBZ"
client = razorpay.Client(auth=(api_key, api_secret))


class user_transaction(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    c_transaction_id = models.UUIDField(default=uuid.uuid4, unique=True, blank=False, null=True)
    transaction_start = models.DateTimeField(blank=False, null=False, default=datetime.now)
    current_package = models.CharField(max_length=100,blank=False,null=True)
    upgrade_package = models.CharField(max_length=100,blank=False,null=True)
    from_date = models.BigIntegerField(blank=False,null=False)
    to_date = models.BigIntegerField(blank=False,null=False)
    razorpay_payment_url = models.URLField(max_length=2000,blank=True)
    razorpay_id = models.CharField(max_length=255, blank=True)
    customer_id = models.CharField(max_length=255, blank=True, null=True, default='NA')
    order_id = models.CharField(max_length=255, blank=True, null=True, default='NA')
    inv_id = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=255, default="Pending")
    amount = models.BigIntegerField(blank=False,null=False, default=99900)

    def save(self, *args, **kwargs):
        if self.razorpay_id == '':
            ts = time.time()
            DATA = {
                "customer": {
                    "name": self.username.first_name+' '+self.username.last_name,
                    "email": self.username.email,
                },
                "type": "link",
                "amount": self.amount,
                "expire_by": int(ts) + 960,
                "currency": "INR",
                "description": self.upgrade_package +" - Creatosaurus"
            }
            final_data = client.invoice.create(data=DATA)
            for key,value in final_data.items():
                if key == 'id':
                    print(value)
                    break

            self.razorpay_id = json.dumps(final_data["id"]).strip('"')
            self.inv_id = value
            self.order_id = json.dumps(final_data["order_id"]).strip('"')
            self.customer_id = json.dumps(final_data["customer_details"]["id"]).strip('"')
            self.razorpay_payment_url = json.dumps(final_data["short_url"]).strip('"')
            self.razorpay_id = json.dumps(final_data["order_id"]).strip('"')
        print('Done, im in models.py')
        super().save(*args, **kwargs)

        if self.status == 'Paid':
            obj = available_package.objects.get(package_name =self.upgrade_package)
            change = current_package_user.objects.get(username = self.username)
            change.package_selected = obj
            change.last_package = self.current_package
            change.save()

            if self.upgrade_package == 'L2':
                init_noti(self.username, 102)
            elif self.upgrade_package == 'L3':
                init_noti(self.username, 103)
            elif self.upgrade_package == 'L4':
                init_noti(self.username, 104)



class notification_pannel(models.Model):
    username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)
    read_hit = models.BooleanField(default=False)
    mark_as_read_hit = models.BooleanField(default=False)
    read_hit_time = models.DateTimeField(blank=True,null=True)
    message = models.CharField(max_length=256,blank=True,null=True)
    follow_link = models.URLField(blank=True,null=True)
    u_code = models.IntegerField(blank=True,null=True)

    def save(self, *args, **kwargs):
        if self.read_hit == True:
            self.read_hit_time = datetime.now()
        if self.mark_as_read_hit == True:
            self.read_hit_time = datetime.now()

        if self.read_hit == False:
            if self.u_code == 102:
                self.message = 'Payment completed Successful,Your Package has been upgraded to L2'
                self.follow_link = 'https://localhost:8000/package/'

            elif self.u_code == 103:
                self.message = 'Payment completed Successful,Your Package has been upgraded to L3'
                self.follow_link = 'https://localhost:8000/package/'

            elif self.u_code == 104:
                self.message = 'Payment completed Successful,Your Package has been upgraded to L4'
                self.follow_link = 'https://localhost:8000/package/'

            elif self.u_code == 101: # Degrading WARNING from l2,l3 or l4 to l1
                self.message = 'Your Package will expire soon, buy a new one in order to keep your data in queue'
                self.follow_link = 'https://localhost:8000/package/'

            elif self.u_code == 100:  # Degraded
                self.message = 'Your Package has expired, Upgrade Now'
                self.follow_link = 'https://localhost:8000/package/'

            elif self.u_code == 200:  # posted successfully
                self.message = 'Your Scheduled Item has been sent successfully, Add more to the Queue'
                self.follow_link = 'https://localhost:8000/schedule-this-month/'

            elif self.u_code == 199:  # placed in queue successfully
                self.message = 'Your Item has been placed in the Queue successfully, Add More'
                self.follow_link = 'https://localhost:8000/schedule-this-month/'

            elif self.u_code == 300:  # account added in selected accounts
                self.message = 'Account setup successful'
            elif self.u_code == 301:  # account added in selected accounts
                self.message = 'Account disconnected successful'
                self.follow_link = 'https://localhost:8000/configure'


            else:
                pass
        super().save(*args, **kwargs)

