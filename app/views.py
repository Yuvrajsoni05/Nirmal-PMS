from calendar import c
import json
import logging

import os
import re
from datetime import datetime


import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (PasswordResetConfirmView,PasswordResetDoneView,

                                       PasswordResetView)


from django.contrib.sessions.models import Session
# mail
from django.core.mail import EmailMultiAlternatives
from django.core.paginator import Paginator
from django.db import utils
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.views.decorators.http import require_GET




from .decorators import *
from .models import *

from . import utils 
# Password

from django.http import HttpResponse

# Swagger Setting


# Create your views here.


# urlpatterns = [
#     urls(r'^$', schema_view)
# ]


# Lecco ai
# Cookies in  Django Section in django

    
logger = logging.getLogger("myapp")
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
    return render(request, "Password/password_update_done.html")





def login_page(request):
    try:
        if request.method == "POST":
            username_email = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()
            remember_me = request.POST.get("remember_me", "").strip()

            valid = re.fullmatch(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", username_email
            )
            print("Received Login:", username_email, password)
    
            if valid:
                try:
                    user_login = Registration.objects.get(
                        email=username_email.lower()
                    ).username
                except Registration.DoesNotExist:
                    messages.error(request, "Email not found.")
                    return redirect("login_page")
                user = authenticate(request, username=user_login, password=password)
            else:
                user = authenticate(request, username=username_email, password=password)
            if user is not None:
                if remember_me == "on":
                    request.session['name'] = username_email
                    request.session.set_expiry(60 * 60 * 24 * 30)
                else:
                    request.session.set_expiry(0)
                login(request, user)
                messages.success(request, f"You are logged in {user.username} ")
                logger.info("user Login")
                return redirect("dashboard_page")
            else:
                messages.error(request, "Invalid Username or Password")
                logger.error(f"Invalid Username or Password")

                return redirect("login_page")
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        messages.warning(request, f"Something went wrong, try again.")
        return redirect("login_page")

    return render(request, "Registration/login_page.html")




        
            
    

@custom_login_required
def register_page(request):
    if "HX-Request" in request.headers:
        username = request.GET.get("username", "").strip()
        email = request.GET.get("emailAddress","").strip()
        
        if username:
            if Registration.objects.filter(username=username).exists():
                return HttpResponse("username already exists")
        if email:
            if Registration.objects.filter(email=email).exists():
                return HttpResponse("email already exists")
        
        return HttpResponse()
 
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        first_name = request.POST.get("firstName", "").strip()
        last_name = request.POST.get("lastName", "").strip()
        email = request.POST.get("emailAddress", "").strip()
        password = request.POST.get("password", "").strip()
        confirm_password = request.POST.get("confirm_password", "").strip()
        required_filed = {
            "First Name": first_name,
            "Last Name": last_name,
            "Username": username,
            "Password": password,
        }

        for i, required in required_filed.items():
            if not required:
                messages.error(
                    request,
                    f" {i} field is Required",
                    extra_tags="custom-danger-style",
                )
                return redirect("register_page")

        if Registration.objects.filter(username=username).exists():
            messages.error(
                request, "Username Already Exist", extra_tags="custom-danger-style"
            )
            return redirect("register_page")

        email_error = utils.email_validator(email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("register_page")

        email_check_error = utils.email_check(email)
        if email_check_error:
            messages.error(
                request, email_check_error, extra_tags="custom-danger-style"
            )
            return redirect("register_page")

        password_error = utils.validator_password(password)
        if password_error:
            messages.error(request, password_error, extra_tags="custom-danger-style")
            if password != confirm_password:
                messages.error(
                    request,
                    "Password Confirm Password must be same",
                    extra_tags="custom-danger-style",
                )
                return redirect("register_page")

        create_user = Registration.objects.create_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            password=password,
            email=email,
        )
        create_user.save()
        messages.success(request, "New User Will Created")
        return redirect("edit_user_page")
    return render(request, "Registration/register.html")


@custom_login_required
def edit_user_page(request):
    user_details = (
        Registration.objects.exclude(is_superuser=True)
        .exclude(id=request.user.id)
        .order_by("username")
    )
    context = {"users": user_details}
    return render(request, "Registration/edit_user.html", context)


@custom_login_required
def delete_user(request, user_id):
    if request.method == "POST":
        Delete_user = get_object_or_404(Registration, id=user_id)
        Delete_user.delete()
        messages.success(request, "User Deleted")
        return redirect("edit_user_page")


@custom_login_required
def update_user(request, user_id):
    try:
        if request.method == "POST":
            update_user = get_object_or_404(Registration, id=user_id)
            username = request.POST.get("username", "").strip()
            email = request.POST.get("email", "").strip()
            first_name = request.POST.get("first_name", "").strip()
            last_name = request.POST.get("last_name", "").strip()

            required_fields = {
                "Username": username,
                "Firstname": first_name,
                "Lastname": last_name,
                "Email": email,
            }
            for field_name, value in required_fields.items():
                if not value:
                    messages.error(
                        request,
                        f"{field_name} is required.",
                        extra_tags="custom-danger-style",
                    )
                    return redirect("edit_user_page")

            email_error = email_error = utils.email_validator(email)
            if email_error:
                messages.error(request, email_error, extra_tags="custom-danger-style")
                return redirect("edit_user_page")

            if (
                username != update_user.username
                and Registration.objects.filter(username=username).exists()
            ):
                messages.error(
                    request,
                    "Username already exists.",
                    extra_tags="custom-danger-style",
                )
                return redirect("edit_user_page")

            if (
                email != update_user.email
                and Registration.objects.filter(email=email).exists()
            ):
                messages.error(
                    request, "Email already exists.", extra_tags="custom-danger-style"
                )
                return redirect("edit_user_page")

            required_fields = {
                "Username": username,
                "Firstname": first_name,
                "Lastname": last_name,
                "Email": email,
            }

            for field_name, value in required_fields.items():
                if not value:
                    messages.error(
                        request,
                        f"{field_name} is required.",
                        extra_tags="custom-danger-style",
                    )
                    return redirect("edit_user_page")

            if username != update_user.username:
                update_user.username = username
            if email != update_user.email:
                update_user.email = email

            update_user.first_name = first_name
            update_user.last_name = last_name

            logout_user = Registration.objects.get(id=user_id)
            for session in Session.objects.all():
                session_data = session.get_decoded()
              
                if str(session_data.get("_auth_user_id")) == str(logout_user.id):
                    session.delete()
            update_user.save()
            messages.success(request, "User updated successfully.")
            return redirect("edit_user_page")
    except Exception as e:
    
        messages.error(
            request, f"Something went wrong", extra_tags="custom-danger-style"
        )
        return redirect("edit_user_page")


