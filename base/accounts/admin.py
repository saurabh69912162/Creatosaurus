from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import business_profile_data, creator_profile_data
from .forms import UserCreationForm
from .models import MyUser

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
admin.site.unregister(Group)