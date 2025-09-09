import random
from django.shortcuts import get_object_or_404, render,redirect
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_control, never_cache
from django.db.models.signals import pre_delete
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from app.templatetags.custom_tags import remove_white
from app.models import Job_detail

# from app.views import update_job
# from torch import t
from .models import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout 
import requests 
from django.contrib.auth import update_session_auth_hash
# from googleapiclient.http import MediaFileUpload
import json
from decimal import Decimal
from django.core.paginator import Paginator

from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.db.models import Q
from django.db.models import Sum
import tempfile
#  google
from django.core.mail import send_mail
from django.http import JsonResponse
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
import mimetypes
import io
import re
import pickle
from django.core.mail import EmailMessage


#Password

from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
import os
from django.conf import settings
# Create your views here.






class CustomPasswordResetView(PasswordResetView):
    template_name = "Password/password_reset_form.html"
    email_template_name = "Password/password_reset_email.html"
    success_url = reverse_lazy("password_reset_done")


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = "Password/password_reset_done.html"
    

class CustomPasswordResetConfirm(PasswordResetConfirmView):
    template_name = "Password/password_reset_confirm.html"
    success_url = reverse_lazy("password_reset_complete")


def password_reset_done(request):
    return render(request,'Password/password_update_done.html')

    
    
    
# SERVICE_ACCOUNT_FILE = os.path.join(settings.BASE_DIR, 'app', 'Google', 'credentials.json')
# SCOPES = ['https://www.googleapis.com/auth/drive']
def login_page(request):    
    if request.method == 'POST':
        username_email = request.POST.get('username')
        password = request.POST.get('password')
        print(username_email)
        print(password)
        
        valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',username_email)
        
        if valid:
            user_login = Registration.objects.get(email = username_email.lower()).username
            user = authenticate(request, username=user_login, password=password)
            
        else:
            user = authenticate(request,username=username_email,password=password)
            
        if user is not None:
            login(request, user)
            messages.success(request,'You are Login')
            return redirect('dashboard_page') 
        else:
            messages.error(request,"Invalid Username and Password ",)
            return redirect('login_page')
    return render(request, 'Registration/login_page.html')  


# def usernmae_validator(username):
#     if len(username) < 3 or len(username) > 12:
#         return "Username must be between 3 and 12 character"




def email_validator(email):
    email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex,email):       
        return "Enter a Valid email Address"

 

def validator_password(password):
    if len(password) < 8:
        return "Password Must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase "
    if not any(char.islower() for char in password):
         return "Password must contain at least one lowercase"
     
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number"
    
    if not any(char in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for char in password):
        return "Password must contain at least one special character."
    
    
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def register_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')

        email = request.POST.get('emailAddress')
        password = request.POST.get('password')
        confirma_password = request.POST.get('confirma_password')

        required_filed = {
           
            'First Name':first_name,
            'Last Name':last_name, 
            'Username':username,
            'Password':password,
        }
    
        for i , required in required_filed.items():
            if not required:
                messages.error(request,f" {i} field is Required",extra_tags="custom-success-style")
                return redirect('register_page')
        
        # email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        # if not re.match(email_regex, email):
        #     messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
        #     return redirect('register_page')
       
        if Registration.objects.filter(username=username).exists():
                messages.error(request,'Username Alredy Exist',extra_tags="custom-success-style")
                return redirect('register_page')
            
        if Registration.objects.filter(email=email).exists():
            messages.error(request,"Email is Alredy Exist",extra_tags="custom-success-style")
            return redirect('register_page')
        
        email_error  = email_validator(email)
        if email_error:
            messages.error(request,email_error,extra_tags="custom-success-style")
            return redirect('register-page')
        
        password_error = validator_password(password)
        if password_error:
            messages.error(request,password_error,extra_tags="custom-success-style")
            if password != confirma_password:
                messages.error(request,'Password Confirm Password must be same',extra_tags="custom-success-style")
                return redirect('register_page')

        create_user = Registration.objects.create_user(
            first_name = first_name,
            last_name = last_name,
            username = username,
            password = password,
            email= email,
        )
        create_user.save()
        messages.success(request,"New User Will Created",)
        
        return redirect('edit_user_page')
    return render(request,'Registration/register.html')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def edit_user_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    user_info = Registration.objects.exclude(is_superuser=True).exclude(id=request.user.id).order_by('username')
    context = {
        'users':user_info
    }
    return render(request,'Registration/edit_user.html',context)

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def delete_user(request,user_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        
        Delete_user = get_object_or_404(Registration,id = user_id)
        Delete_user.delete()
       
        messages.success(request,"User Deleted")
        return redirect('edit_user_page')
    
    
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)    
def update_user(request, user_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    
    try:
        if request.method == 'POST':
            update_user = get_object_or_404(Registration, id=user_id)
            username = request.POST.get('username')
            email = request.POST.get('email')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            
            # email_error = email_validator(email)
            # if email_error:
            #     messages.error(request,email_error,extra_tags="custom-success-style")
            #     return redirect('edit_user_page')
            
        
            print(user_id)
            required_fields = {
                'Username': username,
                'Firstname': first_name,
                'Lastname': last_name,
                'Email': email,
            }

            for field_name, value in required_fields.items():
                if not value:
                    messages.error(request, f"{field_name} is required.",extra_tags="custom-success-style")
                    return redirect('edit_user_page')
                
                
            email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
            if not re.match(email_regex, email):
                messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
                return redirect('edit_user_page')
                
                
            if username != update_user.username and Registration.objects.filter(username=username).exists():
                messages.error(request, "Username already exists.", extra_tags="custom-success-style")
                return redirect('edit_user_page')


            if email != update_user.email and Registration.objects.filter(email=email).exists():
                messages.error(request, "Email already exists.", extra_tags="custom-success-style")
                return redirect('edit_user_page')

        
                
            required_fields = {
                'Username': username,
                'Firstname': first_name,
                'Lastname': last_name,
                'Email': email,
            }

            for field_name, value in required_fields.items():
                if not value:
                    messages.error(request, f"{field_name} is required.",extra_tags="custom-success-style")
                    return redirect('edit_user_page')

            if username != update_user.username:
                update_user.username = username
            if email != update_user.email:
                update_user.email = email
        
            update_user.first_name = first_name
            update_user.last_name = last_name

            logout_user = Registration.objects.get(id=user_id)
            for session in Session.objects.all():
                session_data = session.get_decoded()
                print(session_data)
                if str(session_data.get('_auth_user_id')) == str(logout_user.id):
                    session.delete()
            update_user.save()
            messages.success(request, "User updated successfully.")
            return redirect('edit_user_page')
    except Exception as e:
        messages.error(request,f"Something went wrong {e}",extra_tags="custom-success-style")
        return redirect('edit_user_page')
        
        
        
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def dashboard_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:

        get_q = request.GET.get('q','')
        date_s = request.GET.get('date','')
        date_e = request.GET.get('end_date','')
        sorting = request.GET.get('sorting', '')
        date_sorting = request.GET.get('date_sorting','')
        company_name_sorting = request.GET.get('company_name_sorting' ,'')
        job_name_sorting = request.GET.get('job_name_sorting','')
        cylinder_date_sorting = request.GET.get('cylinder_date_sorting','')
        cylinder_made_in_sorting = request.GET.get('cylinder_made_in_sorting','')
        

        db_sqlite3  = Job_detail.objects.all()

        total_purchse_floats = [] 
        total_purchse = Job_detail.objects.values_list('prpc_purchase') 
        for i in total_purchse:
            data_string = i[0]  
            cleaned_string = data_string.replace(",", "")
            float_value = float(cleaned_string)
            total_purchse_floats.append(float_value)
        total_purchase = sum(total_purchse_floats)

        total_sell_floats = []
        total_sell = Job_detail.objects.values_list('prpc_sell')
        for  i in total_sell:
            sell_data = i[0]
            cleaned_data = sell_data.replace(",","")
            sell_float = float(cleaned_data)
            total_sell_floats.append(sell_float)
        
        total_sales =  sum(total_sell_floats)
      
        filters = Q()
        if get_q:
            
            filters &= (
                Q(job_name__icontains=get_q) |
                Q(company_name__icontains=get_q) |
                Q(cylinder_made_in__icontains=get_q)
            )
        if date_s and date_e:
            filters &= Q(date__range=[date_s, date_e])
        elif date_s:
            filters &= Q(date__icontains=date_s)
        elif date_e:
            filters &= Q(date__icontains=date_e)

        db_sqlite3 = Job_detail.objects.filter(filters)
        
        job_status = Job_detail.objects.values('job_status').distinct()
        
        
        columns = {
            'job_name_sorting':job_name_sorting,
            'date_sorting':date_sorting,
            'cylinder_date_sorting':cylinder_date_sorting,
            'company_name_sorting':company_name_sorting,
            'cylinder_made_in_sorting':cylinder_made_in_sorting,
            'sorting':sorting
            
        }

        
        if job_name_sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('job_name')
        elif job_name_sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-job_name')
        elif date_sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('date')
        elif date_sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-date')
        elif cylinder_date_sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('cylinder_date')
        elif cylinder_date_sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-cylinder_date')
        elif company_name_sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('company_name')
        elif company_name_sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-company_name')
        elif cylinder_made_in_sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('cylinder_made_in')
        elif cylinder_made_in_sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-cylinder_made_in')
        elif sorting == 'asc':
            db_sqlite3 = db_sqlite3.order_by('id')
        elif sorting == 'desc':
            db_sqlite3 = db_sqlite3.order_by('-id')
        else:
            db_sqlite3 = db_sqlite3.order_by('-job_status', 'date')
        p = Paginator(db_sqlite3, 10)
        page = request.GET.get('page')
        datas = p.get_page(page)
        total_job = db_sqlite3.count()
        company_name = CompanyName.objects.all()
        count_of_company =  company_name.count()
       
        cylinder_company_names = CylinderMadeIn.objects.all()
        totla_active_job = Job_detail.objects.filter(job_status='In Progress').count()
        count_of_cylinder_compnay = cylinder_company_names.count() 
        nums = " " * datas.paginator.num_pages  
      
        context = {
            'nums': nums,
            'venues': datas,
            'total_job': total_job,
            'company_name': company_name,
            'cylinder_company_names': cylinder_company_names,
            'count_of_company':count_of_company,
            'count_of_cylinder_compnay':count_of_cylinder_compnay,
            'total_sales':total_sales,
            'datas':datas,                                                                                                              
            'total_purchase':total_purchase,
            'sorting': sorting,
            'company_name_sorting':company_name_sorting,
            'job_name_sorting':job_name_sorting,
            'date_sorting':date_sorting,
            'cylinder_date_sorting':cylinder_date_sorting,
            'cylinder_made_in_sorting':cylinder_made_in_sorting,
            'totla_active_job':totla_active_job,
            'job_status':job_status,
        }
    except Exception as e:
        print(f"Error: {e}")
        return redirect('dashboard_page')

    return render(request, 'dashboard.html', context)


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)   
def delete_data(request,delete_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        
        folder_url = Job_detail.objects.values('folder_url').all().get(id=delete_id)
        if folder_url == '':
            url = os.environ.get('DELETE_WEBHOOK_JOB')
           
            response = requests.delete(f"{url}{delete_id}")
            data = response.json()
            messages.success(request,"Job Deleted successfully ")
            return redirect('dashboard_page')
        else:
            delete_data = get_object_or_404(Job_detail,id=delete_id)
            delete_images = delete_data.image.all()
            print(delete_images)
            for img in delete_images:
                path = img.image.path
                print(path)
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    img.delete()
            
            delete_data.delete()
            messages.success(request,"Job Deleted successfully ")
            return redirect('dashboard_page')
    
    except Exception as e:
        print(e)
        messages.warning(request,"Something went Wrong")
        return redirect('dashboard_page')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)  
