#  Copyright (c) 2022. Lorem ipsum dolor sit amet, consectetur adipiscing elit.
#  Morbi non lorem porttitor neque feugiat blandit. Ut vitae ipsum eget quam lacinia accumsan.
#  Etiam sed turpis ac ipsum condimentum fringilla. Maecenas magna.
#  Proin dapibus sapien vel ante. Aliquam erat volutpat. Pellentesque sagittis ligula eget metus.
#  Vestibulum commodo. Ut rhoncus gravida arcu.

from django.contrib import admin

from .models import Invoice1, LineItem1, Invoice2, LineItem2, Customers

admin.site.register(Invoice1)
admin.site.register(LineItem1)
admin.site.register(Customers)
admin.site.register(Invoice2)
admin.site.register(LineItem2)
# Register your models here.


admin.site.site_header = "APRO IT Solutions"
admin.site.site_title = "APRO Admin Portal"
admin.site.index_title = "Welcome to APRO IT Solutions"


