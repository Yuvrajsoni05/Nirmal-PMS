from django.contrib import admin
from .models import * 
# Register your models here.



admin.site.register(CylinderMadeIn)





class JobDetailHistory(admin.ModelAdmin):
    list_display = ("id", "job" , "field_name" , "old_value" , "new_value" , "changed_at","chnage_user" )
admin.site.register(JobHistory,JobDetailHistory)

class AdminDetail(admin.ModelAdmin):
    list_display = ("first_name" ,"last_name" , "email","username")
admin.site.register(Registration,AdminDetail)



class AdminJobDetails(admin.ModelAdmin):
    list_display = ("id","date", "bill_no" , "company_name" , "job_name" , "prpc_purchase" , "prpc_sell")
admin.site.register(Job_detail,AdminJobDetails)



class AdminCompanyDetail(admin.ModelAdmin):
    list_display  = ["id" ,"company_name"]
admin.site.register(CompanyName,AdminCompanyDetail)


class AdminCDRDetail(admin.ModelAdmin):
    list_display = ["id" , 'company_name']
admin.site.register(CDRDetail,AdminCDRDetail)




admin.site.register(CDRImage)
    
# class AdminCompanyName(admin.ModelAdmin):
#     list_display = ("company_name")
# admin.site.register(CompanyName,AdminCompanyName)