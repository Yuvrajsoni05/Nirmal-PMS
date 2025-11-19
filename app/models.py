from ast import mod
from pyexpat import model
from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import validate_email
from django.forms import CharField



from num2words import num2words


# Create your models here.  
class Registration(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )
    first_name = models.CharField(max_length=200, blank=True,null=True,)
    last_name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True,validators=[validate_email])
    
    
    




# class JobHeader(models.Model):
#     Job_Status = [
#         ("Pending","Pending"),
#         ("Confirmed","Confirmed")
#     ]
#     job_date = models.DateField()
#     bill_no = models.CharField(max_length=200)
#     company_name = models.CharField(max_length=300, blank=True, null=True)
#     correction = models.TextField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
#     job_status  = models.CharField(max_length=200,choices=Job_Status)
    
#     def __str__(self):
#         return self.company_name
    


# class JobMaterial(models.Model):
#     job = models.ForeignKey(JobHeader, on_delete=models.CASCADE, related_name='job_materials')
#     job_name = models.CharField(max_length=200)
#     job_type = models.CharField(max_length=200)
#     noc = models.CharField(max_length=200)
#     prpc_purchase = models.CharField(max_length=200)
#     prpc_sell = models.CharField(max_length=200, blank=True, null=True)
#     cylinder_size = models.CharField(max_length=200)
#     cylinder_made_in = models.CharField(max_length=200)
#     pouch_size = models.CharField(max_length=200)
#     pouch_open_size = models.CharField(max_length=200)
#     pouch_combination = models.CharField(max_length=200)
#     cylinder_date = models.DateField(blank=True, null=True)
#     cylinder_bill_no = models.CharField(blank=True, null=True)
#     created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)

 


class Job_detail(models.Model):
    job_status = [
        ("In Progress","In Progress"),
        ("Close Job","Close Job")
    ]
    date = models.DateField()
    bill_no = models.CharField(max_length=200)
    company_name = models.CharField(max_length=300,blank=True, null=True)
    job_name = models.CharField(max_length=200)
    job_type  = models.CharField(max_length=200)
    noc =  models.TextField(blank=True, null=True)
    prpc_purchase = models.CharField(max_length=200)
    prpc_sell = models.CharField(max_length=200,blank=True, null=True)
    cylinder_size = models.CharField(max_length=200)
    cylinder_made_in = models.CharField(max_length=200)
    pouch_size = models.CharField(max_length=200)
    pouch_open_size = models.CharField(max_length=200)
    pouch_combination = models.CharField(max_length=200)
    correction = models.TextField(blank=True, null=True)
    folder_url = models.URLField()
    image_links = models.CharField(max_length=1000,blank=True, null=True)
    cylinder_date = models.DateField(blank=True, null=True)
    cylinder_bill_no = models.CharField(blank=True, null=True)
    job_status = models.CharField(max_length=200,blank=True, null=True,choices=job_status)
    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    

    def __str__(self):
        return self.company_name

    @property
    def cdr_file_url(self):
        cdr = CDRDetail.objects.filter(
            company_name__iexact=self.company_name,
            job_name__iexact=self.job_name
        ).first() 
        if cdr and cdr.file_url:
            return cdr.file_url
        return None
    @property
    def cdr_images_urls(self):
        
        cdr = CDRDetail.objects.filter(
            company_name__iexact=self.company_name,
            job_name__iexact=self.job_name
        ).first()
        if not cdr:
            return []
        images = cdr.cdr_images.all()
        return [img.image.url for img in images if img.image]



   
    
      
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
    company_name = models.CharField(max_length=200)
    job_name =  models.CharField(max_length=200,blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True,)
    # cdr_upload = models.FileField(upload_to='cdr_file/',blank=True, null=True)
    file_url = models.URLField(max_length=200,blank=True, null=True)
    image_url = models.URLField(max_length=900,blank=True, null=True)
    cdr_corrections = models.TextField(max_length=900,blank=True, null=True)
    
    
    def __str__(self):
        return f"{self.company_name} - {self.job_name}"
  
     
     
class CDRImage(models.Model):
    cdr =  models.ForeignKey(CDRDetail,on_delete=models.CASCADE, related_name='cdr_images')
    image = models.ImageField(upload_to='cdr_files/')

    created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
    
    def __str__(self):
        return f"{self.cdr}"
    
    
    
class CompanyName(models.Model):
    company_name = models.CharField(max_length=300)
    def __str__(self):
        return f"{self.company_name}"
   

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

    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    invoice_no = models.CharField(max_length=200)
    invoice_date = models.DateField()
    mode_payment = models.CharField(max_length=300,default="100%")
    company_name = models.CharField(max_length=300)
    company_contact = models.CharField(max_length=200)
    company_email = models.EmailField(max_length=200)
    billing_address = models.TextField()
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
    
    
    
    def total_worlds(self):
        total_world = self.total.split('.')
        total_in_words = num2words(total_world[0], lang='en_IN').title()
        return total_in_words
    
    
    def __str__(self):
        return f"Proforma Invoice: {self.invoice_no}"

    
        
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
    
    
    

class Company(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    company_name = models.CharField(max_length=200,blank=True,null=True)

  

class CompanyEmail(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='emails')
    email = models.EmailField(max_length=200)

    def __str__(self):
        return f"{self.company.name} - {self.email}"


class CompanyContact(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='contacts')
    contact_number = models.CharField(max_length=20)
