
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import validate_email
from django.forms import CharField
from rest_framework.fields import DateField
from decimal import Decimal, InvalidOperation
from django.core.exceptions import ValidationError

from num2words import num2words



# Create your models here.  
class Registration(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    first_name = models.CharField(max_length=200, blank=True,null=True,)
    last_name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True,validators=[validate_email])
    
    
    


class Party(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party_name = models.CharField(max_length=200, blank=True, null=True,db_index=True)

    def __str__(self):
        return f"{self.party_name}"


  
class PartyEmail(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_emails')
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"{self.party.party_name} - {self.email}"


class PartyContact(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_contacts')
    party_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.party.party_name} - {self.party_number}"

class PartyBillingAddress(models.Model):
    party = models.ForeignKey(Party, on_delete=models.CASCADE, related_name='party_billing_addresses')
    billing_address = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.party.party_name} - {self.billing_address}"
 


class Job_detail(models.Model):
    JOB_STATUS_CHOICES = [
        ("In Progress","In Progress"),
        ("Close Job","Close Job")
    ] 
    JOB_TYPE_CHOICES = [
        ("New Job" , "New Job"),
        ("Damage Repair","Damage Repair"),
        ("Job Work" , "Job Work")
    ]
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )
    date = models.DateField()
    bill_no = models.CharField(max_length=200 , db_index=True)
    
    job_name = models.CharField(max_length=200 ,db_index=True)
    job_type  = models.CharField(max_length=200,choices=JOB_TYPE_CHOICES)
    noc =  models.TextField(blank=True, null=True)
    prpc_purchase = models.CharField(max_length=200)
    prpc_sell = models.CharField(max_length=200,blank=True, null=True)
    cylinder_size = models.CharField(max_length=200)
    cylinder_made_in = models.CharField(max_length=200)
    pouch_size = models.CharField(max_length=200)
    pouch_open_size = models.CharField(max_length=200)
    pouch_combination = models.CharField(max_length=200,blank=True,null=True)
    correction = models.TextField(blank=True, null=True)

    cylinder_date = models.DateField(blank=True, null=True)
    cylinder_bill_no = models.CharField(blank=True, null=True)
    job_status = models.CharField(max_length=200,blank=True, null=True,choices=JOB_STATUS_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    party_details =  models.ForeignKey(Party,on_delete=models.SET_NULL,blank=True,null=True)


    
    @property
    def cdr_images_urls(self):
        cdr = CDRDetail.objects.filter(
            party_details=self.party_details,
            job_name__iexact=self.job_name
        ).first()
        if not cdr:
            return []
        images = cdr.cdr_images.all()
        return [img.image.url for img in images if img.image]
    
    
    def __str__(self):
        return f"{self.job_name}"



class JobHistory(models.Model):
    job = models.ForeignKey(Job_detail, on_delete=models.CASCADE, related_name="job_history")
    field_name = models.CharField(max_length=200)
    old_value = models.TextField(blank=True, null=True)
    new_value = models.TextField(blank=True, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)
    chnage_user = models.ForeignKey(Registration, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.job.job_name} - {self.field_name} changed"



class Jobimage(models.Model):
    job = models.ForeignKey(Job_detail,related_name='image', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='job_images/')
    upload_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    def __str__(self):
        return f"Image for Job ID: {self.job.id}"
    


    
class CDRDetail(models.Model):
    date = models.DateField()
    party_details =  models.ForeignKey(Party,on_delete=models.SET_NULL,blank=True,null=True,related_name='cdr_party_details')
    party_email_used = models.ForeignKey(PartyEmail,on_delete=models.SET_NULL,null=True, blank=True)
    party_contact_used = models.ForeignKey(PartyContact,on_delete=models.SET_NULL,null=True, blank=True)
    job_name =  models.CharField(max_length=200,blank=True, null=True,db_index=True)
    cdr_corrections = models.TextField(max_length=900,blank=True, null=True)
    
    
    def __str__(self):
        return f" {self.party_details} - {self.job_name}"
  
     
     
class CDRImage(models.Model):
    cdr =  models.ForeignKey(CDRDetail,on_delete=models.CASCADE, related_name='cdr_images')
    image = models.ImageField(upload_to='cdr_files/')

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.cdr}"
    
    
    


class CylinderMadeIn(models.Model):
    cylinder_made_in =  models.CharField(max_length=300,unique=True,blank=True, null=True)
    def __str__(self):
        return f"{self.cylinder_made_in}"


class BankDetails(models.Model):
    account_name = models.CharField(max_length=200, blank=True, null=True)
    bank_name = models.CharField(max_length=200)
    bank_brnach_address = models.TextField()
    bank_account_number = models.CharField(max_length=200)
    bank_ifsc_code  =  models.CharField(max_length=200)
    
    def __str__(self):
        return f"{self.bank_name}"




    
    
    