def base_html(request):
    return render(request,'Base/base.html')


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def data_entry(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    # cdr_company_name = CDRDetail.objects.values('company_name').distinct()
    
    comapny_name = CompanyName.objects.values('company_name').union(CDRDetail.objects.values('company_name'))
    print(comapny_name)
    cylinder_company_names = CylinderMadeIn.objects.all()
    cdr_job_name = CDRDetail.objects.values('job_name').distinct()
    context =  {
        'comapany_name':comapny_name ,
        'cylinder_company_names':cylinder_company_names,
        'cdr_job_name':cdr_job_name
    }
    return render(request, 'data_entry.html',context)


# def get_drive_services():
#     creds = service_account.Credentials.from_service_account_file(
#         SERVICE_ACCOUNT_FILE, scopes=SCOPES
#     )
#     return build('drive', 'v3', credentials=creds)


# def get_job_name_folder(service,job_name,parent_job_id):
#     query = (
#     f"name='{job_name}' and mimeType='application/vnd.google-apps.folder'and trashed=false and '{parent_job_id}' in parents"
# )
    
#     result = service.files().list(
#         q=query,
#         spaces = 'drive',
#         fields = 'files(id,name)'
#     ).execute()
    
#     folders = result.get('files',[])
    
# rows = 5  
    # for i in range(1, rows + 1):
    #     for j in range(rows - i):
    #         print(" ", end=" ")
    #     for k in range(2 * i - 1):
    #         print("*", end="")
    #     print()
    
    
#     if folders:
#         job_id  = folders[0]['id']
#         job_url = f"https://drive.google.com/drive/folders/{job_id}"
#         return job_id , job_url
#     else:
#         folder_metadata = {
#             'name':job_name,
#             'parents': [parent_job_id],
#             'mimeType':'application/vnd.google-apps.folder'
            
#         }
#         job_folder = service.files().create(
#             body = folder_metadata,
#             fields = 'id',
#             supportsAllDrives=True
#         ).execute()
        
        
#         job_id = job_folder.get('id')
#         job_url = f"https://drive.google.com/drive/folders/{job_id}"
#         return job_id,job_url
        

# def get_create_folder(service, folder_name, parent_folder_id,):
#     query = (
#         f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder' "
#         f"and trashed=false and '{parent_folder_id}' in parents"
#     )
#     result = service.files().list(
#         q=query,
#         spaces='drive',
#         fields='files(id, name)'
#     ).execute()

#     folders = result.get('files', [])
    
#     if folders:
#         folder_id = folders[0]['id']
#         folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
        
#         return folder_id, folder_url

#     else:
#         # Create new folder
#         folder_metadata = {
#             'name': folder_name,
#             'parents': [parent_folder_id],
#             'mimeType': 'application/vnd.google-apps.folder'
#         }
        
#         folder = service.files().create(
#             body=folder_metadata,
#             fields='id',
#             supportsAllDrives=True
#         ).execute()
        
#         folder_id = folder.get('id')
#         folder_url = f"https://drive.google.com/drive/folders/{folder_id}"
#         return folder_id, folder_url



          


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0)
@login_required(redirect_field_name=None)
def add_job(request):

    try:
        if request.method == 'POST':
            date = request.POST.get('job_date')
            bill_no = request.POST.get('bill_no')
            company_name = request.POST.get('company_name','').strip()
            job_name = request.POST.get('job_name')
            new_job_name = request.POST.get('new_job_name','').strip()
            job_type = request.POST.get('job_type')
            noc = request.POST.get('noc')
            prpc_purchase = request.POST.get('prpc_purchase')
            prpc_sell = request.POST.get('prpc_sell')
            cylinder_size = request.POST.get('cylinder_size')
            cylinder_made_in_s = request.POST.get('cylinder_select')
            cylinder_date = request.POST.get('cylinder_date')
            cylinder_bill_no = request.POST.get('cylinder_bill_no')
            pouch_size = request.POST.get('pouch_size')
            pouch_open_size = request.POST.get('pouch_open_size')
            pouch_combination_1 = request.POST.get('pouch_combination1')
            pouch_combination_2 = request.POST.get('pouch_combination2')
            pouch_combination_3 = request.POST.get('pouch_combination3')
            pouch_combination_4 = request.POST.get('pouch_combination4')
            new_company = request.POST.get('new_company')
            new_cylinder_company_name = request.POST.get('cylinder_made_in_company_name')
            correction = request.POST.get('correction')
            job_status = request.POST.get('job_status')
            files = request.FILES.getlist('files') 
            pouch_combination_total  = f"{pouch_combination_1} + {pouch_combination_2} + {pouch_combination_3} + {pouch_combination_4}"
            
            
                         
            required_filed = {
                    'Date' :date,
                    'Bill no':bill_no,
                    'Company_Name': company_name,
                    'job name' : job_name,
                    'job type':job_type,
                    'Noc':noc,
                    'Prpc Purchase':prpc_purchase,
                    'Cylinder Size':cylinder_size,
                    'Cylinder Made in':cylinder_made_in_s,
                    'Pouch size':pouch_size,
                    'Pouch Open Size':pouch_open_size,
                    'Cylinder Bill No':cylinder_bill_no,
                    'Cylinder Date':cylinder_date
                    
                    
            }
            for i ,r in required_filed.items():
                if not  r:
                    messages.error(request,f"This {r} Filed Was Required",extra_tags="custom-success-style")
                    return redirect('data_entry')
            

            
            valid_extension = [".jpeg", ".jpg", ".png" ,".ai"]
            for file in files:
                ext = os.path.splitext(file.name)[1]
                if ext.lower() not in valid_extension:
                    messages.error(request,"Invalid file  Only .jpg, .jpeg, .png and .ai are allowed." ,extra_tags="custom-success-style")
                    return redirect("data_entry")
                
                
            file_dic = {}
            for i, file in enumerate(files):
                # Get the original file extension
                _, file_extension = os.path.splitext(file.name)
                random_number = random.randint(1, 100)
                new_file_name = f'{date}_{random_number}{file_extension}'
                file.name = new_file_name
                file_key = f"{new_file_name}"
                file_dic[file_key] = (file.name, file, file.content_type)
            
            
            if len(files) > 2:
                messages.error(request, "You can upload only 2 files", extra_tags="custom-error-style")
                return redirect('data_entry')

           
            pouch_combination = pouch_combination_total
            
            if new_job_name != '':
                if new_job_name == '' or new_job_name == None:
                    messages.error(request,'Plz Provide Job Name')
                    return redirect('data-entry')
                if Job_detail.objects.filter(job_name__icontains=new_job_name).exists():
                    messages.error(request,"Job Name Alredy Exists",extra_tags='custom-success-style')
                    return redirect('data_entry')
                else:
                    job_name = new_job_name

            if Job_detail.objects.filter(job_name__icontains = job_name,date__icontains  =date).exists():
                    messages.error(request,"Job Name are alredy Exsits on this date  kidnly Update job",extra_tags='custom-success-style')
                    return redirect('data_entry')
        
            if new_company != '':
       
                if CompanyName.objects.filter(company_name__icontains=new_company).exists():
                    messages.error(request,"Company Name Alredy Exists",extra_tags='custom-success-style')
                    return redirect('data_entry')
                add_company = CompanyName.objects.create(
                    company_name=new_company
                )
                add_company.save()
                company_name = new_company
            if company_name == '' or company_name == None:
                messages.error(request,'Plz Provide Company Name')
                return redirect('data-entry')

            if new_cylinder_company_name != '':
                if CylinderMadeIn.objects.filter(cylinder_made_in__icontains = new_cylinder_company_name).exists():
                    messages.error(request,"Company Name Alredy Exists",extra_tags='custom-success-style')
                    return redirect('data_entry')
                add_new_cylinder_company = CylinderMadeIn.objects.create(
                    cylinder_made_in = new_cylinder_company_name
                )
                add_new_cylinder_company.save()
                cylinder_made_in_s = new_cylinder_company_name
                
             
            data  =  {
                'date':date,
                'bill_no':bill_no,
                'company_name':company_name,
                'job_type':job_type,
                'job_name':job_name,
                'noc':noc,
                'prpc_sell':prpc_sell,
                'prpc_purchase':prpc_purchase,
                'cylinder_size':cylinder_size,
                'cylinder_made_in':cylinder_made_in_s,
                'pouch_size':pouch_size,
                'pouch_open_size':pouch_open_size,
                'pouch_combination':pouch_combination,
                'correction':correction
            }

        try:
            url = os.environ.get('CREATE_WEBHOOK_JOB')
            print(url)
            print(url)
            response = requests.post(f'{url}',data=data,files=file_dic)
            print(response.status_code)
     
            
            if response.status_code == 200:
                data_string  = response.text
                data_dict = json.loads(data_string)
                id_number = data_dict['id']
                cylinder_data = Job_detail.objects.all().get(id=id_number)
                cylinder_data.cylinder_date = cylinder_date
                cylinder_data.cylinder_bill_no = cylinder_bill_no
                cylinder_data.job_status = job_status
                cylinder_data.save()
                messages.success(request,"Job successfully Added")
                return redirect('dashboard_page')
            else:
                job_data = Job_detail.objects.create(
                date = date,
                bill_no = bill_no,
                company_name = company_name,
                job_name = job_name,
                job_type = job_type,
                noc = noc,
                prpc_sell =prpc_sell,
                prpc_purchase = prpc_purchase ,
                cylinder_size = cylinder_size,
                cylinder_made_in = cylinder_made_in_s,
                pouch_size = pouch_size,
                pouch_open_size = pouch_open_size,
                pouch_combination = pouch_combination,
                correction = correction,
                job_status = job_status,
                cylinder_date = cylinder_date,
                cylinder_bill_no = cylinder_bill_no,
            )
            for file in file_dic:
                Jobimage.objects.create(
                    job = job_data,
                    image = file
                )
            job_data.save()
            messages.success(request,"Data  successfully Add on dbsqlite 3")
            return redirect('dashboard_page')
        except Exception :
            job_data = Job_detail.objects.create(
                date = date,
                bill_no = bill_no,
                company_name = company_name,
                job_name = job_name,
                job_type = job_type,
                noc = noc,
                prpc_sell =prpc_sell,
                prpc_purchase = prpc_purchase ,
                cylinder_size = cylinder_size,
                cylinder_made_in = cylinder_made_in_s,
                pouch_size = pouch_size,
                pouch_open_size = pouch_open_size,
                pouch_combination = pouch_combination,
                correction = correction,
                job_status = job_status,
                cylinder_date = cylinder_date,
                cylinder_bill_no = cylinder_bill_no,
            )
            for file_key, file_data in file_dic.items():
                file_obj = file_data[1]  
                Jobimage.objects.create(
                    job=job_data,
                    image=file_obj
                )
            job_data.save()
            messages.success(request,"Data  successfully Add ")
            return redirect('dashboard_page')
    
    except Exception as e:
        messages.error(request,f"Something went wrong {e}")
        print(e)
        return redirect('data_entry')
            # print(cylinder_made_in_s)
        
            # from django.shortcuts import render, redirect
            # from .models import Company
            # from django.core.exceptions import ValidationError
            # import re

            # def normalize_company_name(name):
            #     return re.sub(r'\s+', ' ', name.strip()).lower()

            # def add_company(request):
            #     error = None
            #     if request.method == 'POST':
            #         name = request.POST.get('name', '')
            #         normalized_name = normalize_company_name(name)

            #         # Check for existing company with same normalized name
            #         existing_companies = Company.objects.all()
            #         for company in existing_companies:
            #             if normalize_company_name(company.name) == normalized_name:
            #                 error = "Company name already exists."
            #                 break

            #         if not error:
            #             Company.objects.create(name=name)
            #             return redirect('success_page')  # replace with your redirect

            #     return render(request, 'add_company.html', {'error': error})

            
            # service = get_drive_services()
            # n8n_folder_id = '14AUzR7EWGbCGoQ-MnIoSabVALt_qUeRS' 

            # folder_id, folder_url = get_create_folder(service, company_name, n8n_folder_id,)
            
            # if folder_id:
            #     print("Folder found/created:", folder_id)
            #     print("Folder URL:", folder_url)
            # else:
            #     print("Error with folder operation")
                
            # job_id , job_url = get_job_name_folder(service,job_name,folder_id)
            
            # if job_id:
            #     print("Job Folder found/created:", job_id)
            #     print("Job Folder URL:", job_url)
            # else:
            #     print("Error with folder operation")
            
            
            # uploaded_file_ids = []
            # for file in files:
            #     temp_file = tempfile.NamedTemporaryFile(delete=False)  # Safe temp file creation
            #     with open(temp_file.name, 'wb+') as destination:
            #         for chunk in file.chunks():
            #             destination.write(chunk)

            #     file_metadata = {
            #         'name': file.name,
            #         'parents': [job_id]  # Correct key is 'parents' not 'parent'
            #     }
            #     media = MediaFileUpload(temp_file.name, mimetype=file.content_type)
            #     uploaded_file = service.files().create(
            #         body=file_metadata,
            #         media_body=media,
            #         fields='id',
            #         supportsAllDrives=True
            #     ).execute()
            
            
            #             data_string = "1 + 1 + 1 + 1"

            # # Split the string by " + " to get a list of number strings
            # numbers_as_strings = data_string.split(" + ")

            # # Convert each string to an integer and assign to separate variables
            # # This assumes you know the exact number of elements beforehand
            # if len(numbers_as_strings) >= 1:
            #     var1 = int(numbers_as_strings[0])
            # if len(numbers_as_strings) >= 2:
            #     var2 = int(numbers_as_strings[1])
            # if len(numbers_as_strings) >= 3:
            #     var3 = int(numbers_as_strings[2])
            # if len(numbers_as_strings) >= 4:
            #     var4 = int(numbers_as_strings[3])

            # # You can also store them in a list if the number of elements varies
            # all_numbers = [int(num) for num in numbers_as_strings]

            # # Print the results to verify
            # print(f"var1: {var1}")
            # print(f"var2: {var2}")
            # print(f"var3: {var3}")
            # print(f"var4: {var4}")
            # print(f"All numbers in a list: {all_numbers}")

            #     uploaded_file_ids.append(uploaded_file.get('id'))
            #     os.remove(temp_file.name) 
            # Gauth=GoogleAuth()


