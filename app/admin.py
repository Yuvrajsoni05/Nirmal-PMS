from django.contrib import admin
from .models import * 
from app.models import ProformaInvoice
# Register your models here.



admin.site.register(CylinderMadeIn)







admin.site.register(ProformaInvoice)

admin.site.register(BankDetails)

class JobDetailHistory(admin.ModelAdmin):
    list_display = ("id", "job" , "field_name" , "old_value" , "new_value" , "changed_at","chnage_user" )
admin.site.register(JobHistory,JobDetailHistory)

class AdminDetail(admin.ModelAdmin):
    list_display = ("first_name" ,"last_name" , "email","username")
admin.site.register(Registration,AdminDetail)



class AdminJobDetails(admin.ModelAdmin):
    list_display = ("id","date", "bill_no" , "company_name" , "job_name" , "prpc_purchase" , "prpc_sell" ,)
admin.site.register(Job_detail,AdminJobDetails)






class AdminCDRDetail(admin.ModelAdmin):
    list_display = ["id" , 'job_name', 'party_details' , 'party_email_used' , 'party_contact_used']
admin.site.register(CDRDetail,AdminCDRDetail)



class PartyEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "email" ,"party"]
admin.site.register(PartyEmail, PartyEmailAdmin) 
class PartyContactAdmin(admin.ModelAdmin):
    list_display = ["id", "party_number" ,"party"]
admin.site.register(PartyContact , PartyContactAdmin)
class PartyAdmin(admin.ModelAdmin):
    list_display = ["id", "party_name" ]
admin.site.register(Party , PartyAdmin)


class ProformaJobAdmin(admin.ModelAdmin):
    list_display = ["id", "job_name"]
admin.site.register(ProformaJob , ProformaJobAdmin)





admin.site.register(CDRImage)
    
# class AdminCompanyName(admin.ModelAdmin):
#     list_display = ("company_name")
# admin.site.register(CompanyName,AdminCompanyName)