@custom_login_required
def dashboard_page(request):
    try:
        party_name_search = request.GET.get("party_name", "").strip()
        job_name_search = request.GET.get("job_name_search", "").strip()
        start_date = request.GET.get("start_date", "").strip()
        end_date = request.GET.get("end_date", "").strip()
        sorting = request.GET.get("sorting", "").strip()
        date_sorting = request.GET.get("date_sorting", "").strip()
        party_name_sorting = request.GET.get("party_name_sorting", "").strip()
        job_name_sorting = request.GET.get("job_name_sorting", "").strip()
        cylinder_date_sorting = request.GET.get("cylinder_date_sorting", "").strip()
        cylinder_made_in_sorting = request.GET.get("cylinder_made_in_sorting", "").strip()
        filters = Q()
        if party_name_search:
            filters &= Q(party_details__party_name__icontains=party_name_search)
        if job_name_search:
            filters &= Q(job_name__icontains=job_name_search)


        if start_date and end_date:
            filters &= Q(date__range=[start_date, end_date])
        elif start_date:
            filters &= Q(date__icontains=start_date)
        elif end_date:
            filters &= Q(date__icontains=end_date)
        
        job_details = Job_detail.objects.filter(filters)
        job_status = Job_detail.objects.values("job_status").distinct()
       
        sorting_map = {
            "asc": "id",
            "desc": "-id",
            "job_name_asc": "job_name",
            "job_name_desc": "-job_name",
            "date_asc": "date",
            "date_desc": "-date",
            "cyl_date_asc": "cylinder_date",
            "cyl_date_desc": "-cylinder_date",
            "company_asc": "party_details__party_name",
            "company_desc": "-party_details__party_name",
            "madein_asc": "cylinder_made_in",
            "madein_desc": "-cylinder_made_in",
        }
      
        sort_key = (
            f"job_name_{job_name_sorting}" if job_name_sorting else
            f"date_{date_sorting}" if date_sorting else
            f"cyl_date_{cylinder_date_sorting}" if cylinder_date_sorting else
            f"company_{party_name_sorting}" if party_name_sorting else
            f"madein_{cylinder_made_in_sorting}" if cylinder_made_in_sorting else
            sorting
        )

        
        if sort_key in sorting_map:
            job_details = job_details.order_by(sorting_map[sort_key])
        else:
            job_details = job_details.order_by("-job_status", "date" ,"id")
            
        paginator = Paginator(job_details, 10)
        page_number = request.GET.get("page")
        page_obj = paginator.get_page(page_number)
        
        total_job = job_details.count()
        for i in job_details:
            print(i)
        party_names = Party.objects.values("party_name").distinct()
        job_names = Job_detail.objects.values("job_name").distinct()
        count_of_company = Party.objects.all().order_by("party_name").count()

        cylinder_company_names = CylinderMadeIn.objects.all()
        total_active_job = job_details.filter(job_status="In Progress").count()
        count_of_cylinder_company = cylinder_company_names.count()
        nums = "*" * page_obj.paginator.num_pages
        if not job_details:
            messages.error(request,"No data available", extra_tags="custom-danger-style")
        context = {
            "nums": nums,
            "jobrecoreds": page_obj,
            "total_job": total_job,
            "job_names": job_names,
            "party_names": party_names,
            "cylinder_company_names": cylinder_company_names,
            "count_of_company": count_of_company,
            "count_of_cylinder_company": count_of_cylinder_company,
            "sorting": sorting,
            "party_name_sorting": party_name_sorting,
            "job_name_sorting": job_name_sorting,
            "date_sorting": date_sorting,
            "cylinder_date_sorting": cylinder_date_sorting,
            "cylinder_made_in_sorting": cylinder_made_in_sorting,
            "total_active_job": total_active_job,
            "job_status": job_status,
        }
        
    except Exception as e:
        messages.warning(request, "Something went wrong  try again")
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        return redirect("dashboard_page")
    return render(request, "dashboard.html", context)


@custom_login_required
def delete_data(request, delete_id):
   
    try:
            delete_data = get_object_or_404(Job_detail, id=delete_id)
            delete_images = delete_data.image.all()
            
            for img in delete_images:
                path = img.image.path
               
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    img.delete()
            delete_data.delete()
            messages.success(request, "Job Deleted successfully")
            return redirect("dashboard_page")
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        messages.warning(request, "Something went Wrong", e)
        return redirect("dashboard_page")





@custom_login_required
def job_entry(request):
    party_names = Party.objects.values("party_name").distinct()
    job_status = Job_detail.JOB_STATUS_CHOICES
    job_type = Job_detail.JOB_TYPE_CHOICES
     
    cylinder_company_names = CylinderMadeIn.objects.all()
    cdr_job_name = CDRDetail.objects.values("job_name").distinct()
    context = {
        "party_names": party_names,
        "cylinder_company_names": cylinder_company_names,
        "job_name": cdr_job_name,
        "job_status":job_status,
        "job_type":job_type
    }
    return render(request, "job_entry.html", context)