@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)    
def  update_job(request,update_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        if request.method == 'POST':
            date =  request.POST.get('date')
            bill_no = request.POST.get('bill_no')
            company_name = request.POST.get('company_name')
            job_name = request.POST.get('job_name','')
            job_type = request.POST.get('job_type','')
            noc = request.POST.get('noc')
            prpc_purchase = request.POST.get('prpc_purchase')
            prpc_sell = request.POST.get('prpc_sell')
            cylinder_size = request.POST.get('cylinder_size')
            cylinder_made_in = request.POST.get('cylinder_made_in')
            cylinder_date  = request.POST.get('cylinder_date')
            cylinder_bill_no = request.POST.get('cylinder_bill_no')
            pouch_size = request.POST.get('pouch_size')
            pouch_open_size = request.POST.get('pouch_open_size')
            # pouch_combination = request.POST.get('pouch_combination')
            pouch_combination1 = request.POST.get('pouch_combination1')
            pouch_combination2 = request.POST.get('pouch_combination2')
            pouch_combination3 = request.POST.get('pouch_combination3') 
            pouch_combination4 = request.POST.get('pouch_combination4')
            correction = request.POST.get('correction')
            job_status = request.POST.get('job_status')
            files = request.FILES.getlist('files')
            pouch_combination = f"{pouch_combination1} + {pouch_combination2} + {pouch_combination3} + {pouch_combination4}"
  
        demo = Job_detail.objects.values('date').get(id=update_id)
        date_formatte = demo['date'].strftime("%Y-%m-%d")
        
        
        required_filed = {
            'Date' :date,
            'Bill no':bill_no,
            'Company_Name': company_name,
            'job name' : job_name,
            'job type':job_type,
            'Noc':noc,
            'Prpc Purchase':prpc_purchase,
            'Cylinder Size':cylinder_size,
            'Cylinder Made in':cylinder_made_in,
            'Pouch size':pouch_size,
            'Pouch Open Size':pouch_open_size,
            'Cylinder Bill No':cylinder_bill_no,
            'Cylinder Date':cylinder_date,
            
            
        }
        for i ,r in required_filed.items():
            if not  r:
                messages.error(request,f"This {i} Filed Was Required",extra_tags="custom-success-style")
                return redirect('dashboard_page')
            
    
        jobs = Job_detail.objects.all().get(id=update_id)  
        if job_name != jobs.job_name:
            messages.error(request,"You can't chnage job_name")
            return redirect('dashboard_page')
      
        
        
        if date != date_formatte:
            if Job_detail.objects.filter(date = date, job_name = job_name).exists() :
                messages.error(request,"Job is Alredy exists from this date ",extra_tags="custom-success-style")
                return redirect('dashboard_page')

        if len(files) > 2:
            messages.error(request, "You can upload only 2 files", extra_tags="custom-error-style")
            return redirect('data_entry')

        valid_extension = [".jpeg", ".jpg", ".png" ,".ai"]  

        for file in files:
            ext = os.path.splitext(file.name)[1]
            if ext.lower() not in valid_extension:
                messages.error(request,"Invalid file  Only .jpg, .jpeg, .png and .ai are allowed." ,extra_tags="custom-success-style")
                return redirect("dashboard_page")

        get_data =  Job_detail.objects.all().get(id=update_id)
        get_combinations = get_data.pouch_combination.replace(" ","").split("+")
        while len(get_combinations) < 4:
            get_combinations.append('')
        print(get_combinations)
        folder_id = get_data.folder_url
        
        
        file_dic = {}
        for i, file in enumerate(files):
            _, file_extension = os.path.splitext(file.name)
            random_number = random.randint(1, 100)
            new_file_name = f'{date}_{random_number}{file_extension}'
            file.name = new_file_name
            file_key = f"{new_file_name}"
            file_dic[file_key] = (file.name, file, file.content_type)
        
        url = os.environ.get('UPDATE_WEBHOOK_JOB')
        if folder_id :
            data  =  {
            'date':date,
            'bill_no':bill_no,
            'company_name':company_name,
            'job_type':job_type,
            'job_name':job_name,
            'noc':noc,
            'prpc_purchase':prpc_purchase,
            'prpc_sell':prpc_sell,
            'cylinder_size':cylinder_size,
            'cylinder_made_in':cylinder_made_in,
            'pouch_size':pouch_size,
            'pouch_open_size':pouch_open_size,
            'pouch_combination':pouch_combination,
            'correction':correction
            }
            try:
                response = requests.post(f'{url}{update_id}',
                        data=data,files=file_dic  
                )
                if response.status_code == 200:
                    cylinder_data = Job_detail.objects.all().get(id=update_id)
                    cylinder_data.cylinder_date = cylinder_date
                    cylinder_data.cylinder_bill_no = cylinder_bill_no
                    cylinder_data.job_status = job_status
                    cylinder_data.save()
                    messages.success(request,'Data Updated successfully',)
                    return redirect('dashboard_page')
                else:
                    messages.warning(request,"Your Credentials will Expire")
                    return redirect('dashboard_pag')
            except Exception as e:
                messages.warning(request,"Your Credentials will Expire")
                return redirect('dashboard_pag')
        else:
            try:
                
                update_job_data = get_object_or_404(Job_detail,id=update_id)
                print(update_job_data)
                update_job_data.company_name = company_name
                update_job_data.date = date
                update_job_data.bill_no = bill_no
                update_job_data.job_name = job_name
                update_job_data.job_type = job_type
                update_job_data.noc = noc
                update_job_data.prpc_purchase = prpc_purchase
                update_job_data.prpc_sell = prpc_sell
                update_job_data.cylinder_size = cylinder_size
                update_job_data.cylinder_bill_no = cylinder_bill_no
                update_job_data.cylinder_size = cylinder_size
                update_job_data.correction = correction
                update_job_data.cylinder_made_in = cylinder_made_in
                update_job_data.pouch_size = pouch_size
                update_job_data.pouch_open_size = pouch_open_size
                update_job_data.cylinder_date  = cylinder_date
                update_job_data.job_status = job_status
                update_job_data.pouch_combination = pouch_combination
                
                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]  
                    Jobimage.objects.create(
                        job=update_job_data,
                        image=file_obj
                    )
                update_job_data.save()
                messages.success(request,'Data Update successfully ')
                return redirect('dashboard_page')
            except Exception:
                messages.warning(request,'Something went wrong try again')
                return redirect('dashboard_page')
           
    except Exception as e:
        messages.error(request,f'Something went wrong try again {e}')
        print(e)
        return redirect('dashboard_page')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def user_logout(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        logout(request)
        request.session.clear()
        return redirect('login_page')
    except Exception as e:
        messages.warning(request,f"Something went Wrong try again {e}")
        return redirect('dashboard_page')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def profile_page(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    return render(request,'profile.html')

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def update_profile(request,users_id):
    if not request.user.is_authenticated:
        return redirect('login_page')
    try:
        update_profile = get_object_or_404(Registration,id=users_id)
        if request.method == 'POST':
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            username = request.POST.get('username')
            email = request.POST.get('email')
        
        
        required_filed = {
            'First Name' :first_name,
            'Last Name':last_name,
            'Email':email,
            'Username':username
        } 
        
      
        for filed,required in required_filed.items():
            if not required:
                messages.error(request,f"{filed} is Required" ,extra_tags="custom-success-style")
                return redirect('profile_page')
            
        if email !=  update_profile.email and Registration.objects.filter(email=email).exists():
            messages.error(request,"Email alredy exists" ,extra_tags="custom-success-style")
            return redirect('profile_page')
        
        if username !=  update_profile.username and Registration.objects.filter(username=username).exists():
            messages.error(request,"Username alredy exists",extra_tags="custom-success-style")
            return redirect('profile_page')
        
        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, email):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
            return redirect('profile_page')
                
        update_profile.username = username
        update_profile.last_name = last_name
        update_profile.first_name = first_name
        update_profile.email = email
        update_profile.save()
        
        messages.success(request,"Profile Will Updated",)
        return redirect('profile_page')
    except Exception:
        messages.error(request,'Something went wrong  try again')
        return redirect('profile_page')
    
    
    
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def user_password(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        
        old_password = request.POST.get('old_password','').strip()
        new_password = request.POST.get('new_password','').strip()
        confirm_password = request.POST.get('confirm_password','').strip()
        
        
        if old_password == ''  or old_password == None:
            error = "Please provide Old Password."
            return render (request,'profile.html',context={'error':error})
            
        user_password = request.user
        if not user_password.check_password(old_password):
            messages.error(request,'Old Password is Incorrect',extra_tags='custom-success-style')
            return redirect('profile_page')
        
        
        
        if new_password == ''  or new_password == None:
            errors = "Please provide New Password."
            return render (request,'profile.html',context={'errors':errors})

        password_error = validator_password(new_password)
        if password_error:
            messages.error(request,password_error,extra_tags="custom-success-style")
            return redirect('profile_page') 
        
     
                
        if old_password == new_password:
            messages.error(request,"Your Current Passsword or New Password will same Add some Diffrent",extra_tags='custom-success-style')
            return redirect('profile_page')

        if new_password != confirm_password:
            messages.error(request,"new password or confirm Passworsd Must be same ",extra_tags='custom-success-style')
            return redirect("profile_page")
        
        user_password.set_password(new_password)
        user_password.save()
        # messages.success(request,'Password Updated Successfully',)
        print("Password Update")
        # update_session_auth_hash(request,user_password)
        return redirect('login_page')
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def comapny_add_page(request):
    
    search = request.GET.get('search',' ').strip()
    date = request.GET.get('date','').strip()
    end_date = request.GET.get('end_date','').strip()
    print(date)
    companay_name_sorting = request.GET.get('company_name_sorting','')
    job_name_sorting = request.GET.get('job_name_sorting','')
    date_sorting = request.GET.get('date_sorting','')
    sorting = request.GET.get('sorting','')
    
    # print(date_sorting)
    # print(companay_name_sorting)
    # print(sorting)
    # date = date.replace('-',',')
    # print(date)
    # date_object = datetime.strptime(date, "%Y-%m-%d")

   
    # one_year_later = date_object + relativedelta(years=1)

   
    # end_date = one_year_later.strftime("%Y-%m-%d")
    cdr_data = CDRDetail.objects.all()
    if search and date:
        cdr_data = CDRDetail.objects.filter(
            Q(date__icontains=date) &
            (
                Q(job_name__icontains=search) |
                Q(company_name__icontains=search) |
                Q(company_email__icontains=search)
            )
        )
    
    elif end_date and date:
        cdr_data = CDRDetail.objects.filter(date__range=(date, end_date))
    elif search:
        cdr_data  = CDRDetail.objects.filter(Q(job_name__icontains = search)| Q(company_name__icontains = search)| Q(company_email__icontains = search))
    elif date:
        cdr_data = CDRDetail.objects.filter(Q(date__icontains =  date))
    elif end_date:
        cdr_data = CDRDetail.objects.filter(Q(date__icontains =  end_date))
        
    order_by = ''
    if companay_name_sorting == 'asc':
        order_by = 'company_name'
    elif companay_name_sorting == 'desc':
        order_by = '-company_name'
    elif job_name_sorting == 'asc':
        order_by = 'job_name'
    elif job_name_sorting == 'desc':
        order_by = '-job_name'
    elif date_sorting == 'asc':
        order_by = 'date'
        print  (cdr_data)
    elif date_sorting == 'desc':   
        order_by = '-date'
    elif sorting == 'desc':
        order_by = '-id'
        
    if order_by:
        cdr_data = cdr_data.order_by(order_by)
    else:
        cdr_data = cdr_data.order_by('date')
    
    
    
        
 
    p = Paginator(cdr_data,10)
    
    page =  request.GET.get('page')
    cdr_emails = CDRDetail.objects.values('company_email').distinct()
    cdr_company_name = CDRDetail.objects.values('company_name').distinct()
    cdr_job_name = CDRDetail.objects.values('job_name').distinct()
    
    print(cdr_emails)
    datas = p.get_page(page)
    nums = "a" * datas.paginator.num_pages
    context = {
        
        'nums': nums,
        'cdr_details':datas,
        'page_obj':datas,
        'search':search,
        'date':date,
        'end_date':end_date,
        'cdr_email':cdr_emails,
        'cdr_company_name':cdr_company_name,
        'cdr_job_names':cdr_job_name,
        
    }
    return render(request,'CDR/add_company.html',context)


def cdr_add(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name','').strip()
        company_email = request.POST.get('company_email','').strip()
        cdr_upload_date = request.POST.get('cdr_upload_date','').strip()
        cdr_files  =  request.FILES.getlist('cdr_files','')
        job_name = request.POST.get('job_name',)
        cdr_corrections_data = request.POST.get('cdr_corrections')
        new_company_name = request.POST.get('new_company_name','').strip()
        new_company_email = request.POST.get('new_company_email','').strip()
        new_job_name =  request.POST.get('new_job_name','').strip()
        
        
            
            

        if not job_name or not cdr_upload_date:
            messages.error(request, "Job name and upload date are required.", extra_tags='custom-error-style')
            return redirect('company_add_page')
        
        if new_job_name !='':
            job_name = new_job_name

        if new_company_email != '':
            company_email = new_company_email 
        if new_company_name != '':
            company_name = new_company_name  

        
        
        required_filed = {
            'Company Name': company_name,
            'Company Email': company_email,
            'Upload Date': cdr_upload_date,
            'Job Name': job_name,
        }


        for filed,required in required_filed.items():
            if not required:
                messages.error(request,f"{filed} is Required" ,extra_tags="custom-success-style")
                return redirect('company_add_page')
        
        if not cdr_files:
            messages.error(request,"CDR File is Required",extra_tags='custom-success-style')
            return redirect('company_add_page')
        if len(cdr_files) > 2:
            messages.error(request, "You can upload only 2 files", extra_tags="custom-error-style")
            return redirect('company_add_page')
        

        if CDRDetail.objects.filter(company_name = company_name, company_email=company_email).exists():
            print("Valid")
        else:
            if CDRDetail.objects.filter(company_name = company_name).exists():
                messages.error(request,"Choose Another Company Name",extra_tags='custom-success-style')
                return redirect('company_add_page')
            if CDRDetail.objects.filter(company_email = company_email).exists():
                messages.error(request,"Choose Another Email",extra_tags='custom-success-style')
                return redirect('company_add_page')
            
        
        if CompanyName.objects.filter(company_name__icontains = company_name).exists():
            print("Compnay Alredy Exsits")
        else:
            company_add_in = CompanyName.objects.create(
                company_name = company_name
            )       
            company_add_in.save()        
        
        if CDRDetail.objects.filter(job_name__icontains = job_name,date=cdr_upload_date ).exists():
            messages.error(request,'Job Name are alredy Exsits on this date  kidnly Update job',extra_tags='custom-success-style')
            return redirect('company_add_page')

        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, company_email):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style") 
            return redirect('company_add_page')

        
      

       
        data = {
            'company_name':company_name,
            'company_email':company_email,
            'cdr_upload_date':cdr_upload_date,
            'job_name':job_name,
            'cdr_corrections':cdr_corrections_data,
            
        }
        file_dic = {}
        for i, file in enumerate(cdr_files):
            _, file_extension = os.path.splitext(file.name)
            random_number = random.randint(1, 100)
            new_file_name = f'{cdr_upload_date}_{random_number}{file_extension}'
            file.name = new_file_name
            file_key = f"{new_file_name}"
            file_dic[file_key] = (file.name, file, file.content_type)
            
            
            
        url = os.environ.get('CREATE_WEBHOOK_CDR')
        response = requests.post(f'{url}',data=data,files=file_dic)
        print(response.status_code)
        
        data_string  = response.text
 
        print(data_string)
        
        if response.status_code  == 200:
            print("Positive Response : ",response)
            messages.success(request,"Data Succfully Add ")
            return redirect('company_add_page')
        else:

            cdr_data = CDRDetail.objects.create(
                date=cdr_upload_date,
                company_name=company_name,
                company_email=company_email,
                cdr_corrections=cdr_corrections_data,
                job_name=job_name
            )

            for file_key, file_data in file_dic.items():
                file_object = file_data[1]  
                CDRImage.objects.create(
                    cdr=cdr_data,
                    image=file_object,
                )
            cdr_data.save()
            messages.success(request, 'Data successfully added to SQLite DB')

            return redirect('company_add_page')
    

@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def cdr_delete(request,delete_id):
    url = os.environ.get('DELETE_WEBHOOK_CDR')
    folder_url = CDRDetail.objects.get(id=delete_id).file_url
    print(folder_url)
    if folder_url:
        response = requests.delete(f"{url}{delete_id}")
        if response.status_code == 200:
            messages.success(request,"CDR File Deleted successfully ")
            return redirect('company_add_page')
        else:
            messages.warning(request,"Your Credentials will Expire")
            return redirect('company_add_page')

    else:
        delete = get_object_or_404(CDRDetail, id = delete_id)
        print(delete)
        delete_image = delete.cdr_images.all()
        for img in delete_image:
            path = img.image.path
            print(path)
            if os.path.isfile(path):
                os.remove(path)
            else:
                img.delete()
        delete.delete()
        messages.success(request,"Data Delete successfully")
        return redirect('company_add_page')

        
    
    # response = requests.delete(f"http://localhost:5678/webhook/d51a7064-e3b9-41f5-a76f-264e19f60b70/cdr/delete/{delete_id}")
    # print(response.status_code)
    # if response.status_code == '200':
    #     messages.success(request,"CDR File Deleted successfully ")
    #     return redirect('company_add_page')
    # messages.success(request,"CDR File Deleted successfully ")
    # return redirect('company_add_page')





@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def cdr_update(request,update_id):
    
    id = update_id
    if request.method == 'POST':
        date = request.POST.get('cdr_upload_date')
        
        company_email = request.POST.get('company_email','').strip()
        cdr_files = request.FILES.getlist('files')
        company_name = request.POST.get('company_name')
        job_names = request.POST.get('job_name')
    
        cdr_corrections = request.POST.get('cdr_corrections')
        
        
        if CDRDetail.objects.filter(company_name__icontains = company_name, company_email=company_email).exists():
            print("Valid")
        else:
        
            if CDRDetail.objects.filter(company_email__icontains = company_email).exists():
                messages.error(request,"Choose Another Email",extra_tags='custom-success-style')
                return redirect('company_add_page')

        
        if len(cdr_files) > 2:
            messages.error(request,"More than 2 file not allowed",extra_tags='custom-success-style')
            return redirect('company_add_page')
        
        file_dic = {}
        for i, file in enumerate(cdr_files):
            # Get the original file extension
            _, file_extension = os.path.splitext(file.name)
            random_number = random.randint(1, 100)
            new_file_name = f'{date}_{random_number}{file_extension}'
            file.name = new_file_name
            file_key = f"{new_file_name}"
            file_dic[file_key] = (file.name, file, file.content_type)
        
        company_email = str(company_email).strip()
        print(company_email)
        
        get_email = CDRDetail.objects.values_list('company_email').get(id=id)
        email_string = get_email[0] 
        print(str(email_string))
        
        if company_email ==  email_string:
            print("No Chnage")
        else:
            CDRDetail.objects.filter(company_email=email_string).update(company_email=company_email)     
        url = os.environ.get('UPDATE_WEBHOOK_CDR')
        if not cdr_files:
            update_details = get_object_or_404(CDRDetail,id=id)
            update_details.company_email = company_email
            update_details.cdr_corrections = cdr_corrections
            update_details.job_name = job_names
            update_details.date = date
            update_details.save()
            messages.success(request,"CDR Data Updated")
            return redirect('company_add_page')
        else:
            get_folder_url = CDRDetail.objects.values_list('file_url').get(id=id)
            folder_url = get_folder_url[0]
            if folder_url:
                data = {
                    'date':date,
                    'company_email':company_email,
                    'company_name':company_name,
                    'job_name':job_names,
                    'cdr_corrections':cdr_corrections
                }
                response = requests.post(f"{url}{id}",data=data,files=file_dic)
                
                if response.status_code == 200:
                    messages.success(request,'Data Update Successfully')
                    return redirect('company_add_page')
                else:
                    messages.warning(request,"Your Credentials will Expire")
                    return redirect('company_add_page')
            else:
                update_details = get_object_or_404(CDRDetail,id=id)
                update_details.company_email = company_email
                update_details.cdr_corrections = cdr_corrections
                update_details.job_name = job_names
                update_details.date = date
                
                for file in file_dic:
                    CDRImage.objects.create(
                        
                        cdr = update_details,
                        image = file
                    )
                update_details.save()
                messages.success(request,'Data Update Successfullyss')
                return redirect('company_add_page')
            
    return redirect('company_add_page')

def offline_page(request):
    return render(request,'Base/offline_page.html')

from django.core.mail import EmailMultiAlternatives
@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def cdr_sendmail_data(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        date = request.POST.get('date'," ")
        cdr_company_name = request.POST.get('cdr_company_name'," ")
        cdr_company_address = request.POST.get('cdr_company_address'," ")
        attachments  = request.FILES.getlist('attachment')
        cdr_job_name = request.POST.get('cdr_job_name',' ')
        cdr_corrections = request.POST.get('cdr_corrections'," ")
        cdr_notes = request.POST.get('notes'," ")
        correction_check = request.POST.get('correction_check','')
        cdr_date_check = request.POST.get('cdr_date_check')
   
        if cdr_date_check == None or cdr_date_check == '':
            date = ''
        else:
            date = date
        if correction_check == None or correction_check == '':
            cdr_corrections = ''
        else:
            cdr_corrections = cdr_corrections
        # print(date)
        
        # for attachment in attachments:
        #     print(attachment.size)

        #     if attachments.size > 25  * 1024 *1024:
        #         messages.error(request,"This Image Error ")
        #         return redirect("company_add_page")
        # print(selected_items)
        
        
        email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, cdr_company_address):
            messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style")
            return redirect('company_add_page')
    
        total_attachment_size = sum(f.size for f in attachments)
        MAX_SIZE_MB = 25
        if total_attachment_size > MAX_SIZE_MB * 1024 * 1024:
            messages.error(request, f"Total file size exceeds {MAX_SIZE_MB}MB. Please upload smaller files.",extra_tags="custom-success-style")
            return redirect('company_add_page')
        
        
        CDR_INFO = {
            "date":date,
            "Company_Email":cdr_company_address,
            "Company_Name":cdr_company_name,
            "cdr_job_name":cdr_job_name,
            "cdr_corrections":cdr_corrections,
            "notes":cdr_notes,
        }

        receiver_email = cdr_company_address
        template_name =  "Base/cdr_email.html"
        convert_to_html_content =  render_to_string(
        template_name=template_name,
        context=CDR_INFO

        )
        email = EmailMultiAlternatives(
            subject="Mail From Nirmal Ventures",
            body="plain_message",
            from_email='Soniyuvraj9499@gmail.com',
            to=[receiver_email]
        )
        email.attach_alternative(convert_to_html_content,"text/html")
        for i in attachments:
            email.attach(i.name, i.read(), i.content_type)
        email.send()
        messages.success(request,"Mail Send successfully")
        return redirect('company_add_page')
    
    return redirect('company_add_page')





@never_cache
@cache_control(no_store=True, no_cache=True, must_revalidate=True, max_age=0) 
@login_required(redirect_field_name=None)
def send_mail_data(request):
    if not request.user.is_authenticated:
        return redirect('login_page')
    if request.method == 'POST':
        date_check = request.POST.get('date_check')
        date = request.POST.get('date',"")
        bill_no = request.POST.get('bill_no',"")
        company_name = request.POST.get('company_name',"")
        company_email_address = request.POST.get('company_address')
        job_name = request.POST.get('job_name',"")
        noc = request.POST.get('noc',"")
        prpc_sell_check = request.POST.get('prpc_sell_check','')
        prpc_sell = request.POST.get('prpc_sell',"")
        cylinder_size = request.POST.get('cylinder_size',"")
        pouch_size = request.POST.get('pouch_size',"")
        pouch_open_size = request.POST.get('pouch_open_size',"")
        correction = request.POST.get('correction',"")
        correction_check = request.POST.get('correction_check','')
        attachments  = request.FILES.getlist('attachment')
        note  = request.POST.get('note')
        # selected_item = request.POST.getlist('select_item[]',"")

    # if len(attachments) >= 3 :
    #     messages.error(request,"You can upload only 2 file")
    #     return redirect('dashboard_page')
    if date_check == None or date_check == '':
        date = ''
    else:
        date = date 
    
    
    
    if correction_check == None or correction_check == '':
        correction = ''
    else:
        correction = correction
    
    if prpc_sell_check == None or prpc_sell_check == '':
        prpc_sell = ''
    else:
        prpc_sell = prpc_sell
    
    # if 'prpc_sell_check' in request.POST:
        
    #     is_checked = True   
    #     prpc_sell = prpc_sell
    # else:
    #     is_checked = False
    #     prpc_sell = ''
    

    # print(prpc_sell)
    # print(date,bill_no,company_name,company_email_address,job_name,noc,prpc_sell,cylinder_size,pouch_size,pouch_open_size,correction)
    # print(attachments)
    # required_field = {
    #                 'Date' :date,
    #                 'Bill no':bill_no,
    #                 'Company_Name': company_name,
    #                 'job name' : job_name,
    #                 'Noc':noc,
    #                 'Cylinder Size':cylinder_size,
    #                 'Pouch size':pouch_size,
    #                 'Prpc Sell':prpc_sell,
    #                 'Pouch Open Size':pouch_open_size,
    #                 'Company Email Address':company_email_address , 
                    
    #         }
    
    # for i ,r in required_field.items(): 
    #     if not  r:
    #         messages.error(request,f"This {i} Field Was Required",extra_tags="custom-success-style")
    #         return redirect('dashboard_page')
    
    
    if company_email_address == '' or company_email_address == None:
        messages.error(request,"Kindly provide Company email",extra_tags="custom-success-style")
        return redirect('dashboard_page')
    
    email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex, company_email_address):
        messages.error(request, "Enter a valid email address.",extra_tags="custom-success-style")
        return redirect('dashboard_page')
    
     
    
    
    # ValidateImage = [".jpeg", ".jpg", ".png" ,".ai"]
    # for file in attachments:
    total_attachment_size = sum(f.size for f in attachments)
    print(total_attachment_size)
    MAX_SIZE_MB = 25
    if total_attachment_size > MAX_SIZE_MB * 1024 * 1024:
        messages.error(request, f"Total file size exceeds {MAX_SIZE_MB}MB. Please upload smaller files.",extra_tags="custom-success-style")
        return redirect('dashboard_page')
    
    
    job_info = {
                "date": date,
                "bill_no": bill_no,
                "company_name": company_name,
                "company_email_address": company_email_address,
                "job_name":job_name,
                "noc":noc,
                "prpc_sell":prpc_sell,
                "cylinder_size":cylinder_size,
                "pouch_size":pouch_size,
                "pouch_open_size":pouch_open_size,
                "correction":correction,
                'note':note

        }
    
    print(job_info)
    
    receiver_email = company_email_address
    template_name  = "Base/send_email.html"
    convert_to_html_content =  render_to_string(
    template_name=template_name,
    context=job_info

    )
    email = EmailMultiAlternatives(
    subject="Mail From Nirmal Ventuers",
    body='plain_message',
    from_email=request.user.email,
    to=[receiver_email],

    )
    email.attach_alternative(convert_to_html_content, "text/html")
    for  i in attachments:
        email.attach(i.name, i.read(), i.content_type)
    email.send()
        
    messages.success(request,"Mail Send successfully")
    return redirect('dashboard_page')
    
def company_name_suggestion(request):
    company_name = request.GET.get('company_name', '')
    if company_name:
      
     
        jobs = list(
            CDRDetail.objects.filter(company_name__iexact=company_name)
            .values('job_name')  
            .distinct()
        )

        email = list(CDRDetail.objects.filter(company_name__iexact=company_name).values('company_email').distinct())
        print(email)
        return JsonResponse({
            'email': email,
            'jobs': jobs
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)


def company_name_suggestion_job(request):
    company_name = request.GET.get('company_name', '')
    
    
    if company_name:
        # jobs = list(
        #     Job_detail.objects.filter(company_name__iexact=company_name)
        #     .values('job_name').distinct()
        # )
        job_detail = Job_detail.objects.filter(company_name__iexact=company_name).values('job_name').distinct()
        # print(job_detail)
        cdr_job = CDRDetail.objects.filter(company_name__iexact=company_name).values('job_name').distinct()
        # print(cdr_job)
 
        jobs = list(job_detail.union(cdr_job))


        # for _ in job_detail:
        #     if _ not in cdr_job:
        #         cdr_job.append(job_detail)
        # print(cdr_job)


        
        return JsonResponse({'jobs': jobs})
    return JsonResponse({'error': 'Invalid request'}, status=400)
        
# def job_detail_print(request,job_id):
#     print(job_id)
    
#     try:
        
#         item = Job_detail.objects.get(id = job_id)
#         data = {
#             'id': item.id,
#             'description': item.correction,
            
#         }
#         return JsonResponse(data)
#     except Job_detail.DoesNotExist:
#             return JsonResponse({'error': 'Item not found'}, status=404)

# email = EmailMessage(
#                 'Subject of the email',
#                 'Body of the email',
#                 'sender@example.com',  # From email address
#                 ['recipient@example.com'], # To email address(es)
#             )

#             # Attach each file
#             for uploaded_file in attachments:
#                 email.attach(uploaded_file.name, uploaded_file.read(), uploaded_file.content_type)

#             email.send()
#             return render(request, 'success.html')
# def check_user_active_session(user_id):
#     try:
#         user = User.objects.get(pk=user_id)  # Retrieve the User object by ID
#     except User.DoesNotExist:
#         # Handle the case where no user with that ID exists
#         return False

#     # Check for active sessions associated with this user
#     sessions = Session.objects.filter(expire_date__gt=datetime.now()) # Filter for active sessions
    
#     for session in sessions:
#         decoded_session = session.get_decoded()  # Decode the session data
#         if decoded_session.get('_auth_user_id') == user.id:  # Check if the session belongs to the given user
#             return True  # User is currently logged in via an active session
    
#     return False


# # views.py

# import os
# import io
# from django.shortcuts import redirect, render
# from django.conf import settings
# from django.core.files.storage import default_storage
# from google_auth_oauthlib.flow import Flow
# from googleapiclient.discovery import build
# from googleapiclient.http import MediaIoBaseUpload
# from django.views.decorators.csrf import csrf_exempt

# # Scopes for Drive
# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# # Temp in-memory user session token storage (for demo)
# user_credentials = {}

# def authorize(request):
#     flow = Flow.from_client_config(
#         {
#             "web": {
#                 "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
#                 "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#                 "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#             }
#         },
#         scopes=SCOPES,
#     )
#     flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
#     authorization_url, state = flow.authorization_url(
#         access_type='offline',
#         include_granted_scopes='true',
#         prompt='consent'
#     )
#     request.session['state'] = state
#     return redirect(authorization_url)


# def oauth2callback(request):
#     state = request.session['state']
#     flow = Flow.from_client_config(
#         {
#             "web": {
#                 "client_id": settings.GOOGLE_OAUTH2_CLIENT_ID,
#                 "client_secret": settings.GOOGLE_OAUTH2_CLIENT_SECRET,
#                 "redirect_uris": [settings.GOOGLE_OAUTH2_REDIRECT_URI],
#                 "auth_uri": "https://accounts.google.com/o/oauth2/auth",
#                 "token_uri": "https://oauth2.googleapis.com/token",
#             }
#         },
#         scopes=SCOPES,
#         state=state
#     )
#     flow.redirect_uri = settings.GOOGLE_OAUTH2_REDIRECT_URI
#     flow.fetch_token(authorization_response=request.build_absolute_uri())
#     credentials = flow.credentials

#     # Save credentials for later use
#     request.session['credentials'] = {
#         'token': credentials.token,
#         'refresh_token': credentials.refresh_token,
#         'token_uri': credentials.token_uri,
#         'client_id': credentials.client_id,
#         'client_secret': credentials.client_secret,
#         'scopes': credentials.scopes
#     }

#     return redirect('upload_file')


# @csrf_exempt
# def upload_file(request):
#     if request.method == 'POST':
#         file = request.FILES['file']
#         credentials_data = request.session.get('credentials')

#         if not credentials_data:
#             return redirect('authorize')

#         from google.oauth2.credentials import Credentials

#         credentials = Credentials(
#             **credentials_data
#         )

#         service = build('drive', 'v3', credentials=credentials)

#         file_metadata = {'name': file.name}
#         media = MediaIoBaseUpload(file, mimetype=file.content_type)

#         uploaded_file = service.files().create(
#             body=file_metadata,
#             media_body=media,
#             fields='id'
#         ).execute()

#         return render(request, 'upload.html', {
#             'message': f"File uploaded successfully to Google Drive with ID: {uploaded_file.get('id')}"
#         })

#     return render(request, 'upload.html')
       # import re
# from django.shortcuts import redirect
# from django.contrib import messages
# from .models import CDRDetail
# from .google_drive_service import get_drive_service, create_company_folder


# def cdr_add(request):
#     if request.method == 'POST':
#         company_name = request.POST.get('company_name')
#         company_email = request.POST.get('company_email')
#         cdr_upload_date = request.POST.get('cdr_upload_date')
#         cdr_files = request.FILES.getlist('cdr_files')  # assuming multiple files

#         # Validate required fields
#         required_fields = {
#             'Company Name': company_name,
#             'Company Email': company_email,
#             'Upload Date': cdr_upload_date,
#         }

#         for field_name, value in required_fields.items():
#             if not value:
#                 messages.error(request, f'{field_name} is required.')
#                 return redirect('company_add_page')

#         # Check for existing email
#         if CDRDetail.objects.filter(company_email=company_email).exists():
#             messages.error(request, "Company Email already exists.", extra_tags='custom-success-style')
#             return redirect('company_add_page')

#         # Validate email format
#         email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
#         if not re.match(email_regex, company_email):
#             messages.error(request, "Enter a valid email address.", extra_tags="custom-success-style")
#             return redirect('company_add_page')

#         # Create database record
#         cdr_upload = CDRDetail.objects.create(
#             date=cdr_upload_date,
#             company_email=company_email,
#             company_name=company_name
#         )

#         # Google Drive folder creation
#         try:
#             service = get_drive_service()
#             parent_folder_id = 'YOUR_PARENT_FOLDER_ID'  # Replace with your actual parent folder ID
#             folder_id, folder_link = create_company_folder(service, company_name, parent_folder_id)

#             # Save folder link
#             cdr_upload.google_drive_folder = folder_link
#             cdr_upload.save()
#         except Exception as e:
#             messages.error(request, f"Google Drive folder creation failed: {str(e)}")
#             return redirect('company_add_page')

#         messages.success(request, "New company added successfully.")
#         return redirect('company_add_page')

#     return redirect('company_add_page')


# import os
# import pickle
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build

# SCOPES = ['https://www.googleapis.com/auth/drive.file']

# def get_drive_service():
#     creds = None
#     if os.path.exists('token.pickle'):
#         with open('token.pickle', 'rb') as token:
#             creds = pickle.load(token)

#     if not creds or not creds.valid:
#         flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#         creds = flow.run_local_server(port=0)
#         with open('token.pickle', 'wb') as token:
#             pickle.dump(creds, token)

#     return build('drive', 'v3', credentials=creds)


# def create_company_folder(service, company_name, parent_folder_id=None):
#     file_metadata = {
#         'name': company_name,
#         'mimeType': 'application/vnd.google-apps.folder',
#     }
#     if parent_folder_id:
#         file_metadata['parents'] = [parent_folder_id]

#     folder = service.files().create(body=file_metadata, fields='id').execute()
#     folder_id = folder.get('id')
#     folder_link = f"https://drive.google.com/drive/folders/{folder_id}"
#     return folder_id, folder_link



# ajax part


        
        
   


# def get_company_data(request):
#     company_name = request.GET.get('company_name')
#     if company_name:

#         jobs = list(
#             CDRDetail.objects.filter(company_name=company_name)
#             .values('job_name')
#             .distinct()
#         )
       
#         email = CDRDetail.objects.filter(company_name=company_name).values_list('company_email', flat=True).first()
        
#         return JsonResponse({
#             'email': email,
#             'jobs': jobs
#         })
#     return JsonResponse({'error': 'Invalid request'}, status=400)