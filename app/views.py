from calendar import c
import json
import logging

import os
import re
from datetime import datetime


import requests
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import (PasswordResetConfirmView,PasswordResetDoneView,PasswordResetView)

from dotenv import load_dotenv
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
                messages.success(request, f"You are signed in {user.username} ")
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


        if request.method == "POST":
            if "job_print" in request.POST:
                job_id = request.POST.get("job_id","").strip()
                if job_id:
                    job_data = Job_detail.objects.get(id=job_id)
                return render(request,"includes/dashboard_page/print.html",context={"job_data":job_data})
        
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
        # for i in job_details:
        #     print(i)
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


def offline_page(request):
    return render(request, "Base/offline_page.html")









        