@custom_login_required
def create_job(request):
    try:
        if request.method == "POST":
            date = request.POST.get("job_date" ,'')
            bill_no = request.POST.get("bill_no"  ,'')
            party_name = request.POST.get("party_name", "")
            new_party_name = request.POST.get("new_party_name", "").strip()
            job_name_list = request.POST.getlist("job_name_real")
            job_type = request.POST.getlist("job_type")
            noc = request.POST.getlist("noc")
            prpc_purchase = request.POST.getlist("prpc_purchase")
            prpc_sell = request.POST.getlist("prpc_sell")
            cylinder_size = request.POST.getlist("cylinder_size[]")
            cylinder_made_in_s = request.POST.getlist("cylinder_made_in_real")
            cylinder_date = request.POST.getlist("cylinder_date")
            cylinder_bill_no = request.POST.getlist("cylinder_bill_no")
            pouch_size = request.POST.getlist("pouch_size[]")
            pouch_open_size = request.POST.getlist("pouch_open_size[]")
            pouch_combination = request.POST.getlist('pouch_combination[]')
            correction = request.POST.get("correction")
            job_status = request.POST.get("job_status")
        
            job_name = [name.strip() for name in job_name_list]

            required_filed = {
                "Date": date,
                "Bill no": bill_no,
                "Party Name": party_name,
                "job name": job_name,
                "job type": job_type,
                "Noc": noc,
                "Prpc Purchase": prpc_purchase,
                "Cylinder Size": cylinder_size,
                "Cylinder Made in": cylinder_made_in_s,
                "Pouch size": pouch_size,
                "Pouch Open Size": pouch_open_size,
                "Cylinder Bill No": cylinder_bill_no,
                "Cylinder Date": cylinder_date,
                "Prpc Sell": prpc_sell,
                "Job Status": job_status
            }            
            
            for i, r in required_filed.items():
                print(i,r)
                if not r:
                    messages.error(
                        request,
                        f"This {i} Filed Was Required",
                        extra_tags="custom-danger-style",
                    )
                    return redirect("job_entry")

            if new_party_name:
                party_name = new_party_name

            if cylinder_made_in_s:
                for value in cylinder_made_in_s:
                    if CylinderMadeIn.objects.filter(cylinder_made_in__iexact=value).exists():
                        pass
                    else:
                        CylinderMadeIn.objects.create(
                            cylinder_made_in=value
                        )
          
                    
            party_details, _ = Party.objects.get_or_create(
                party_name=party_name.strip() if party_name.strip() else "None"
            )
            for i in range(len(job_name)):
                job = Job_detail.objects.create(
                    date=date,
                    bill_no=bill_no,
                    party_details=party_details,
                    job_name=job_name[i],
                    job_type=job_type[i],
                    noc=noc[i],
                    prpc_sell=prpc_sell[i],
                    prpc_purchase=prpc_purchase[i],
                    cylinder_size=cylinder_size[i],
                    cylinder_made_in=cylinder_made_in_s[i],
                    pouch_size=pouch_size[i],
                    pouch_open_size=pouch_open_size[i],
                    pouch_combination=pouch_combination[i],
                    correction=correction,
                    job_status=job_status,
                    cylinder_date=cylinder_date[i],
                    cylinder_bill_no=cylinder_bill_no[i],
                )
                files_for_this_job = request.FILES.getlist(f"files[{i}][]")
                file_dic = utils.file_name_convert(files_for_this_job)
                
                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]
                    
                    Jobimage.objects.create(job=job, image=file_obj)

                job.save()
            messages.success(request, "New job Add Successfully")
            return redirect("dashboard_page")
    except Exception as e:
        messages.error(request, f"Something went wrong {e}")
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        return redirect("job_entry")
    

