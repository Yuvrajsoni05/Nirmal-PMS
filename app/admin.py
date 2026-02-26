from django.contrib import admin
from .models import (
    Registration,
    Job_detail,
    Party,
    ProformaJob,
    CDRDetail,
    PouchParty,
    PouchPartyEmail,
    PouchPartyContact,
    CylinderMadeIn,
    PouchMaster,
    ProformaInvoice,
    BankDetails,
    PartyBillingAddress,
    PouchQuotation,
    JobHistory,
    PartyEmail,
    PartyContact,
    PartyBillingAddress,
    PouchPartyEmail,
    PouchPartyContact,
    CDRImage,

)


# Register your models here.



admin.site.register(CylinderMadeIn)
admin.site.register(ProformaInvoice)
admin.site.register(PouchMaster)

class JobDetailHistory(admin.ModelAdmin):
    list_display = ("id", "job" , "field_name" , "old_value" , "new_value" , "changed_at","chnage_user" )
admin.site.register(JobHistory,JobDetailHistory)

class AdminDetail(admin.ModelAdmin):
    list_display = ("first_name" ,"last_name" , "email","username")
admin.site.register(Registration,AdminDetail)



class AdminJobDetails(admin.ModelAdmin):
    list_display = ("id","date", "bill_no", "job_name" , "prpc_purchase" , "prpc_sell",)
admin.site.register(Job_detail,AdminJobDetails)


class AdminCDRDetail(admin.ModelAdmin):
    list_display = ["id" , 'job_name', 'party_details' , 'party_email_used' , 'party_contact_used']
admin.site.register(CDRDetail,AdminCDRDetail)

class PartyAdmin(admin.ModelAdmin):
    list_display = ["party_name" ]
admin.site.register(Party , PartyAdmin)

class PartyEmailAdmin(admin.ModelAdmin):
    list_display = ["id", "email" ,"party"]
admin.site.register(PartyEmail, PartyEmailAdmin)

class PartyContactAdmin(admin.ModelAdmin):
    list_display = ["id", "party_number" ,"party"]
admin.site.register(PartyContact , PartyContactAdmin)

class PartyBillingAdmin(admin.ModelAdmin):
    list_display = ["id", "billing_address" ,"party"]
admin.site.register(PartyBillingAddress , PartyBillingAdmin)


class BankDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_name' , 'bank_name' , 'bank_account_number']
admin.site.register(BankDetails,BankDetailsAdmin)

class ProformaJobAdmin(admin.ModelAdmin):
    list_display = ["id", "job_name"]
admin.site.register(ProformaJob , ProformaJobAdmin)


admin.site.register(CDRImage)

class PouchQuotationAdmin(admin.ModelAdmin):
    list_display = ["id" ,"delivery_date" ,"quantity_variate"]
admin.site.register(PouchQuotation,PouchQuotationAdmin)

class PouchPartyAdmin(admin.ModelAdmin):
    list_display = ["id" ,"party_name"]
admin.site.register(PouchParty,PouchPartyAdmin)