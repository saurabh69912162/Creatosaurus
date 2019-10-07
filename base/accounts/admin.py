from django.contrib import admin

from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import business_profile_data, creator_profile_data
from .forms import UserCreationForm
from .models import MyUser

# Register your models here.

class UserAdmin(BaseUserAdmin):
	add_form = UserCreationForm

	list_display = ('username','email','is_admin','first_name','last_name','category')
	list_filter = ('is_admin',)

	fieldsets = (
			(None, {'fields': ('username','email','first_name','last_name','category','password')}),
			('Permissions', {'fields': ('is_admin',)})
		)
	search_fields = ('username','email','first_name','last_name','category')
	ordering = ('username','email','last_name','first_name')

	filter_horizontal = ()


admin.site.register(MyUser, UserAdmin)
admin.site.register(business_profile_data)
admin.site.register(creator_profile_data)
admin.site.unregister(Group)