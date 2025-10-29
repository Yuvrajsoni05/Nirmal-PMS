from ast import mod
from pyexpat import model
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.core.validators import validate_email
# from simple_history.models import HistoricalRecords


# Create your models here.  
class Registration(AbstractUser):
    
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True
    )

    first_name = models.CharField(max_length=200, blank=True,null=True,)
    last_name = models.CharField(max_length=200,blank=True, null=True)
    email = models.EmailField(max_length=200, unique=True,validators=[validate_email])

class Job_detail(models.Model):
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
        job_status = models.CharField(max_length=200,blank=True, null=True)
        created_at = models.DateTimeField(auto_now_add=True,blank=True, null=True)
        # history = HistoricalRecords()

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
    # thumbnail_image = models.FileField(upload_to='cdr_thumbnail_image/',blank=True, null=True)
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
    
    
class ProformaInvoice(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, db_index=True)
    invoice_no = models.CharField(max_length=200, unique=True)
    invoice_date = models.DateField()
    mode_payment = models.CharField(max_length=300,default="100%")
    company_name = models.CharField(max_length=300)
    company_contact = models.CharField(max_length=200)
    company_email = models.EmailField(max_length=200)
    billing_address = models.TextField()
    billing_gstin_no = models.CharField(max_length=100)
    billing_state_name = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    job_name = models.CharField(max_length=200)
    quantity = models.DecimalField(max_digits=15, decimal_places=4,default=0.0000)
    pouch_open_size = models.CharField(max_length=200)
    cylinder_size = models.CharField(max_length=200)
    prpc_rate = models.DecimalField(max_digits=10, decimal_places=2,default=0.00)
    banking_details = models.TextField()
    gst = models.DecimalField(max_digits=5, decimal_places=4,default=0.00)
    total = models.CharField()
    terms_note = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Proforma Invoice: {self.invoice_no}"

        
