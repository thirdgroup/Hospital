from django.contrib import admin
from database.models import Admission, Registration, DoctorManage, Department, RegisterItems, PayItems
# Register your models here.

admin.site.register(Department)
admin.site.register(DoctorManage)
admin.site.register(Registration)
admin.site.register(Admission)
admin.site.register(PayItems)
admin.site.register(RegisterItems)