@custom_login_required
def update_job(request, update_id):
    try:
        if request.method == "POST":
            date = request.POST.get("date")
            bill_no = request.POST.get("bill_no")
            

            job_type = request.POST.get("job_type", "")
            noc = request.POST.get("noc")
            prpc_purchase = request.POST.get("prpc_purchase")
            prpc_sell = request.POST.get("prpc_sell")
            cylinder_size = request.POST.get("cylinder_size")
            cylinder_made_in = request.POST.get("cylinder_made_in")
            cylinder_date = request.POST.get("cylinder_date")
            cylinder_bill_no = request.POST.get("cylinder_bill_no")
            pouch_size = request.POST.get("pouch_size")
            pouch_open_size = request.POST.get("pouch_open_size")
           
            pouch_combination1 = request.POST.get("pouch_combination1")
            pouch_combination2 = request.POST.get("pouch_combination2")
            pouch_combination3 = request.POST.get("pouch_combination3")
            pouch_combination4 = request.POST.get("pouch_combination4")
            correction = request.POST.get("correction")
            job_status = request.POST.get("job_status")
            files = request.FILES.getlist("files")
            pouch_combination = f"{pouch_combination1} + {pouch_combination2} + {pouch_combination3} + {pouch_combination4}"
            

  

        required_filed = {
            "Date": date,
            "Bill no": bill_no,
         
            "job type": job_type,
            "Noc": noc,
            "Prpc Purchase": prpc_purchase,
            "Cylinder Size": cylinder_size,
            "Cylinder Made in": cylinder_made_in,
            "Pouch size": pouch_size,
            "Pouch Open Size": pouch_open_size,
            "Cylinder Bill No": cylinder_bill_no,
            "Cylinder Date": cylinder_date,
            "Prpc Sell": prpc_sell,
        }
        for i, r in required_filed.items():
            if not r:
                messages.error(
                    request,
                    f"This {i} field is required.",
                    extra_tags="custom-danger-style",
                )
                return redirect("dashboard_page")

       

    
        file_error = utils.file_validation(files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-danger-style")
            return redirect("dashboard_page")

        get_data = Job_detail.objects.all().get(id=update_id)
        get_combinations = get_data.pouch_combination.replace(" ", "").split("+")
        while len(get_combinations) < 4:
            get_combinations.append("")
      
        file_dic = utils.file_name_convert(files)
        try:
            old_job = Job_detail.objects.get(id=update_id)
            update_job_data = get_object_or_404(Job_detail, id=update_id)
            job = old_job
            for field in [
                "job_status",
                "cylinder_bill_no",
                "correction",
                "cylinder_size",
                "prpc_sell",
                "prpc_purchase",
                "noc",
                "job_type",
                "job_name",
             
                "bill_no",
                "pouch_open_size",
                "pouch_size",
                "cylinder_made_in",
                "cylinder_date",
                "date",
                
            ]:
                old_value = getattr(old_job, field)
                new_value = request.POST.get(field)
                if str(old_value) != new_value:
                    JobHistory.objects.create(
                        job=job,
                        field_name=field,
                        old_value=old_value,
                        new_value=new_value,
                        chnage_user=request.user,
                    )
                    setattr(job, field, new_value)
            job.save()
            update_job_data.date = date
            update_job_data.bill_no = bill_no
            
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
            update_job_data.cylinder_date = cylinder_date
            update_job_data.job_status = job_status
            update_job_data.pouch_combination = pouch_combination
            
            for file_key, file_data in file_dic.items():
                file_obj = file_data[1]
                Jobimage.objects.create(job=update_job_data, image=file_obj)
            update_job_data.save()
            messages.success(request, "Job Update successfully ")
            return redirect("dashboard_page")
        except Exception as e:
            messages.warning(request, f"Something went wrong try again {e}")
            return redirect("dashboard_page")

    except Exception as e:
        messages.error(request, f"Something went wrong try again {e}")
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        return redirect("dashboard_page")


@custom_login_required
def user_logout(request):
    try:
        logout(request)
        request.session.clear()
        return redirect("login_page")
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        messages.warning(request, f"Something went Wrong try again {e}")
        return redirect("dashboard_page")


@custom_login_required
def profile_page(request):
    return render(request, "profile.html")


@custom_login_required
def update_profile(request, users_id):
    try:
        update_profile = get_object_or_404(Registration, id=users_id)
        if request.method == "POST":
            first_name = request.POST.get("first_name")
            last_name = request.POST.get("last_name")
            username = request.POST.get("username")
            email = request.POST.get("email")
            
        required_filed = {
            "First Name": first_name,
            "Last Name": last_name,
            "Email": email,
            "Username": username,
        }

        for filed, required in required_filed.items():
            if not required:
                messages.error(
                    request, f"{filed} is Required", extra_tags="custom-danger-style"
                )
                return redirect("profile_page")

        if email != update_profile.email:
            email_check_error = utils.email_check(email)
            if email_check_error:
                messages.error(
                    request, email_check_error, extra_tags="custom-danger-style"
                )
                return redirect("profile_page")

        if (
            username != update_profile.username
            and Registration.objects.filter(username=username).exists()
        ):
            messages.error(
                request, "Username already exists", extra_tags="custom-danger-style"
            )
            return redirect("profile_page")

        email_error = utils.email_validator(email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("profile_page")
        update_profile.username = username
        update_profile.last_name = last_name
        update_profile.first_name = first_name
        update_profile.email = email
        update_profile.save()
        messages.success(
            request,
            "Profile Will Updated",
        )
        return redirect("profile_page")
    except Exception:
        messages.error(request, "Something went wrong  try again")
        logger.warning("something went wrong in User Profile")
        return redirect("profile_page")


@custom_login_required
def user_password(request):
    try:

        if request.method == "POST":
            old_password = request.POST.get("old_password", "").strip()
            new_password = request.POST.get("new_password", "").strip()
            confirm_password = request.POST.get("confirm_password", "").strip()

            if old_password == "" or old_password == None:
                error = "Please provide old Password."
                return render(request, "profile.html", context={"error": error})

            user_password = request.user
            if not user_password.check_password(old_password):
                messages.error(
                    request,
                    "old Password is Incorrect",
                    extra_tags="custom-danger-style",
                )
                return redirect("profile_page")

            if new_password == "" or new_password == None:
                errors = "Please provide New Password."
                return render(request, "profile.html", context={"errors": errors})

            password_error = utils.validator_password(new_password)
            if password_error:
                messages.error(
                    request, password_error, extra_tags="custom-danger-style"
                )
                return redirect("profile_page")

            if old_password == new_password:
                messages.error(
                    request,
                    "Your Current Password or New Password will same Add some Different",
                    extra_tags="custom-danger-style",
                )
                return redirect("profile_page")

            if new_password != confirm_password:
                messages.error(
                    request,
                    "new password or confirm Passwords Must be same ",
                    extra_tags="custom-danger-style",
                )
                return redirect("profile_page")

            user_password.set_password(new_password)
            user_password.save()

            return redirect("login_page")
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        messages.warning(request, "Something went wrong")
        return redirect("profile_page")


@custom_login_required
def cdr_page(request):
    search = request.GET.get("search", "").strip()
    date = request.GET.get("date", "").strip()
    end_date = request.GET.get("end_date", "").strip()
    party_name_sorting = request.GET.get("party_name_sorting", "")
    job_name_sorting = request.GET.get("job_name_sorting", "")
    date_sorting = request.GET.get("date_sorting", "")
    sorting = request.GET.get("sorting", "")
    
    
    cdr_data = CDRDetail.objects.all()
    if search and date:
        cdr_data = CDRDetail.objects.filter(
            Q(date__range=(date, end_date)) &
            (
                Q(job_name__icontains=search) |
                Q(party_details__party_name__icontains=search)
            )
        )
    elif date and end_date:
        cdr_data = CDRDetail.objects.filter(date__range=(date, end_date))

    elif end_date and date and search:
        cdr_data = CDRDetail.objects.filter(date__range=(date, end_date)) & (
            Q(job_name__icontains=search)
            | Q(party_details__party_name__icontains=search)
        )
   
    elif search:
        cdr_data = CDRDetail.objects.filter(
            Q(job_name__icontains=search)
            | Q(party_details__party_name__icontains=search)
        )
    elif date:
        cdr_data = CDRDetail.objects.filter(Q(date__icontains=date))


    order_by = ""
    if party_name_sorting == "asc":
        order_by = "party_details"
    elif party_name_sorting == "desc":
        order_by = "-party_details"
    elif job_name_sorting == "asc":
        order_by = "job_name"
    elif job_name_sorting == "desc":
        order_by = "-job_name"
    elif date_sorting == "asc":
        order_by = "date"
    elif date_sorting == "desc":
        order_by = "-date"
    elif sorting == "desc":
        order_by = "-id"

    if order_by:
        cdr_data = cdr_data.order_by(order_by)
    else:
        cdr_data = cdr_data.order_by("date","id")

    paginator = Paginator(cdr_data, 3)
    page_number = request.GET.get("page")

    party_names = Party.objects.values("party_name").distinct()
    cdr_job_names = CDRDetail.objects.values("job_name").distinct()

    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages
   
    context = {
        
        "cdr_details": page_obj,
        "page_range": page_range_placeholder,
        "search": search,
        "date": date,
        "end_date": end_date,
        "party_names": party_names,
        "cdr_job_names": cdr_job_names,
    }
       
    return render(request, "CDR/cdr_page.html", context)


@custom_login_required
def cdr_add(request):
    if request.method == "POST":
        party_name = request.POST.get("party_name","").strip()
        party_email = request.POST.get("party_email","").strip()
        cdr_upload_date = request.POST.get("cdr_upload_date","").strip()
        cdr_files = request.FILES.getlist("cdr_files","")
        job_name = request.POST.get("job_name","").strip()
        cdr_corrections_data = request.POST.get("cdr_corrections")
        new_party_name = request.POST.get("new_party_name","").strip()
        new_party_email = request.POST.get("new_party_email","").strip()
        new_job_name = request.POST.get("new_job_name","").strip()
        party_contact_used = request.POST.get("party_contact_used","").strip()
        new_party_contact = request.POST.get("new_party_contact","").strip()
        
        
        required_fields = {
            "Party Name": party_name,
            "Party Email": party_email,
            "Upload Date": cdr_upload_date,
            "Job Name": job_name,
        }

        

        for field, required in required_fields.items():
            if not required:
                messages.error(
                    request, f"{field} is Required", extra_tags="custom-danger-style"
                )
                return redirect("company_add_page")
            
        if not cdr_files:
            messages.error(
                request, "CDR File is Required", extra_tags="custom-danger-style")
            return redirect("company_add_page")

        if new_job_name != "":
            job_name = new_job_name
            
        if new_party_contact != "":
            party_contact_used = new_party_contact
            
        if new_party_email != "":
            party_email = new_party_email
            
        if new_party_name != "":
            party_name = new_party_name
            
            party_name_exists = Party.objects.filter(
                party_name__iexact=party_name
            ).exists()
            if party_name_exists:
                messages.error(
                    request,
                    "This Party Name is already exists.",
                    extra_tags="custom-danger-style",
                )
                return redirect("company_add_page")
        
        party_number_check = utils.phone_number_check(party_contact_used)
        if party_number_check:
            messages.error(
                request, party_number_check, extra_tags="custom-danger-style"
            )
            return redirect("company_add_page")
            
            
        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("company_add_page")
        
    
        file_error = utils.file_validation(cdr_files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-danger-style")
            return redirect("company_add_page")
        file_dic = utils.file_name_convert(cdr_files)

        try:
            party_details, _ = Party.objects.get_or_create(
                party_name=party_name.strip() if party_name.strip() else "None"
            )

            email_obj, _ = PartyEmail.objects.get_or_create(
                party=party_details,
                email=party_email
            )
            
            contact_obj, _ = PartyContact.objects.get_or_create(
                party=party_details,
                party_number=party_contact_used
            )
            
            
            cdr_data = CDRDetail.objects.create(
                date=cdr_upload_date,
                party_email_used = email_obj,
                party_details=party_details,
                cdr_corrections=cdr_corrections_data,
                job_name=job_name,
                party_contact_used= contact_obj )

            for file_key, file_data in file_dic.items():
                file_obj = file_data[1]
                CDRImage.objects.create(cdr=cdr_data, image=file_obj)

            cdr_data.save()
            messages.success(request, "CDR Upload Successfully ")
            return redirect("company_add_page")
        except Exception as e:
            logger.error(f"Something went wrong: {str(e)}", exc_info=True)
            messages.error(request, f"Something went wrong {e}")
            return redirect("company_add_page")
        

@custom_login_required
def cdr_delete(request, delete_id):
    delete = get_object_or_404(CDRDetail, id=delete_id)
    
    delete_image = delete.cdr_images.all()
    for img in delete_image:
        path = img.image.path
        
        if os.path.isfile(path):
            os.remove(path)
        else:
            img.delete()
    delete.delete()
    messages.success(request, "Data Delete successfully")
    return redirect("company_add_page")


@custom_login_required
def cdr_update(request, update_id):
    id = update_id
    if request.method == "POST":
        date = request.POST.get("cdr_upload_date")

        party_email = request.POST.get("party_email", "").strip()
        party_number = request.POST.get("party_number", "").strip()
        cdr_files = request.FILES.getlist("files")
        job_names = request.POST.get("job_name").strip()
        
        cdr_corrections = request.POST.get("cdr_corrections")

        
      
        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("company_add_page")
        

        file_error = utils.file_validation(cdr_files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-danger-style")
            return redirect("job_entry")

        file_dic = utils.file_name_convert(cdr_files)

        party_email = str(party_email).strip()

        update_details = get_object_or_404(CDRDetail, id=id)
        
        # Party Email Uniqueness Check
        party_id = update_details.party_details.id
        email_exists = PartyEmail.objects.filter(
            party=party_id, email=party_email
        ).exclude(id=update_details.party_email_used.id).exists()
        if email_exists:
            messages.error(
                request,
                "This email is already exists.",
                extra_tags="custom-danger-style",
            )
            return redirect("company_add_page")
        
      
        contact_exists = PartyContact.objects.filter(
            party=party_id, party_number=party_number
        ).exclude(id=update_details.party_contact_used.id).exists()
        if contact_exists:
            messages.error(
                request,
                "This contact number is already exists.",
                extra_tags="custom-danger-style",
            )
            return redirect("company_add_page")
        
        
         
        
        update_details.cdr_corrections = cdr_corrections
        update_details.job_name = job_names
        update_details.date = date
        update_details.save()
        
        update_details.party_email_used.email = party_email
        update_details.party_email_used.save()
        
        
        update_details.party_contact_used.party_number = party_number
        update_details.party_contact_used.save()

        for file_key, file_data in file_dic.items():
            file_obj = file_data[1]
            CDRImage.objects.create(cdr=update_details, image=file_obj) 
        
        messages.success(request, "CDR Updated Successfully")
        return redirect("company_add_page")
    return redirect("company_add_page")


def offline_page(request):
    return render(request, "Base/offline_page.html")


@custom_login_required
def cdr_sendmail_data(request):

    if request.method == "POST":
        date = request.POST.get("date", "")
        cdr_party_name = request.POST.get("cdr_party_name", "")
        cdr_party_address = request.POST.get("cdr_party_address", "")
        attachments = request.FILES.getlist("attachment")
        cdr_job_name = request.POST.get("cdr_job_name", "")
        cdr_corrections = request.POST.get("cdr_corrections", "")
        cdr_notes = request.POST.get("notes", "")
        correction_check = request.POST.get("correction_check", "")
        cdr_date_check = request.POST.get("cdr_date_check")

        if cdr_date_check == None or cdr_date_check == "":
            date = ""
        else:
            date = date
        if correction_check == None or correction_check == "":
            cdr_corrections = ""
        else:
            cdr_corrections = cdr_corrections

        total_attachment_size = sum(f.size for f in attachments)
        email_attachment_check = utils.email_attachment_size(total_attachment_size)
        if email_attachment_check:
            messages.error(request, email_attachment_check, extra_tags="custom-danger-style")
            return redirect("company_add_page")


        email_error = utils.email_validator(cdr_party_address)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("company_add_page")

        CDR_INFO = {
            "date": date,
            "Party_Email": cdr_party_address,
            "Party_Name": cdr_party_name,
            "cdr_job_name": cdr_job_name,
            "cdr_corrections": cdr_corrections,
            "notes": cdr_notes,
        }

        receiver_email = cdr_party_address
        template_name = "Base/cdr_email.html"
        convert_to_html_content = render_to_string(
            template_name=template_name, context=CDR_INFO
        )
        email = EmailMultiAlternatives(
            subject=f"CDR Details {cdr_job_name}",
            body="plain_message",
            from_email="soniyuvraj9499@gmail.com",
            to=[receiver_email],
        )
        email.attach_alternative(convert_to_html_content, "text/html")
        for i in attachments:
            email.attach(i.name, i.read(), i.content_type)
        email.send()
        messages.success(request, "Mail Send successfully")
        return redirect("company_add_page")
        # return render(request, 'Base/cdr_email.html',context=CDR_INFO)
    return redirect("company_add_page")


@custom_login_required
def send_mail_data(request):
    if request.method == "POST":
        date_check = request.POST.get("date_check")
        date = request.POST.get("date", "")
        bill_no = request.POST.get("bill_no", "")
        party_name = request.POST.get("party_name", "")
        party_email_address = request.POST.get("party_email_address")
        job_name = request.POST.get("job_name", "")
        noc = request.POST.get("noc", "")
        prpc_sell_check = request.POST.get("prpc_sell_check", "")
        prpc_sell = request.POST.get("prpc_sell", "")
        cylinder_size = request.POST.get("cylinder_size", "")
        pouch_size = request.POST.get("pouch_size", "")
        pouch_open_size = request.POST.get("pouch_open_size", "")
        correction = request.POST.get("correction", "")
        correction_check = request.POST.get("correction_check", "")
        attachments = request.FILES.getlist("attachment")
        note = request.POST.get("notes", "")
    if date_check == None or date_check == "":
        date = ""
    else:
        date = date

    if correction_check == None or correction_check == "":
        correction = ""
    else:
        correction = correction

    if prpc_sell_check == None or prpc_sell_check == "":
        prpc_sell = ""
    else:
        prpc_sell = prpc_sell

    if party_email_address == "" or party_email_address == None:
        messages.error(
            request, "Kindly provide Company email", extra_tags="custom-danger-style"
        )
        return redirect("dashboard_page")

    email_error = utils.email_validator(party_email_address)
    if email_error:
        messages.error(request, email_error, extra_tags="custom-danger-style")
        return redirect("dashboard_page")

    total_attachment_size = sum(f.size for f in attachments)
    
    
    
    email_attachment_check = utils.email_attachment_size(total_attachment_size)
    if email_attachment_check:
        messages.error(request, email_attachment_check, extra_tags="custom-danger-style")
        return redirect("dashboard_page")



    job_info = {
        "date": date,
        "bill_no": bill_no,
        "party_name": party_name,
        "party_email_address": party_email_address,
        "job_name": job_name,
        "noc": noc,
        "prpc_sell": prpc_sell,
        "cylinder_size": cylinder_size,
        "pouch_size": pouch_size,
        "pouch_open_size": pouch_open_size,
        "correction": correction,
        "note": note,
    }
    

    receiver_email = party_email_address
    template_name = "Base/send_email.html"
    convert_to_html_content = render_to_string(
        template_name=template_name, context=job_info
    )
    email = EmailMultiAlternatives(
        subject=f"Job Details {job_name}",
        body="plain_message",
        from_email='soniyuvraj949@gmail.com',
        to=[receiver_email],
    )
    email.attach_alternative(convert_to_html_content, "text/html")
    for i in attachments:
        email.attach(i.name, i.read(), i.content_type)
    email.send()

    messages.success(request, "Mail Send successfully")
    return redirect("dashboard_page")
    


@require_GET
@custom_login_required
def cdr_page_ajax(request):
    party_name = request.GET.get("party_name", "")
    
    if party_name:
        jobs = utils.all_job_name_list(party_name)
        jobs = list(jobs)
        email = list(Party.objects.filter(party_name=party_name).values('party_emails__email').distinct())
        contacts = list(
            Party.objects
            .filter(party_name=party_name)
            .values('party_contacts__party_number')
            .distinct()
        )
        
        
       
        return JsonResponse({"email": email, "jobs": jobs, "contact":contacts})
    return JsonResponse({"error": "Invalid request"}, status=400)


@require_GET
@custom_login_required
def job_page_ajax(request):
    party_name = request.GET.get("party_name", "")

    if party_name:
        jobs = utils.all_job_name_list(party_name)
        
        jobs = list(jobs) 
        
        return JsonResponse({"jobs": jobs})
    return JsonResponse({"error": "Invalid request"}, status=400)



@custom_login_required
def ProformaInvoicePage(request):
    party_name_list = Party.objects.values("party_name").distinct()
    job_name = list(Job_detail.objects.values("job_name").distinct())
    bank_details = BankDetails.objects.all()
    states = ProformaInvoice.INDIAN_STATES
    invoice_status = ProformaInvoice.Invoice_Status
   
    
    context = {
        "party_name_list": party_name_list,
        "states": states,
        "invoice_status": invoice_status,
        "bank_details": bank_details,
        "job_names":job_name,
    }
    return render(
        request, "ProformaInvoice/proforma_invoice_page.html", context=context
    )


def ViewProformaInvoice(request):
    
    proformaInvoice = (
        ProformaInvoice.objects.prefetch_related("bank_details", "job_details")
        .all()
        .order_by("invoice_status", "invoice_date")
    )
    
    
    date_sorting = request.GET.get("invoice_date_sorting", "")
    start_date = request.GET.get("start_date", "")
    end_date = request.GET.get("end_date", "")
    select_company = request.GET.get("select_company", "")
    states = ProformaInvoice.INDIAN_STATES
    invoice_status = ProformaInvoice.Invoice_Status
    
    if date_sorting == "asc":
        proformaInvoice = proformaInvoice.order_by("invoice_date")
    elif date_sorting == "desc":
        proformaInvoice = proformaInvoice.order_by("-invoice_date")
        

    if select_company and start_date and end_date:
        proformaInvoice = proformaInvoice.filter(
            Q(invoice_date__range=[start_date, end_date])
            & Q(party_details__icontains=select_company)
        )
    
    elif select_company and start_date:

        proformaInvoice = proformaInvoice.filter(
            Q(invoice_date__icontains=start_date)
            & Q(party_details__party_name__icontains=select_company)
        )

    elif start_date and end_date and select_company:
        proformaInvoice = proformaInvoice.filter(
            invoice_date__range=[start_date, end_date]
        ) & Q(party_details__party_name__icontains=select_company)
    elif start_date and end_date.strip():

        proformaInvoice = proformaInvoice.filter(
            invoice_date__range=[start_date, end_date]
        )
    elif start_date.strip():
        proformaInvoice = proformaInvoice.filter(Q(invoice_date__icontains=start_date))
    elif select_company.strip():
        proformaInvoice = proformaInvoice.filter(
        party_details__party_name__icontains=select_company
        )

                    
    party_name = Party.objects.values('party_name').distinct()
    
    P = Paginator(proformaInvoice, 10)
    page = request.GET.get("page")
    proformaInvoice = P.get_page(page)
    nums = "a" * proformaInvoice.paginator.num_pages

    try:
        for proforma in proformaInvoice:
            gst_value = str(proforma.gst).strip()
            gst_value = re.sub(r"\s+", "", gst_value)
            gst_value = gst_value.replace("'", '"')

            proforma.gst = json.loads(gst_value)
    except (json.JSONDecodeError, TypeError):
        cleaned = gst_value.replace("[", "").replace("]", "").replace('"', "")
        proforma.gst = [x for x in cleaned.split(",") if x]

    
    if not proformaInvoice:
        messages.error(request,"No data available",extra_tags="custom-danger-style")
       
    context = {
        "nums": nums,
        "proformaInvoices": proformaInvoice,
        "party_name": party_name,
        "states": states,
        "invoice_status": invoice_status,
    }
    return render(
        request, "ProformaInvoice/view_proforma_invoice.html", context=context
    )



@custom_login_required
def ProformaSendMail(request):
    if request.method == "POST":
        party_email = request.POST.get("party_email", "")
        fields_to_send_mail = [
            "invoice_no",
            "invoice_date",
            "party_name",
            "party_email",
            "party_contact",
            "billing_address",
            "billing_state_name",
            "billing_gstin_no",
            "total",
            "account_name",
            "bank_name",
            "bank_account_number",
            "bank_brnach_address",
            "bank_ifsc_code",
            "term_note",
            "gst",
            "total_in_words",
            "total_taxable_value",
            "gst_value",
            "mode_payment",
        ]
        if party_email == None or party_email == "":
            messages.error(
                request, "Company email is Required", extra_tags="custom-danger-style"
            )
            return redirect("view_proforma_invoice")

        

        item_dic = {}
        for field in fields_to_send_mail:
            field_value = request.POST.get(field, "")
            if field_value:
                item_dic[field] = field_value
          
        job_names = request.POST.getlist("job_name[]")
        titles = request.POST.getlist("title[]")
        quantities = request.POST.getlist("quantity[]")
        pouch_sizes = request.POST.getlist("pouch_open_size[]")
        cylinder_sizes = request.POST.getlist("cylinder_size[]")
        prpc_rates = request.POST.getlist("prpc_rate[]")
        taxable_value = request.POST.getlist("taxable_value[]")
        date = datetime.now().strftime("%Y-%m-%d")
        job_list = []
        for jn, tl, qt, ps, cs, pr, tx in zip(
            job_names,
            titles,
            quantities,
            pouch_sizes,
            cylinder_sizes,
            prpc_rates,
            taxable_value,
        ):
            job_list.append(
                {
                    "job_name": jn,
                    "title": tl,
                    "quantity": qt,
                    "pouch_open_size": ps,
                    "cylinder_size": cs,
                    "prpc_rate": pr,
                    "taxable_value": tx,
                }
            )
        item_dic["jobs"] = job_list
        
        item_dic["date"] = date

        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("view_proforma_invoice")

        receiver_email = party_email
        template_name = "Base/proforma_send_mail.html"
        convert_to_html_content = render_to_string(
            template_name=template_name, context={"data": item_dic}
        )
        email = EmailMultiAlternatives(
            subject=f"Proforma Details",
            body="plain message",
            from_email="soniyuvraj9499@gmail.com",
            to=[receiver_email],
        )
        email.attach_alternative(convert_to_html_content, "text/html")
        email.send()
        messages.success(request, "mail send successfully")
        return redirect("view_proforma_invoice")

    return redirect("proforma_sendmail")


@custom_login_required
def DeleteProformaInvoice(request, proforma_id):
    if request.method == "POST":
   
        item = get_object_or_404(ProformaInvoice, id=proforma_id)
        
        item.delete()
        messages.success(request, "Proforma Invoice Deleted Successfully")
        return redirect("view_proforma_invoice")
    return redirect("view_proforma_invoice")


@custom_login_required
def ProformaInvoiceCreate(request):
    if request.method == "POST":
        invoice_no = request.POST.get("invoice_no", "").strip()
        invoice_date = request.POST.get("invoice_date", "").strip()
        mode_payment = request.POST.get("mode_payment", "").strip()
        party_name = request.POST.get("party_name", "").strip()
        party_contact = request.POST.get("party_contact", "").strip()
        party_email = request.POST.get("party_email", "").strip()
        billing_address = request.POST.get("billing_address", "").strip()
        billing_state_name = request.POST.get("billing_state_name", "").strip()
        billing_gstin_no = request.POST.get("billing_gstin_no", "").strip()
        terms = request.POST.get("terms", "").strip()
        totals = request.POST.get("total_amount", "").strip()
        banking_details = request.POST.get("bank_details", "").strip()
        new_party_name = request.POST.get("new_party_name", "").strip()

        title = request.POST.getlist("title[]")
        job_names = request.POST.getlist("job_name")

        quantities = request.POST.getlist("quantity[]")
        pouch_open_sizes = request.POST.getlist("pouch_open_size[]")
        cylinder_sizes = request.POST.getlist("cylinder_size[]")
        prpc_price = request.POST.getlist("prpc_price[]")
        gst_list = request.POST.getlist("gst[]")
        gst_value = request.POST.get("gst_value")
        taxable_value = request.POST.get("taxable_value")
        invoice_status = request.POST.get("invoice_status")

        
        required_fields = {
            "invoice no": invoice_no,
            "invoice date": invoice_date,
            "mode payment": mode_payment,
            "party name": party_name,
            "company contact": party_contact,
            "company email": party_email,
            "billing address": billing_address,
            "billing state_name": billing_state_name,
            "billing GST in no": billing_gstin_no,
            "terms": terms,
            "totals": totals,
            "banking details": banking_details,
            "gst value": gst_value,
            "taxable value": taxable_value,
        }
        
        for field, required in required_fields.items():
            if not required:
                messages.error(
                    request, f"{field} is Required", extra_tags="custom-danger-style"
                )
                return redirect("proforma_invoice_page")
        
        
        if party_name == "" or new_party_name != "":
            party_name = new_party_name.strip()  
            party_name_exists = Party.objects.filter(
                party_name__iexact=party_name
            ).exists()
            if party_name_exists:
                messages.error(
                    request,
                    "This Party Name is already exists.",
                    extra_tags="custom-danger-style",
                )
                return redirect("proforma_invoice_page")
            
        party_number_check = utils.phone_number_check(party_contact)
        if party_number_check:
            messages.error(
                request, party_number_check, extra_tags="custom-danger-style"
            )
            return redirect("proforma_invoice_page")
        
        
        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("proforma_invoice_page")
        
        bank_instance = (
            BankDetails.objects.get(id=banking_details) if banking_details else None
        )
        
        if ProformaInvoice.objects.filter(invoice_no=invoice_no).exists():
            messages.error(
                request,
                "Invoice number already exists",
                extra_tags="custom-danger-style",
            )
            return redirect("proforma_invoice_page")

        try:
            
            party_details, _ = Party.objects.get_or_create(
                party_name=party_name.strip() if party_name else None
            )

         
            email_obj, _ = PartyEmail.objects.get_or_create(
                party=party_details,
                email=party_email
            ) 

           
            contact_obj, _ = PartyContact.objects.get_or_create(
                party=party_details,
                party_number=party_contact
            )

            proforma = ProformaInvoice.objects.create(
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                mode_payment=mode_payment,
                party_details=party_details,
                party_email_used=email_obj,
                party_contact_used=contact_obj,    
                billing_address=billing_address,
                billing_state_name=billing_state_name,
                billing_gstin_no=billing_gstin_no,  
                terms_note=terms,
                bank_details=bank_instance,
                gst=gst_list,
                total=totals,
                gst_value=gst_value,
                total_taxable_value=taxable_value,
                invoice_status=invoice_status,
            )

           
            for i in range(len(job_names)):
                ProformaJob.objects.create(
                    proforma_invoice=proforma,
                    title=title[i],
                    job_name=job_names[i],
                    quantity=quantities[i],
                    pouch_open_size=pouch_open_sizes[i],
                    cylinder_size=cylinder_sizes[i],
                    prpc_rate=prpc_price[i],
                )
            messages.success(request, "Proforma Invoice Created Successfully!")
            return redirect("proforma_invoice_page")
        except Exception as e:
            messages.warning(request, "Something went Wrong")
            return redirect("proforma_invoice_page")

    return redirect("proforma_invoice_page")


@require_GET
def ProformaInvoicePageAJAX(request):
    def safe_int(value, default=0):
        try:
            return int(value)
        except (TypeError, ValueError):
            return default

    def safe_float(value, default=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
    try:
        
        igst = request.GET.get("igsts")
        cgst = request.GET.get("cgsts")
        sgst = request.GET.get("sgsts")
        quantities = request.GET.getlist("quantities[]")
        prpc_prices = request.GET.getlist("prpc_prices[]")
        party_name = request.GET.get("party_name", "")

        igst_val = safe_int(igst)
        cgst_val = safe_int(cgst)
        sgst_val = safe_int(sgst)
        gst = igst_val + cgst_val + sgst_val

        
        quantities = [safe_float(q) for q in quantities if q not in (None, "", "0", 0)]
        prpc_prices = [safe_float(p) for p in prpc_prices if p not in (None, "", "0", 0)]

        taxable_value = sum(q * p for q, p in zip(quantities, prpc_prices))
        gst_amount = taxable_value * (gst / 100) if gst else 0
        total_amount = round(taxable_value + gst_amount, 2)
        job = []  
    
        billing_address = []
        party_contact_qs = []
        party_email_qs = []
        
        
        
    
        if party_name:
            
            jobs = utils.all_job_name_list(party_name)
            job = list(jobs)
            party_email_qs = list(Party.objects.filter(
                party_name=party_name
            ).values('party_emails__email').distinct())

            
            party_contact_qs = list(Party.objects.filter(
                party_name__iexact=party_name
            ).values("party_contacts__party_number").distinct())
                    
            billing_address_qs = ProformaInvoice.objects.filter(
                party_details__party_name__iexact=party_name
            ).values("billing_address").distinct()
            
            billing_address = (
                billing_address_qs[0]["billing_address"] if billing_address_qs else ""
            )
            
        context = {
            "total_amount": total_amount,
            "job": job, 
            "contacts": party_contact_qs,
            "emails": party_email_qs,
            "billing_address": billing_address,
            "taxable_value": taxable_value,
            "gst_amount": gst_amount,
        }
    except Exception as e:
        messages.error(request,f"Something went wrong try again ")
        logger.error(f"something went wrong {str(e)}",exc_info=True)
        return redirect("dashboard_page")

    
    return JsonResponse(context)



def quotation_page(request):
    
    
    party_names = Party.objects.values('party_name')
    pouch_types =  PouchQuotation.POUCH_TYPE
    
    if request.method == 'POST':
        if 'save_quotation' in request.POST:
            delivery_date =  request.POST.get('delivery_date')
            party_name = request.POST.get('party_name')
            job_name = request.POST.get('job_name')
            pouch_open_size = request.POST.get('pouch_size')
            pouch_combination = request.POST.get('pouch_combination')
            quantity = request.POST.get('quantity')
            purchase_rate_per_kg = request.POST.get('purchase_rate_per_kg')
            no_of_pouch_kg = request.POST.get('no_of_pouch_kg')
            per_pouch_rate_basic = request.POST.get('per_pouch_rate_basic')
            zipper_cost = request.POST.get('zipper_cost')
            final_rare = request.POST.get('final_rare')
            minium_quantity = request.POST.get('minium_quantity')
            pouch_type = request.POST.get('pouch_type')
            special_instruction = request.POST.get('special_instruction')
            delivery_address = request.POST.get('delivery_address')
            quantity_variation = request.POST.get('quantity_variation')
            freight = request.POST.get('freight')
            gst = request.POST.get('gst')
            note = request.POST.get('note')
            pouch_charge = request.POST.get('pouch_charge')
            
            
            party_details, _ = Party.objects.get_or_create(
                    party_name=party_name.strip() if party_name else None
                )

            required_fields = {
                "delivery_date":delivery_date,
                    "party_name":party_name,
                    "job_name":job_name,
                    "pouch_open_size":pouch_open_size,
                    "pouch_combination":pouch_combination,
                    "quantity":quantity,
                    "purchase_rate_per_kg":purchase_rate_per_kg,
                    "no_of_pouch_kg":no_of_pouch_kg,
                    "per_pouch_rate_basic":per_pouch_rate_basic,
                    "zipper_cost":zipper_cost,
                    "final_rare":final_rare,
                    "minium_quantity":minium_quantity,
                    "pouch_type":pouch_type,
                    "special_instruction":special_instruction,
                    "delivery_address":delivery_address,
                    "quantity_variation":quantity_variation,
                    
                                
            }
            for field, required in required_fields.items():
                if not required:
                    messages.error(
                        request, f"{field} is Required", extra_tags="custom-danger-style"
                    )
                    return redirect("quotation_page")
            
            
            

            pq = PouchQuotation.objects.create(
                delivery_date=delivery_date,
                party_details=party_details,
                job_name=job_name,
                pouch_open_size=pouch_open_size,
                pouch_combination=pouch_combination,
                quantity=quantity,
                pouch_charge=pouch_charge,
                purchase_rate_per_kg=purchase_rate_per_kg,
                no_of_pouch_kg=no_of_pouch_kg,
                per_pouch_rate_basic=per_pouch_rate_basic,
                zipper_cost=zipper_cost,
                final_rare=final_rare,
                minium_quantity=minium_quantity,
                pouch_type=pouch_type,
                special_instruction=special_instruction,
                delivery_address=delivery_address,
                quantity_variate=quantity_variation,
                freight=freight,
                gst=gst,
                note=note,    
            )
            pq.save()
            return redirect('quotation_page')
            
        
    context = {
        'pouch_types':pouch_types,
        'party_names':party_names
    }
    
    return render(request, "Quotation/quotation.html",context)


def quotation_page_htmxs(request):
    if request.headers.get("HX-Request"):
        purchase_rate = request.GET.get('purchase_rate') 
        purchase_rate_unit = request.GET.get('purchase_rate_unit')
        no_of_pouch_kg = float(request.GET.get('no_of_pouch_kg') or 1)  

        total_ppb = 0
        if purchase_rate_unit == 'polyester_printed_bug':
            total_ppb = float(purchase_rate)  / float(no_of_pouch_kg)
        elif purchase_rate == 'polyester_printed_roll':
            total_ppb = purchase_rate
            
        else :
            total_ppb = purchase_rate
        print(total_ppb)
        return HttpResponse(
                            { total_ppb}
        )
    return HttpResponse("")
        
    
        
        
        
        
        
        
    
        




