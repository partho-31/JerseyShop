from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import CustomUser,Contact,PaymentHistory


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('email','first_name','last_name','is_active','last_login')
    list_filter = ('is_active','is_staff')

    fieldsets = (
        (None,{'fields':('email','password')}),
        ('Personal Info',{'fields':(
            'first_name','last_name','address','phone_number','image',
            )}),
        ('Permissions',{'fields':('is_active','is_staff','is_superuser','groups','user_permissions')}),
        ('Important Dates',{'fields':('last_login','date_joined')})
    )

    add_fieldsets = (
        ('Create User', {
            'classes': ('wide',),
            'fields': ('email','password1','password2', 'is_active')
        }),
    )
    

    search_fields = ('first_name','email')
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Contact)
admin.site.register(PaymentHistory)
