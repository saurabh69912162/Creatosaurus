from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import business_profile_data, creator_profile_data
from .forms import UserCreationForm
from .models import *
admin.site.unregister(Group)
# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username','email','is_admin','first_name','last_name','category','date_of_joining','dirtybit')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','email','first_name','last_name','category','password','date_of_joining','dirtybit')}),
			('Permissions', {'fields': ('is_admin','email_verified','phone_verified','cache_hit')})
		)
	search_fields = ('username','email','first_name','last_name','category','date_of_joining','dirtybit')
	ordering = ('username','email','last_name','first_name')

	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)


class creator_profile_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','skills','artist_category','location','cache_hit')
	list_filter = ('skills',)

	fieldsets = (
			(None, {'fields': ('username','dirtybit','skills','artist_category','location','cache_hit')}),
			('Description', {'fields': ('description',)})
		)
	search_fields = ('username','dirtybit','skills','artist_category','location','cache_hit')
	ordering = ('username','dirtybit','skills','artist_category','location','cache_hit')

	filter_horizontal = ()


admin.site.register(creator_profile_data, creator_profile_data_admin)



class business_profile_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')
	list_filter = ('company_category','location')

	fieldsets = (
			(None, {'fields': ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')}),
			('Description', {'fields': ('overview',)})
		)
	search_fields = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')
	ordering = ('username','dirtybit','first_name','company_category','location','field_of_interest','cache_hit')

	filter_horizontal = ()


admin.site.register(business_profile_data, business_profile_data_admin)

class selected_connections_admin(admin.ModelAdmin):

	list_display = ('username','within_limit','selected','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')
	list_filter = ('provider',)

	fieldsets = (
			(None, {'fields': ('username','within_limit','selected','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','access_expiry','long_token','long_expiry')}),
			('Description', {'fields': ('extra_data',)})
		)
	search_fields = ('username','selected','account_name','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')
	ordering = ('username','within_limit','selected','account_name','account_token','access_token_secret','account_uid','dirtybit','connection_dirtybit','provider','access_token','extra_data','access_expiry','long_token','long_expiry')

	filter_horizontal = ()


admin.site.register(selected_connections, selected_connections_admin)



class current_package_user_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','package_selected','queue_size','account_connection_size','team_member_size')
	list_filter = ('package_selected',)


	search_fields = ('username','dirtybit','package_selected','queue_size','account_connection_size','team_member_size')
	ordering = ('username','dirtybit','package_selected','queue_size','account_connection_size','team_member_size')

	filter_horizontal = ()


admin.site.register(current_package_user, current_package_user_admin)



	
class available_package_admin(admin.ModelAdmin):

	list_display = ('package_name','package_id_int','amount','queue_size','account_connection_size','team_member_size','package_dirtybit')

	filter_horizontal = ()


admin.site.register(available_package, available_package_admin)



class scheduler_model_admin(admin.ModelAdmin):

	list_display = ('hit','calc','username','dirtybit','init_schedule_fk','schedule_dirtybit','provider','content','scheduled_datetime','timestamp','upload_datetime','image','video')
	ordering = ['timestamp']
	filter_horizontal = ()


admin.site.register(scheduler_model,scheduler_model_admin)


class init_schedule_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','self_dirtybit','providers','content','scheduled_datetime','upload_datetime','image','video')

	filter_horizontal = ()

admin.site.register(init_schedule, init_schedule_admin)


class upcomming_queue_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','init_schedule_fk','schedule_dirtybit','timestamp')
	ordering = ['timestamp']
	filter_horizontal = ()

admin.site.register(upcomming_queue, upcomming_queue_admin)




class user_connection_data_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','max_connections','total_connections','max_seleceted_connections','total_seleceted_connections','max_team_members','total_team_members',)

	filter_horizontal = ()

admin.site.register(user_connection_data, user_connection_data_admin)


class queue_statistics_admin(admin.ModelAdmin):

	list_display = ('username','dirtybit','account_name','provider','selected_account','limit','left')
	filter_horizontal = ()

admin.site.register(queue_statistics, queue_statistics_admin)

admin.site.register(temp_data)


class user_transaction_admin(admin.ModelAdmin):

	list_display = ('username','c_transaction_id','transaction_start','current_package','upgrade_package','from_date','to_date','razorpay_payment_url','razorpay_id','inv_id','status')
	filter_horizontal = ()

admin.site.register(user_transaction, user_transaction_admin)



class notification_pannel_admin(admin.ModelAdmin):

	list_display = ('username','timestamp','read_hit','mark_as_read_hit','read_hit_time','message','follow_link','u_code')
	filter_horizontal = ()

admin.site.register(notification_pannel, notification_pannel_admin)


'''   
 
 class notification_pannel_admin(admin.ModelAdmin):

	list_display = ('username','timestamp','read_hit','mark_as_read_hit','read_hit_time','message','follow_link','u_code')
	filter_horizontal = ()

admin.site.register(notification_pannel, notification_pannel_admin)


 username = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=datetime.now)
    read_hit = models.BooleanField(default=False)
    mark_as_read_hit = models.BooleanField(default=False)
    read_hit_time = models.DateTimeField(blank=True,null=True)
    message = models.CharField(max_length=256,blank=False,null=False)
    follow_link = models.URLField(blank=True,null=True)
    u_code = models.IntegerField(blank=True,null=True)
'''