class ProformaInvoice(models.Model):
    
    Invoice_Status = [
        ("Pending","Pending"),
        ("Confirmed","Confirmed")
    ]
    
    INDIAN_STATES = [
        ("Andhra Pradesh", "Andhra Pradesh"),
        ("Arunachal Pradesh", "Arunachal Pradesh"),
        ("Assam", "Assam"),
        ("Bihar", "Bihar"),
        ("Chhattisgarh", "Chhattisgarh"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jharkhand", "Jharkhand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telangana", "Telangana"),
        ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("Uttarakhand", "Uttarakhand"),
        ("West Bengal", "West Bengal"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    invoice_no = models.CharField(max_length=200)
    invoice_date = models.DateField()
    mode_payment = models.CharField(max_length=300,default="100%")
    
    billing_gstin_no = models.CharField(max_length=100)
    billing_state_name = models.CharField(max_length=200, choices=INDIAN_STATES)
    bank_details = models.ForeignKey(BankDetails,on_delete=models.SET_NULL,blank=True,null=True,related_name='bank_details')
    gst = models.CharField(max_length=200,blank=True, null=True)
    total_taxable_value = models.CharField(max_length=200,blank=True, null=True)
    gst_value = models.CharField(max_length=200,blank=True, null=True)
    terms_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total = models.CharField(max_length=200,blank=True, null=True)
    invoice_status = models.CharField(max_length=200,choices=Invoice_Status,blank=True, null=True)
    party_details = models.ForeignKey(Party,on_delete=models.SET_NULL,blank=True,null=True,related_name='party_details')
    party_contact_used = models.ForeignKey(PartyContact,on_delete=models.SET_NULL,null=True, blank=True)
    party_email_used = models.ForeignKey(PartyEmail,on_delete=models.SET_NULL,null=True, blank=True)
    party_billing_address_used = models.ForeignKey(PartyBillingAddress,on_delete=models.SET_NULL,null=True, blank=True)
    
    
    def total_worlds(self):

        if not self.total:
            return ""
        total_str = str(self.total).replace(',', '').strip()
        int_part = total_str.split('.')[0]
        try:
            num = int(int_part)
        except (ValueError, TypeError):
            return ""
        try:
            return num2words(num, lang='en_IN').title()
        except OverflowError:
            return f"{num:,}"
    
    def __str__(self):
        return f"Proforma Invoice:  {self.invoice_no}" 





class ProformaJob(models.Model):
    proforma_invoice = models.ForeignKey(ProformaInvoice,on_delete=models.CASCADE,related_name="job_details")
    title = models.CharField(max_length=200)
    job_name = models.CharField(max_length=200)
    quantity = models.CharField(max_length=200)
    pouch_open_size = models.CharField(max_length=200)
    cylinder_size = models.CharField(max_length=200)
    prpc_rate = models.CharField(max_length=200)
    
    
    @property
    def taxable_value(self):
        try:
            return float(self.prpc_rate) * float(self.quantity)
        except TypeError:
            return None 
    
    
    def __str__(self):
        return f"{self.title} {self.taxable_value}"
    





# Pouch Party Details Models 
class PouchParty(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    party_name = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.party_name}"
    
class PouchPartyEmail(models.Model):
    party = models.ForeignKey(PouchParty, on_delete=models.CASCADE, related_name='pouch_party_emails')
    email = models.EmailField(max_length=200)
    def __str__(self):
        return f"{self.party} - {self.email}"


class PouchPartyContact(models.Model):
    party = models.ForeignKey(PouchParty, on_delete=models.CASCADE, related_name='pouch_party_contacts')
    party_number = models.CharField(max_length=20)
    def __str__(self):
        return f"{self.party} - {self.party_number}"


class PouchQuotation(models.Model):

    POUCH_STATUS = [
        ('Pending' , 'Pending'),
        ('Approved' , 'Approved'),
        ('Rejected' , 'Rejected'),
        ('Cancelled' , 'Cancelled'),
        ('Delivered' , 'Delivered'),
      
    ]

    pouch_quotation_number = models.CharField(max_length=200 ,default="234KG@$S" ,blank=True, null=True)
    delivery_date  = models.DateField()
    party_details = models.ForeignKey(
        PouchParty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="quotations_party_name"
    )
    party_email = models.ForeignKey(PouchPartyEmail, on_delete=models.SET_NULL, null=True, blank=True,related_name='pouch_quotation_party_email')
    pouch_status = models.CharField(max_length=200,choices=POUCH_STATUS,blank=True, null=True)
    quantity_variate = models.CharField(max_length=200)
    freight = models.CharField(max_length=200)
    gst = models.CharField(max_length=200)
    note = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)

    
    def __str__(self):
        return f" - {self.party_details}"
    
    
class PouchQuotationJob(models.Model):
    POUCH_TYPE = [
        ('Center Seal Pouch' , 'Center Seal Pouch'),
        ('3 Side Seal Pouch' , '3 Side Seal Pouch'),
        ('6 Side Seal Pouch' , '6 Side Seal Pouch'),
        ('6 Side Seal Pouch With D Cut' ,'6 Side Seal Pouch With D Cut'),
        ('Stand Up Pouch With Zipper' , 'Stand Up Pouch With Zipper'),
        ('Perforation Pouch' , 'Perforation Pouch'),
        ('3 Side Seal Bag With Dori Handel' ,'3 Side Seal Bag With Dori Handel'),
        ('3 Side Seal Zipper With V Nouch' ,'3 Side Seal Zipper With V Nouch'),
        ('Printed Roll' , 'Printed Roll'),
        ('Flat Bottom Pouch With Zipper' ,'Flat Bottom Pouch With Zipper'),
    ]
    POLYESTER_UNIT =[
        ('polyester_printed_roll' , 'Polyester Printed Roll'),
        ('polyester_printed_bag' ,'Polyester Printed Bag')
    ]




    quotation = models.ForeignKey(PouchQuotation,on_delete=models.CASCADE,related_name="pouch_quotation_jobs")
    job_name = models.CharField(max_length=200)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    purchase_rate_per_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    no_of_pouch_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    pouch_open_size = models.CharField(max_length=200)
    delivery_address = models.TextField()
    minimum_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True
    )    
    final_rate = models.DecimalField(
        max_digits=12, decimal_places=2, default=0 , blank=True, null=True
    )
    per_pouch_rate_basic = models.DecimalField(
        max_digits=12, decimal_places=4, default=0 , blank=True, null=True
    )
    zipper_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    pouch_combination = models.CharField(max_length=200)
    pouch_type = models.CharField(max_length=200,choices=POUCH_TYPE)
    special_instruction = models.TextField()
    pouch_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    polyester_unit = models.CharField(max_length=200,choices=POLYESTER_UNIT,blank=True, null=True)
    

class PurchaseOrder(models.Model):

    POUCH_STATUS = [
        ('Pending' , 'Pending'),
        ('Approved' , 'Approved'),
        ('Rejected' , 'Rejected'),
        ('Cancelled' , 'Cancelled'),
        ('Delivered' , 'Delivered'),
      
    ]
    pouch_purchase_number = models.CharField(max_length=200 ,default="234KG@$S",blank=True, null=True)
    delivery_date  = models.DateField()
    party_email = models.ForeignKey(PouchPartyEmail, on_delete=models.SET_NULL, null=True, blank=True,related_name='pouch_purchase_party_email')
    party_details = models.ForeignKey(
        PouchParty,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="purchase_party_name"
    )
    
    quantity_variate = models.CharField(max_length=200)
    freight = models.CharField(max_length=200)
    gst = models.CharField(max_length=200)
    note = models.TextField(max_length=200)
    pouch_status = models.CharField(max_length=200,choices=POUCH_STATUS,blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    
    def __str__(self):
        return f"PO #{self.id} - {self.party_details}"


class PurchaseOrderJob(models.Model):
    POUCH_TYPE = [
        ('Center Seal Pouch' , 'Center Seal Pouch'),
        ('3 Side Seal Pouch' , '3 Side Seal Pouch'),
        ('6 Side Seal Pouch' , '6 Side Seal Pouch'),
        ('6 Side Seal Pouch With D Cut' ,'6 Side Seal Pouch With D Cut'),
        ('Stand Up Pouch With Zipper' , 'Stand Up Pouch With Zipper'),
        ('Perforation Pouch' , 'Perforation Pouch'),
        ('3 Side Seal Bag With Dori Handel' ,'3 Side Seal Bag With Dori Handel'),
        ('3 Side Seal Zipper With V Nouch' ,'3 Side Seal Zipper With V Nouch'),
        ('Printed Roll' , 'Printed Roll'),
        ('Flat Bottom Pouch With Zipper' ,'Flat Bottom Pouch With Zipper'),
    ]
    
    
    POLYESTER_UNIT =[
        ('polyester_printed_roll' , 'Polyester Printed Roll'),
        ('polyester_printed_bag' ,'Polyester Printed Bag')
    ]
    purchase_order = models.ForeignKey(PurchaseOrder,on_delete=models.CASCADE,related_name="purchase_order_jobs")
    job_name = models.CharField(max_length=200)
    quantity = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    purchase_rate_per_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    no_of_pouch_kg = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    pouch_open_size = models.CharField(max_length=200)
    polyester_unit = models.CharField(max_length=200,choices=POLYESTER_UNIT,blank=True, null=True)

    delivery_address = models.TextField()
    minimum_quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        blank=True,
        null=True
    ) 
    final_rate = models.DecimalField(
        max_digits=12, decimal_places=2, default=0 , blank=True, null=True
    )
    per_pouch_rate_basic = models.DecimalField(
        max_digits=12, decimal_places=4, default=0 , blank=True, null=True
    )
    zipper_cost = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )
    pouch_combination = models.CharField(max_length=200)
    pouch_type = models.CharField(max_length=200,choices=POUCH_TYPE,blank=True, null=True)
    special_instruction = models.TextField()
    pouch_charge = models.DecimalField(
        max_digits=10, decimal_places=2, default=0 , blank=True, null=True
    )