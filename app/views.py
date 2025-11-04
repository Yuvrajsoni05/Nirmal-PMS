from ast import Import
from calendar import c
from ctypes import util
import email
from email.mime import image
from genericpath import isfile
from io import BytesIO
from math import nan
from multiprocessing import context
from pydoc import pager
from traceback import print_tb
from PIL import Image
from django.views.decorators.http import require_GET
from django.db import utils
from pyparsing import C
from regex import P




from app.templatetags import custom_tags
from app.utils import email_check, file_name_convert

from numpy import size
from rest_framework.serializers import Serializer, ValidationError
from django.test import RequestFactory
from rest_framework import serializers, status
import random
from urllib import response

from django.shortcuts import get_object_or_404, render, redirect
import pandas as pd
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import cache_control, never_cache
from django.db.models.signals import pre_delete
from django.template.context_processors import request
from django.views.generic import TemplateView
from datetime import date, datetime, timedelta
from django.core.files.base import ContentFile

from app.models import CDRDetail, Job_detail, ProformaInvoice
from app.serializers import CDRDataSerializer, JobDetailSerializer, JobUpdateSerializer
from .models import *
from django.contrib import messages, sessions
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
import requests

import json
from decimal import Decimal
from django.core.paginator import Paginator

from django.contrib.sessions.models import Session
from django.utils.timezone import now
from django.template.loader import render_to_string
from django.utils.html import strip_tags
import logging

from django.db.models import Q
from django.db.models import Sum
from django.forms import fields
from django.core.exceptions import ObjectDoesNotExist




# mail
from django.core.mail import send_mail
from django.http import JsonResponse
from django.core.mail import EmailMultiAlternatives
import re

from django.core.mail import EmailMessage
from .decorators import *
from django.core.files import File

# Password

from django.urls import path, reverse_lazy
from django.contrib.auth.views import PasswordResetDoneView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
import os


# Swagger Setting

from . import utils

# Create your views here.


# urlpatterns = [
#     urls(r'^$', schema_view)
# ]


# Lecco ai
# Cookies in  Django Section in django


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


logger = logging.getLogger("myapp")

def login_page(request):
    try:
        if request.method == "POST":
            username_email = request.POST.get("username", "").strip()
            password = request.POST.get("password", "").strip()
            remember_me = request.POST.get("remember_me", "").strip()

            valid = re.fullmatch(
                r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", username_email
            )
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
                    extra_tags="custom-success-style",
                )
                return redirect("register_page")

        if Registration.objects.filter(username=username).exists():
            messages.error(
                request, "Username Already Exist", extra_tags="custom-success-style"
            )
            return redirect("register_page")

        email_error = utils.email_validator(email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-success-style")
            return redirect("register_page")

        email_check_error = utils.email_check(email)
        if email_check_error:
            messages.error(
                request, email_check_error, extra_tags="custom-success-style"
            )
            return redirect("register_page")

        password_error = utils.validator_password(password)
        if password_error:
            messages.error(request, password_error, extra_tags="custom-success-style")
            if password != confirm_password:
                messages.error(
                    request,
                    "Password Confirm Password must be same",
                    extra_tags="custom-success-style",
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
                        extra_tags="custom-success-style",
                    )
                    return redirect("edit_user_page")

            email_error = email_error = utils.email_validator(email)
            if email_error:
                messages.error(request, email_error, extra_tags="custom-success-style")
                return redirect("edit_user_page")

            if (
                username != update_user.username
                and Registration.objects.filter(username=username).exists()
            ):
                messages.error(
                    request,
                    "Username already exists.",
                    extra_tags="custom-success-style",
                )
                return redirect("edit_user_page")

            if (
                email != update_user.email
                and Registration.objects.filter(email=email).exists()
            ):
                messages.error(
                    request, "Email already exists.", extra_tags="custom-success-style"
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
                        extra_tags="custom-success-style",
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
                # print(session_data)
                if str(session_data.get("_auth_user_id")) == str(logout_user.id):
                    session.delete()
            update_user.save()
            messages.success(request, "User updated successfully.")
            return redirect("edit_user_page")
    except Exception as e:
        print(e)
        messages.error(
            request, f"Something went wrong", extra_tags="custom-success-style"
        )
        return redirect("edit_user_page")


@custom_login_required
def dashboard_page(request):
    try:
        get_q = request.GET.get("q", "")
        date_s = request.GET.get("date", "")
        date_e = request.GET.get("end_date", "")
        sorting = request.GET.get("sorting", "")
        date_sorting = request.GET.get("date_sorting", "")
        company_name_sorting = request.GET.get("company_name_sorting", "")
        job_name_sorting = request.GET.get("job_name_sorting", "")
        cylinder_date_sorting = request.GET.get("cylinder_date_sorting", "")
        cylinder_made_in_sorting = request.GET.get("cylinder_made_in_sorting", "")

        db_sqlite3 = Job_detail.objects.all()

        filters = Q()
        if get_q:
            filters &= (
                Q(job_name__icontains=get_q)
                | Q(company_name__icontains=get_q)
                | Q(cylinder_made_in__icontains=get_q)
            )
        if date_s and date_e:
            filters &= Q(date__range=[date_s, date_e])
        elif date_s:
            filters &= Q(date__icontains=date_s)
        elif date_e:
            filters &= Q(date__icontains=date_e)
        db_sqlite3 = Job_detail.objects.filter(filters)
        job_status = Job_detail.objects.values("job_status").distinct()
        if job_name_sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("job_name")
        elif job_name_sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-job_name")
        elif date_sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("date")
        elif date_sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-date")
        elif cylinder_date_sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("cylinder_date")
        elif cylinder_date_sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-cylinder_date")
        elif company_name_sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("company_name")
        elif company_name_sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-company_name")
        elif cylinder_made_in_sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("cylinder_made_in")
        elif cylinder_made_in_sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-cylinder_made_in")
        elif sorting == "asc":
            db_sqlite3 = db_sqlite3.order_by("id")
        elif sorting == "desc":
            db_sqlite3 = db_sqlite3.order_by("-id")
        else:
            db_sqlite3 = db_sqlite3.order_by("-job_status", "date")
        p = Paginator(db_sqlite3, 10)
        page = request.GET.get("page")
        datas = p.get_page(page)
        total_job = db_sqlite3.count()
        company_name = CompanyName.objects.all().order_by("company_name")
        count_of_company = company_name.count()

        cylinder_company_names = CylinderMadeIn.objects.all()
        total_active_job = Job_detail.objects.filter(job_status="In Progress").count()
        count_of_cylinder_company = cylinder_company_names.count()
        nums = " " * datas.paginator.num_pages

           
        context = {
            "nums": nums,
            "venues": datas,
            "total_job": total_job,
            "company_name": company_name,
            "cylinder_company_names": cylinder_company_names,
            "count_of_company": count_of_company,
            "count_of_cylinder_company": count_of_cylinder_company,
            # 'total_sales':total_sales,
            "datas": datas,
            # 'total_purchase':total_purchase,
            "sorting": sorting,
            "company_name_sorting": company_name_sorting,
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
    print(delete_id)
    try:
        folder_url = Job_detail.objects.values_list("folder_url", flat=True).get(id=delete_id)


        print(delete_id)
        if folder_url and folder_url != 'nan':
            try:
                print(folder_url)
                url = os.environ.get("DELETE_WEBHOOK_JOB")
                print(url)
                response = requests.delete(f"{url}{delete_id}")
                
                messages.success(request, "Job Deleted successfully ")
                return redirect("dashboard_page")
            except Exception as e:
                messages.warning(request, "Something went wrong try again")
                logger.error(f"Something went wrong: {str(e)}", exc_info=True)
                return redirect("dashboard_page")
        else:
            delete_data = get_object_or_404(Job_detail, id=delete_id)
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
            messages.success(request, "Job Deleted successfully w")
            return redirect("dashboard_page")
    except Exception as e:
        logger.error(f"Something went wrong: {str(e)}", exc_info=True)
        messages.warning(request, "Something went Wrong", e)
        return redirect("dashboard_page")


@custom_login_required
def base_html(request):
    return render(request, "Base/base.html")


@custom_login_required
def job_entry(request):

    company_name = CompanyName.objects.values("company_name").union(
        CDRDetail.objects.values("company_name")
    )

    cylinder_company_names = CylinderMadeIn.objects.all()
    cdr_job_name = CDRDetail.objects.values("job_name").distinct()
    context = {
        "company_name": company_name,
        "cylinder_company_names": cylinder_company_names,
        "cdr_job_name": cdr_job_name,
    }
    return render(request, "job_entry.html", context)


@custom_login_required
def add_job(request):

    try:
        if request.method == "POST":
            date = request.POST.get("job_date")
            bill_no = request.POST.get("bill_no").strip()
            company_name = request.POST.get("company_name", "").strip()
            job_name = request.POST.get("job_name")
            new_job_name = request.POST.get("new_job_name", "").strip()
            job_type = request.POST.get("job_type").strip()
            noc = request.POST.get("noc").strip()
            prpc_purchase = request.POST.get("prpc_purchase").strip()
            prpc_sell = request.POST.get("prpc_sell").strip()
            cylinder_size = request.POST.get("cylinder_size").strip()
            cylinder_made_in_s = request.POST.get("cylinder_select").strip()
            cylinder_date = request.POST.get("cylinder_date")
            cylinder_bill_no = request.POST.get("cylinder_bill_no").strip()
            pouch_size = request.POST.get("pouch_size")
            pouch_open_size = request.POST.get("pouch_open_size")
            pouch_combination_1 = request.POST.get("pouch_combination1").strip()
            pouch_combination_2 = request.POST.get("pouch_combination2").strip()
            pouch_combination_3 = request.POST.get("pouch_combination3").strip()
            pouch_combination_4 = request.POST.get("pouch_combination4").strip()
            new_company = request.POST.get("new_company")
            new_cylinder_company_name = request.POST.get(
                "cylinder_made_in_company_name"
            )
            correction = request.POST.get("correction")
            job_status = request.POST.get("job_status")
            files = request.FILES.getlist("files")
            
            
            
            
            
            pouch_combination = f"{pouch_combination_1} + {pouch_combination_2} + {pouch_combination_3} + {pouch_combination_4}"
            
            required_filed = {
                "Date": date,
                "Bill no": bill_no,
                "Company_Name": company_name,
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
            }
            for i, r in required_filed.items():
                if not r:
                    messages.error(
                        request,
                        f"This {r} Filed Was Required",
                        extra_tags="custom-success-style",
                    )
                    return redirect("job_entry")

            file_error = utils.file_validation(files)
            if file_error:
                messages.error(request, file_error, extra_tags="custom-success-style")
                return redirect("job_entry")

            file_dic = file_name_convert(files)

            
            print(file_dic)
            
            
            
            if new_job_name != "":
                if new_job_name == "" or new_job_name == None:
                    messages.error(request, "Plz Provide Job Name")
                    return redirect("data-entry")
                if Job_detail.objects.filter(job_name__icontains=new_job_name).exists():
                    messages.error(
                        request,
                        "Job Name Already Exists",
                        extra_tags="custom-success-style",
                    )
                    return redirect("job_entry")
                else:
                    job_name = new_job_name

            if Job_detail.objects.filter(
                job_name__icontains=job_name, date__icontains=date
            ).exists():
                messages.error(
                    request,
                    "Job Name are already Exists on this date kindly Update job",
                    extra_tags="custom-success-style",
                )
                return redirect("job_entry")

            if new_company != "":
                if CompanyName.objects.filter(
                    company_name__icontains=new_company
                ).exists():
                    messages.error(
                        request,
                        "Company Name Already Exists",
                        extra_tags="custom-success-style",
                    )
                    return redirect("job_entry")
                add_company = CompanyName.objects.create(company_name=new_company)
                add_company.save()
                company_name = new_company
            if company_name == "" or company_name == None:
                messages.error(request, "Plz Provide Company Name")
                return redirect("data-entry")

            if new_cylinder_company_name != "":
                if CylinderMadeIn.objects.filter(
                    cylinder_made_in__icontains=new_cylinder_company_name
                ).exists():
                    messages.error(
                        request,
                        "Company Name Already Exists",
                        extra_tags="custom-success-style",
                    )
                    return redirect("job_entry")
                add_new_cylinder_company = CylinderMadeIn.objects.create(
                    cylinder_made_in=new_cylinder_company_name
                )
                add_new_cylinder_company.save()
                cylinder_made_in_s = new_cylinder_company_name

            data = {
                "date": date,
                "bill_no": bill_no,
                "company_name": company_name,
                "job_type": job_type,
                "job_name": job_name,
                "noc": noc,
                "prpc_sell": prpc_sell,
                "prpc_purchase": prpc_purchase,
                "cylinder_size": cylinder_size,
                "cylinder_made_in": cylinder_made_in_s,
                "pouch_size": pouch_size,
                "pouch_open_size": pouch_open_size,
                "pouch_combination": pouch_combination,
                "correction": correction,
            }

        try:
            url = os.environ.get("CREATE_WEBHOOK_JOB")
            response = requests.post(f"{url}", data=data, files=file_dic)
            if response.status_code == 200:
                data_string = response.text
                data_dict = json.loads(data_string)
                id_number = data_dict["id"]
                cylinder_data = Job_detail.objects.all().get(id=id_number)
                cylinder_data.cylinder_date = cylinder_date
                cylinder_data.cylinder_bill_no = cylinder_bill_no
                cylinder_data.job_status = job_status
                cylinder_data.save()
                messages.success(request, "Job successfully Added")
                return redirect("dashboard_page")
            else:
                job_data = Job_detail.objects.create(
                    date=date,
                    bill_no=bill_no,
                    company_name=company_name,
                    job_name=job_name,
                    job_type=job_type,
                    noc=noc,
                    prpc_sell=prpc_sell,
                    prpc_purchase=prpc_purchase,
                    cylinder_size=cylinder_size,
                    cylinder_made_in=cylinder_made_in_s,
                    pouch_size=pouch_size,
                    pouch_open_size=pouch_open_size,
                    pouch_combination=pouch_combination,
                    correction=correction,
                    job_status=job_status,
                    cylinder_date=cylinder_date,
                    cylinder_bill_no=cylinder_bill_no,
                )
                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]
                    Jobimage.objects.create(job=job_data, image=file_obj)
                job_data.save()
                messages.success(request, "Data  successfully Add on sqlite 3")
                return redirect("dashboard_page")

        except Exception as e:
            logger.error(f"Something went wrong: {str(e)}", exc_info=True)
            job_data = Job_detail.objects.create(
                date=date,
                bill_no=bill_no,
                company_name=company_name,
                job_name=job_name,
                job_type=job_type,
                noc=noc,
                prpc_sell=prpc_sell,
                prpc_purchase=prpc_purchase,
                cylinder_size=cylinder_size,
                cylinder_made_in=cylinder_made_in_s,
                pouch_size=pouch_size,
                pouch_open_size=pouch_open_size,
                pouch_combination=pouch_combination,
                correction=correction,
                job_status=job_status,
                cylinder_date=cylinder_date,
                cylinder_bill_no=cylinder_bill_no,
            )
            for file_key, file_data in file_dic.items():
                file_obj = file_data[1]
                Jobimage.objects.create(job=job_data, image=file_obj)
            job_data.save()
            messages.success(request, "Data successfully Add ")
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
            company_name = request.POST.get("company_name")
            job_name = request.POST.get("job_name", "")
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
            # pouch_combination = request.POST.get('pouch_combination')
            pouch_combination1 = request.POST.get("pouch_combination1")
            pouch_combination2 = request.POST.get("pouch_combination2")
            pouch_combination3 = request.POST.get("pouch_combination3")
            pouch_combination4 = request.POST.get("pouch_combination4")
            correction = request.POST.get("correction")
            job_status = request.POST.get("job_status")
            files = request.FILES.getlist("files")
            pouch_combination = f"{pouch_combination1} + {pouch_combination2} + {pouch_combination3} + {pouch_combination4}"

        demo = Job_detail.objects.values("date").get(id=update_id)
        date_formatte = demo["date"].strftime("%Y-%m-%d")

        required_filed = {
            "Date": date,
            "Bill no": bill_no,
            "Company_Name": company_name,
            "job name": job_name,
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
                    extra_tags="custom-success-style",
                )
                return redirect("dashboard_page")

        jobs = Job_detail.objects.all().get(id=update_id)
        if job_name != jobs.job_name:
            messages.error(request, "You can't chnage job_name")
            return redirect("dashboard_page")

        if date != date_formatte:
            if Job_detail.objects.filter(date=date, job_name=job_name).exists():
                messages.error(
                    request,
                    "Job is Already exists from this date ",
                    extra_tags="custom-success-style",
                )
                return redirect("dashboard_page")

        file_error = utils.file_validation(files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-success-style")
            return redirect("dashboard_page")

        get_data = Job_detail.objects.all().get(id=update_id)
        get_combinations = get_data.pouch_combination.replace(" ", "").split("+")
        while len(get_combinations) < 4:
            get_combinations.append("")

        folder_id = get_data.folder_url

        file_dic = file_name_convert(files)
        url = os.environ.get("UPDATE_WEBHOOK_JOB")
        if folder_id:

            data = {
                "date": date,
                "bill_no": bill_no,
                "company_name": company_name,
                "job_type": job_type,
                "job_name": job_name,
                "noc": noc,
                "prpc_purchase": prpc_purchase,
                "prpc_sell": prpc_sell,
                "cylinder_size": cylinder_size,
                "cylinder_made_in": cylinder_made_in,
                "pouch_size": pouch_size,
                "pouch_open_size": pouch_open_size,
                "pouch_combination": pouch_combination,
                "correction": correction,
            }
            try:
                response = requests.post(f"{url}{update_id}", data=data, files=file_dic)
                if response.status_code == 200:
                    cylinder_data = Job_detail.objects.all().get(id=update_id)
                    cylinder_data.cylinder_date = cylinder_date
                    cylinder_data.cylinder_bill_no = cylinder_bill_no
                    cylinder_data.job_status = job_status
                    cylinder_data.save()
                    messages.success(
                        request,
                        "Data Updated successfully",
                    )
                    return redirect("dashboard_page")
                else:
                    messages.warning(request, "Your Credentials will Expire")
                    return redirect("dashboard_page")
            except Exception as e:
                logger.error(f"Something went wrong: {str(e)}", exc_info=True)
                messages.warning(request, "Your Credentials will Expire")
                return redirect("dashboard_page")
        else:
            try:
                old_job = Job_detail.objects.get(id=update_id)
                update_job_data = get_object_or_404(Job_detail, id=update_id)
                job = old_job
                print(old_job)
                for field in ['job_status', 'cylinder_bill_no', 'correction' , 'cylinder_size' , 'prpc_sell' , 'prpc_purchase' , 'noc' , 'job_type' , 'job_name', 'company_name' , 'bill_no'  , 'pouch_open_size' , 'pouch_size' , 'cylinder_made_in']:
                    
                    old_value = getattr(old_job, field)
                    new_value = request.POST.get(field)
                    print(f"{field} -  {old_value} -  {new_value}")
                    if old_value != new_value:

                        JobHistory.objects.create(
                            job=job,
                            field_name=field,
                            old_value=old_value,
                            new_value=new_value,
                            chnage_user=request.user
                        )
                        setattr(job, field, new_value)
                job.save()        

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
                update_job_data.cylinder_date = cylinder_date
                update_job_data.job_status = job_status
                update_job_data.pouch_combination = pouch_combination

                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]
                    Jobimage.objects.create(job=update_job_data, image=file_obj)
                update_job_data.save()
                messages.success(request, "Data Update successfully ")
                return redirect("dashboard_page")
            except Exception as e:
                print(e)
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
                    request, f"{filed} is Required", extra_tags="custom-success-style"
                )
                return redirect("profile_page")

        if email != update_profile.email:
            email_check_error = utils.email_check(email)
            if email_check_error:
                messages.error(
                    request, email_check_error, extra_tags="custom-success-style"
                )
                return redirect("profile_page")

        if (
            username != update_profile.username
            and Registration.objects.filter(username=username).exists()
        ):
            messages.error(
                request, "Username already exists", extra_tags="custom-success-style"
            )
            return redirect("profile_page")

        email_error = utils.email_validator(email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-success-style")
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
                    extra_tags="custom-success-style",
                )
                return redirect("profile_page")

            if new_password == "" or new_password == None:
                errors = "Please provide New Password."
                return render(request, "profile.html", context={"errors": errors})

            password_error = utils.validator_password(new_password)
            if password_error:
                messages.error(
                    request, password_error, extra_tags="custom-success-style"
                )
                return redirect("profile_page")

            if old_password == new_password:
                messages.error(
                    request,
                    "Your Current Password or New Password will same Add some Different",
                    extra_tags="custom-success-style",
                )
                return redirect("profile_page")

            if new_password != confirm_password:
                messages.error(
                    request,
                    "new password or confirm Passwords Must be same ",
                    extra_tags="custom-success-style",
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
    search = request.GET.get("search", " ").strip()
    date = request.GET.get("date", "").strip()
    end_date = request.GET.get("end_date", "").strip()
    # print(date)
    company_name_sorting = request.GET.get("company_name_sorting", "")
    job_name_sorting = request.GET.get("job_name_sorting", "")
    date_sorting = request.GET.get("date_sorting", "")
    sorting = request.GET.get("sorting", "")

    cdr_data = CDRDetail.objects.all()
    if search and date:
        cdr_data = CDRDetail.objects.filter(
            Q(date__icontains=date)
            & (
                Q(job_name__icontains=search)
                | Q(company_name__icontains=search)
                | Q(company_email__icontains=search)
            )
        )

    elif end_date and date:
        cdr_data = CDRDetail.objects.filter(date__range=(date, end_date))
    elif search:
        cdr_data = CDRDetail.objects.filter(
            Q(job_name__icontains=search)
            | Q(company_name__icontains=search)
            | Q(company_email__icontains=search)
        )
    elif date:
        cdr_data = CDRDetail.objects.filter(Q(date__icontains=date))
    elif end_date:
        cdr_data = CDRDetail.objects.filter(Q(date__icontains=end_date))

    order_by = ""
    if company_name_sorting == "asc":
        order_by = "company_name"
    elif company_name_sorting == "desc":
        order_by = "-company_name"
    elif job_name_sorting == "asc":
        order_by = "job_name"
    elif job_name_sorting == "desc":
        order_by = "-job_name"
    elif date_sorting == "asc":
        order_by = "date"
        print(cdr_data)
    elif date_sorting == "desc":
        order_by = "-date"
    elif sorting == "desc":
        order_by = "-id"

    if order_by:
        cdr_data = cdr_data.order_by(order_by)
    else:
        cdr_data = cdr_data.order_by("date")

    p = Paginator(cdr_data, 10)
    page = request.GET.get("page")
    cdr_emails = CDRDetail.objects.values("company_email").distinct()
    cdr_company_name = CDRDetail.objects.values("company_name").distinct()
    cdr_job_name = CDRDetail.objects.values("job_name").distinct()

    datas = p.get_page(page)
    nums = "a" * datas.paginator.num_pages
    context = {
        "nums": nums,
        "cdr_details": datas,
        "page_obj": datas,
        "search": search,
        "date": date,
        "end_date": end_date,
        "cdr_email": cdr_emails,
        "cdr_company_name": cdr_company_name,
        "cdr_job_names": cdr_job_name,
    }
    return render(request, "CDR/cdr_page.html", context)


@custom_login_required
def cdr_add(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name", "").strip()
        company_email = request.POST.get("company_email", "").strip()
        cdr_upload_date = request.POST.get("cdr_upload_date", "").strip()
        cdr_files = request.FILES.getlist("cdr_files", "")
        job_name = request.POST.get("job_name", "").strip()
        cdr_corrections_data = request.POST.get("cdr_corrections")
        new_company_name = request.POST.get("new_company_name", "").strip()
        new_company_email = request.POST.get("new_company_email", "").strip()
        new_job_name = request.POST.get("new_job_name", "").strip()

        if not job_name or not cdr_upload_date:
            messages.error(
                request,
                "Job name and upload date are required.",
                extra_tags="custom-error-style",
            )
            return redirect("company_add_page")

        if new_job_name != "":
            job_name = new_job_name

        if new_company_email != "":
            company_email = new_company_email

        if new_company_name != "":
            company_name = new_company_name

        required_fields = {
            "Company Name": company_name,
            "Company Email": company_email,
            "Upload Date": cdr_upload_date,
            "Job Name": job_name,
        }

        email_error = utils.email_validator(company_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-success-style")
            return redirect("company_add_page")

        for field, required in required_fields.items():
            if not required:
                messages.error(
                    request, f"{field} is Required", extra_tags="custom-success-style"
                )
                return redirect("company_add_page")

        if not cdr_files:
            messages.error(
                request, "CDR File is Required", extra_tags="custom-success-style"
            )
            return redirect("company_add_page")
        if len(cdr_files) > 2:
            messages.error(
                request, "You can upload only 2 files", extra_tags="custom-error-style"
            )
            return redirect("company_add_page")

        if CDRDetail.objects.filter(
            company_name=company_name, company_email=company_email
        ).exists():
            pass
        else:
            if CDRDetail.objects.filter(company_name=company_name).exists():
                messages.error(
                    request,
                    "Choose Another Company Name",
                    extra_tags="custom-success-style",
                )
                return redirect("company_add_page")
            if CDRDetail.objects.filter(company_email=company_email).exists():
                messages.error(
                    request, "Choose Another Email", extra_tags="custom-success-style"
                )
                return redirect("company_add_page")

        # Ensure company is added
        if CompanyName.objects.filter(company_name__icontains=company_name).exists():
            pass
        else:
            company_add_in = CompanyName.objects.create(company_name=company_name)
            company_add_in.save()

        if CDRDetail.objects.filter(
            job_name__icontains=job_name, date=cdr_upload_date
        ).exists():
            messages.error(
                request,
                "Job Name already exists on this date. Kindly update job.",
                extra_tags="custom-success-style",
            )
            return redirect("company_add_page")

        data = {
            "company_name": company_name,
            "company_email": company_email,
            "cdr_upload_date": cdr_upload_date,
            "job_name": job_name,
            "cdr_corrections": cdr_corrections_data,
        }

        uarl = os.environ.get("CREATE_WEBHOOK_CDR")
       
        if url:
            
            file_dic = file_name_convert(cdr_files)
            print(file_dic)
            url = os.environ.get("CREATE_WEBHOOK_CDR")
            response = requests.post(f"{url}", data=data, files=file_dic)
            if response.status_code == 200:
                print("Positive Response : ", response)
                messages.success(request, "CDR Upload Successfully ")
                return redirect("company_add_page")

            else:
                cdr_data = CDRDetail.objects.create(
                    date=cdr_upload_date,
                    company_name=company_name,
                    company_email=company_email,
                    cdr_corrections=cdr_corrections_data,
                    job_name=job_name,
                )
                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]
                    CDRImage.objects.create(
                        cdr=cdr_data, image=file_obj
                    )
                    
                cdr_data.save()
                messages.success(request, "CDR Upload Successfully SQLite DB")
                return redirect("company_add_page")

              
                
                


@custom_login_required
def cdr_delete(request, delete_id):
    url = os.environ.get("DELETE_WEBHOOK_CDR")
    folder_url = CDRDetail.objects.get(id=delete_id).file_url
    print(folder_url)
    if folder_url:
        response = requests.delete(f"{url}{delete_id}")
        if response.status_code == 200:
            messages.success(request, "CDR File Deleted successfully ")
            return redirect("company_add_page")
        else:
            messages.warning(request, "Your Credentials will Expire")
            return redirect("company_add_page")

    else:
        delete = get_object_or_404(CDRDetail, id=delete_id)
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
        messages.success(request, "Data Delete successfully")
        return redirect("company_add_page")




@custom_login_required
def cdr_update(request, update_id):

    id = update_id
    if request.method == "POST":
        date = request.POST.get("cdr_upload_date")

        company_email = request.POST.get("company_email", "").strip()
        cdr_files = request.FILES.getlist("files")
        company_name = request.POST.get("company_name").strip()
        job_names = request.POST.get("job_name").strip()

        cdr_corrections = request.POST.get("cdr_corrections")

        get_date = CDRDetail.objects.values("date").get(id=id)
        date_formatte = get_date["date"].strftime("%Y-%m-%d")

        if CDRDetail.objects.filter(
            company_name__icontains=company_name, company_email=company_email
        ).exists():
            pass
        else:
            if CDRDetail.objects.filter(
                company_email__icontains=company_email
            ).exists():
                messages.error(
                    request, "Choose Another Email", extra_tags="custom-success-style"
                )
                return redirect("company_add_page")

        if date != date_formatte:
            if CDRDetail.objects.filter(
                job_name__icontains=job_names, date=date
            ).exists():
                messages.error(
                    request,
                    "CDR Job Name are already Exists on this date kindly Update job",
                    extra_tags="custom-success-style",
                )
                return redirect("company_add_page")

        file_error = utils.file_validation(cdr_files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-success-style")
            return redirect("job_entry")

        file_dic = file_name_convert(cdr_files)

        company_email = str(company_email).strip()
        print(company_email)

        get_email = CDRDetail.objects.values_list("company_email").get(id=id)
        email_string = get_email[0]
        print(str(email_string))

        if company_email == email_string:
            pass
        else:
            CDRDetail.objects.filter(company_email=email_string).update(
                company_email=company_email
            )
        url = os.environ.get("UPDATE_WEBHOOK_CDR")
        if not cdr_files:
            update_details = get_object_or_404(CDRDetail, id=id)
            update_details.company_email = company_email
            update_details.cdr_corrections = cdr_corrections
            update_details.job_name = job_names
            update_details.date = date
            update_details.save()
            messages.success(request, "CDR Data Updated")
            return redirect("company_add_page")
        else:
            get_folder_url = CDRDetail.objects.values_list("file_url").get(id=id)
            folder_url = get_folder_url[0]
            if folder_url:
                data = {
                    "date": date,
                    "company_email": company_email,
                    "company_name": company_name,
                    "job_name": job_names,
                    "cdr_corrections": cdr_corrections,
                }
                response = requests.post(f"{url}{id}", data=data, files=file_dic)

                if response.status_code == 200:
                    messages.success(request, "Data Update Successfully")
                    return redirect("company_add_page")
                else:
                    messages.warning(request, "Your Credentials will Expire")
                    return redirect("company_add_page")
            else:
                update_details = get_object_or_404(CDRDetail, id=id)
                update_details.company_email = company_email
                update_details.cdr_corrections = cdr_corrections
                update_details.job_name = job_names
                update_details.date = date
                
                for file_key, file_data in file_dic.items():
                    file_obj = file_data[1]
                    CDRImage.objects.create(cdr=update_details, image=file_obj)
                update_details.save()
                messages.success(request, "Data Updated Successfully")
                return redirect("company_add_page")

    return redirect("company_add_page")


def offline_page(request):
    return render(request, "Base/offline_page.html")





@custom_login_required
def cdr_sendmail_data(request):

    if request.method == "POST":
        date = request.POST.get("date", " ")
        cdr_company_name = request.POST.get("cdr_company_name", " ")
        cdr_company_address = request.POST.get("cdr_company_address", " ")
        attachments = request.FILES.getlist("attachment")
        cdr_job_name = request.POST.get("cdr_job_name", " ")
        cdr_corrections = request.POST.get("cdr_corrections", " ")
        cdr_notes = request.POST.get("notes", " ")
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
        MAX_SIZE_MB = 25
        if total_attachment_size > MAX_SIZE_MB * 1024 * 1024:
            messages.error(
                request,
                f"Total file size exceeds {MAX_SIZE_MB}MB. Please upload smaller files.",
                extra_tags="custom-success-style",
            )
            return redirect("company_add_page")

        email_error = utils.email_validator(cdr_company_address)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-success-style")
            return redirect("company_add_page")

        CDR_INFO = {
            "date": date,
            "Company_Email": cdr_company_address,
            "Company_Name": cdr_company_name,
            "cdr_job_name": cdr_job_name,
            "cdr_corrections": cdr_corrections,
            "notes": cdr_notes,
        }

        receiver_email = cdr_company_address
        template_name = "Base/cdr_email.html"
        convert_to_html_content = render_to_string(
            template_name=template_name, context=CDR_INFO
        )
        email = EmailMultiAlternatives(
            subject="Mail From Nirmal Ventures",
            body="plain_message",
            from_email="Soniyuvraj9499@gmail.com",
            to=[receiver_email],
        )
        email.attach_alternative(convert_to_html_content, "text/html")
        for i in attachments:
            email.attach(i.name, i.read(), i.content_type)
        email.send()
        messages.success(request, "Mail Send successfully")
        return redirect("company_add_page")

    return redirect("company_add_page")


@custom_login_required
def send_mail_data(request):

    if request.method == "POST":
        date_check = request.POST.get("date_check")
        date = request.POST.get("date", "")
        bill_no = request.POST.get("bill_no", "")
        company_name = request.POST.get("company_name", "")
        company_email_address = request.POST.get("company_address")
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
        # selected_item = request.POST.getlist('select_item[]',"")

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

    if company_email_address == "" or company_email_address == None:
        messages.error(
            request, "Kindly provide Company email", extra_tags="custom-success-style"
        )
        return redirect("dashboard_page")

    email_error = utils.email_validator(company_email_address)
    if email_error:
        messages.error(request, email_error, extra_tags="custom-success-style")
        return redirect("dashboard_page")

    total_attachment_size = sum(f.size for f in attachments)

    MAX_SIZE_MB = 25
    if total_attachment_size > MAX_SIZE_MB * 1024 * 1024:
        messages.error(
            request,
            f"Total file size exceeds {MAX_SIZE_MB}MB. Please upload smaller files.",
            extra_tags="custom-success-style",
        )
        return redirect("dashboard_page")

    job_info = {
        "date": date,
        "bill_no": bill_no,
        "company_name": company_name,
        "company_email_address": company_email_address,
        "job_name": job_name,
        "noc": noc,
        "prpc_sell": prpc_sell,
        "cylinder_size": cylinder_size,
        "pouch_size": pouch_size,
        "pouch_open_size": pouch_open_size,
        "correction": correction,
        "note": note,
    }

    print(job_info)
    receiver_email = company_email_address
    template_name = "Base/send_email.html"
    convert_to_html_content = render_to_string(
        template_name=template_name, context=job_info
    )
    email = EmailMultiAlternatives(
        subject="Mail From Nirmal Ventures",
        body="plain_message",
        from_email=request.user.email,
        to=[receiver_email],
    )
    email.attach_alternative(convert_to_html_content, "text/html")
    for i in attachments:
        email.attach(i.name, i.read(), i.content_type)
    email.send()

    messages.success(request, "Mail Send successfully")
    return redirect("dashboard_page")

@custom_login_required
def company_name_suggestion(request):
    company_name = request.GET.get("company_name", "")
    if company_name:

        jobs = list(
            CDRDetail.objects.filter(company_name__iexact=company_name)
            .values("job_name")
            .distinct()
        )

        email = list(
            CDRDetail.objects.filter(company_name__iexact=company_name)
            .values("company_email")
            .distinct()
        )
        print(email)
        return JsonResponse({"email": email, "jobs": jobs})
    return JsonResponse({"error": "Invalid request"}, status=400)

@custom_login_required
def company_name_suggestion_job(request):
    company_name = request.GET.get("company_name", "")

    if company_name:
        jobs = list(
            Job_detail.objects.filter(company_name__iexact=company_name)
            .values("job_name")
            .distinct()
        )
        job_detail = (
            Job_detail.objects.filter(company_name__iexact=company_name)
            .values("job_name")
            .distinct()
        )
        cdr_job = (
            CDRDetail.objects.filter(company_name__iexact=company_name)
            .values("job_name")
            .distinct()
        )
        jobs = list(job_detail.union(cdr_job))

        return JsonResponse({"jobs": jobs})
    return JsonResponse({"error": "Invalid request"}, status=400)

@custom_login_required
def file_convert(images):
    valid_extension = [".jpeg", ".jpg", ".png", ".ai"]
    for i in images:
        print(i)
        ext = os.path.splitext(i.name)[1]
        if ext.lower() not in valid_extension:
            return {
                "Error": "Invalid file. Only .jpg, .jpeg, .png, and .ai are allowed."
            }
    return None

@custom_login_required
def cdr_job_check(job_name, date):
    if CDRDetail.objects.filter(job_name__icontains=job_name, date=date).exists():
        return {"Error": "Job Name already exists on this date. Kindly update job"}
    return None

@custom_login_required
def cdr_company_check(company_name, company_email):
    if CDRDetail.objects.filter(
        company_name=company_name, company_email=company_email
    ).exists():
        pass
    else:
        if CDRDetail.objects.filter(company_name=company_name).exists():
            return {"Error": "Choose Another Company Name"}
        if CDRDetail.objects.filter(company_email=company_email).exists():
            return {"Error": "Choose Another Email"}



@custom_login_required
def ProformaInvoicePage(request):
    company_list  = CompanyName.objects.values("company_name").distinct().union(
        ProformaInvoice.objects.values("company_name").distinct()
    )
    states = ProformaInvoice.INDIAN_STATES
    context = {"company_list":company_list,
               "states":states
    }
    return render(request, "ProformaInvoice/proforma_invoice_page.html",context=context)

def ViewProformaInvoice(request):
    proformaInvoice = ProformaInvoice.objects.all().order_by('invoice_date')
    company_name = ProformaInvoice.objects.values_list('company_name', flat=True).distinct()
    start_date = request.GET.get('start_date')
    end_date =  request.GET.get("end_date")
    select_company = request.GET.get('select_company',"")
    states = ProformaInvoice.INDIAN_STATES
    
    if start_date and end_date:
         proformaInvoice = proformaInvoice.filter(invoice_date__range=[start_date,end_date])
    
    if select_company and select_company.strip(): 
        proformaInvoice = proformaInvoice.filter(company_name__icontains=select_company.strip())
        
        
    P = Paginator(proformaInvoice,5)
    page = request.GET.get("page")
    proformaInvoice = P.get_page(page)  
    nums = "a" * proformaInvoice.paginator.num_pages
    
    try:
        for proforma in proformaInvoice:
            gst_value = str(proforma.gst).strip()
            gst_value = re.sub(r'\s+', '', gst_value)  
            gst_value = gst_value.replace("'", '"')
            
            proforma.gst = json.loads(gst_value)
    except (json.JSONDecodeError, TypeError): 
        cleaned = gst_value.replace("[", "").replace("]", "").replace('"', "")
        proforma.gst = [x for x in cleaned.split(",") if x]

        
    print(proforma.gst)
    context = {
        "nums" :nums,
        "proformaInvoices": proformaInvoice,
        "company_name":company_name,
        "states":states
    }
    return render(request, "ProformaInvoice/view_proforma_invoice.html",context=context)



def UpdateProformaInvoice(request,proforma_id):
    if request.method  == "POST":
        invoice_date = request.POST.get("invoice_date")
        mode_payment  = request.POST.get("mode_payment")
        billing_address = request.POST.get("billing_address")
        billing_gstin = request.POST.get("billing_gstin_no")
        billing_state_name = request.POST.get("billing_state_name")
        quantity = request.POST.get("quantity")
        pouch_open_size  = request.POST.get("pouch_open_size")
        cylinder_size = request.POST.get("cylinder_size")
        prpc_rate = request.POST.get("prpc_rate")
      
        total = request.POST.getlist("total")
        
        company_name = request.POST.get("company_name")
        company_email = request.POST.get("company_email")
        company_contact = request.POST.get("company_contact")
        title = request.POST.get("title")
        banking_details = request.POST.get("banking_details")
        
        
        
        print(invoice_date,mode_payment,billing_state_name,billing_address,billing_gstin,quantity,pouch_open_size,cylinder_size,prpc_rate,total,company_name,company_email,company_contact,title,banking_details)
        print(proforma_id)
        item = get_object_or_404(ProformaInvoice,id=proforma_id)
        item.invoice_date = invoice_date
        item.mode_payment = mode_payment
        item.billing_address = billing_address
        item.billing_state_name = billing_state_name
        item.billing_gstin_no = billing_gstin
        item.quantity = quantity
        item.pouch_open_size = pouch_open_size
        item.cylinder_size = cylinder_size
        item.prpc_rate = prpc_rate
        item.company_name = company_name
        item.company_email = company_email
        item.company_contact = company_contact
        item.title = title
        item.banking_details = banking_details
        item.save()
        messages.success(request,"Data  Successfully")
        return redirect('view_proforma_invoice')
    
        
        
        
    return redirect("view_proforma_invoice")
    

@custom_login_required
def DeleteProformaInvoice(request,proforma_id):
    if request.method == "POST":
        print(proforma_id)
        item = get_object_or_404(ProformaInvoice, id=proforma_id)
        print("Delete Request Received")
        item.delete()
        messages.success(request, "Proforma Invoice Deleted Successfully")
        return redirect("view_proforma_invoice")
    return redirect("view_proforma_invoice")
             
        
@custom_login_required
def ProformaInvoiceCreate(request):
    if request.method == "POST":
        invoice_no = request.POST.get("invoice_no","").strip()
        invoice_date = request.POST.get("invoice_date","").strip()
        mode_payment = request.POST.get("mode_payment","").strip()
        company_name = request.POST.get("company_name","").strip()
        company_contact = request.POST.get("company_contact","").strip()
        company_email = request.POST.get("company_email","").strip()
        billing_address = request.POST.get("billing_address","").strip()
        billing_state_name = request.POST.get("billing_state_name","").strip()
        billing_gstin_no = request.POST.get("billing_gstin_no","").strip()
        title = request.POST.get("title","").strip()
        
        job_name = request.POST.get("job_name","").strip()
        pouch_diameter = request.POST.get("pouch_diameter","").strip()
        pouch_height = request.POST.get("pouch_height","").strip()
        
        cylinder_diameter = request.POST.get("cylinder_diameter","").strip()
        cylinder_height = request.POST.get("cylinder_height","").strip()
        cylinder_size = f"{cylinder_diameter} x {cylinder_height}"
        pouch_open_size = f"{pouch_diameter} x {pouch_height}"

        
        prpc_price = request.POST.get("prpc_price","").strip()
        quantity = request.POST.get("quantity","").strip()
        gst = request.POST.getlist("gst[]")
        terms = request.POST.get("terms","").strip()
        total_amount = request.POST.get("total_amount","").strip()
        banking_details = request.POST.get("bank_details","").strip()
        new_company = request.POST.get("new_company","").strip()
        new_job = request.POST.get("new_job","").strip()
        
        
        if company_name == "" or new_company != "":
            company_name = new_company
        if job_name == "" or new_job != "":
            job_name = new_job
            
            
        for field_name, field_value in {
            "Invoice No": invoice_no,
            "Invoice Date": invoice_date,
            "Mode Payment": mode_payment,
            "Company Name": company_name,
            "Company Contact": company_contact,
            "Company Email": company_email,
            "Billing Address": billing_address,
            "Billing State Name": billing_state_name,
            "Billing GSTIN No": billing_gstin_no,
            "Title": title,
            "Job Name": job_name,
            "Pouch Open Size": pouch_open_size,
            "Cylinder Size": cylinder_size,
            "PRPC Price": prpc_price,
            "Quantity": quantity,
            "GST": gst,
            "Terms": terms,
            "Total Amount": total_amount,
            "Banking Details": banking_details,
        }.items():
            if not field_value:
                messages.error(
                    request,
                    f"{field_name} is Required",
                    extra_tags="custom-success-style",
                )
                return redirect("proforma_invoice_page")
            
            
        if ProformaInvoice.objects.filter(invoice_no=invoice_no).exists():
            messages.error(request,"Invoice number already exists",extra_tags="custom-success-style")
            return redirect("proforma_invoice_page")
        
        
        email_error = utils.email_validator(company_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-success-style")
            return redirect("proforma_invoice_page")
        if ProformaInvoice.objects.filter(company_name=company_name).exists():
            
            if ProformaInvoice.objects.filter(company_name=company_name, company_email=company_email, company_contact=company_contact).exists():
                pass
            else:
                messages.error(request,"You Can't Chnage Data ")
                return redirect("proforma_invoice_page")
        else:
            if ProformaInvoice.objects.filter(company_email=company_email).exists():
                messages.error(request,"Email already Exists",extra_tags="custom-success-style")
                return redirect("proforma_invoice_page")
            if ProformaInvoice.objects.filter(company_contact=company_contact).exists():
                messages.error(request,"Contact already Exists",extra_tags="custom-success-style")
                return redirect("proforma_invoice_page")
            
        try:    
            proforma_invoice = ProformaInvoice.objects.create(
                invoice_no=invoice_no,
                invoice_date=invoice_date,
                mode_payment=mode_payment,
                company_name=company_name,
                company_contact=company_contact,
                company_email=company_email,
                billing_address=billing_address,
                billing_state_name=billing_state_name,
                billing_gstin_no=billing_gstin_no,
                title=title,
                job_name=job_name,
                pouch_open_size=pouch_open_size,
                cylinder_size=cylinder_size,
                prpc_rate=prpc_price,
                quantity=quantity,
                gst=gst,
                terms_note=terms,
                banking_details=banking_details,
                total=total_amount,
            )
            proforma_invoice.save()
            messages.success(request, "Proforma Invoice Created Successfully")
            return redirect("proforma_invoice_page")
        except Exception as e:
            messages.warning(request, f"Something went wrong try again {e}")
     
            return redirect("proforma_invoice_page")
        
    return redirect("proforma_invoice_page")   

 
def ProformaInvoicePageAJAX(request):
    igst = request.GET.get('igsts')
    cgst = request.GET.get('cgsts')
    sgst = request.GET.get('sgsts')
    quantity = request.GET.get("quantity","0")
    prpc_price = request.GET.get("prpc_price","0")
    company_name = request.GET.get("company_name", "")
    if quantity == "" or prpc_price == "":
        quantity = 0
        prpc_price = 0
        
    gst = int(igst) + int(cgst) + int(sgst)
    
    quantity = float(quantity)
    prpc_price = float(prpc_price)
    base_amount = quantity * prpc_price
    gst_amount = base_amount * (gst/100)
    total_amount = base_amount + gst_amount
    
    total_amount = round(total_amount, 2)
    job = ""
    company_contact = ""
    company_email = ""
    billing_address = ""
    if company_name:
        job = list(
            ProformaInvoice.objects.filter(company_name__iexact=company_name)
            .values("job_name")
            .distinct()
            .union(
                CDRDetail.objects.filter(company_name__iexact=company_name)
                .values("job_name")
                .distinct()
            )
          .union(
                Job_detail.objects.filter(company_name__iexact=company_name)
                .values("job_name")
                .distinct()
            )
        )

        company_contact = list(ProformaInvoice.objects.filter(company_name__iexact=company_name).values("company_contact").distinct())
        
        company_email = list(ProformaInvoice.objects.filter(company_name__iexact=company_name).values("company_email").distinct().union(
            CDRDetail.objects.filter(company_name__iexact=company_name).values("company_email").distinct()
        ))
        
        billing_address = list(ProformaInvoice.objects.filter(company_name__iexact=company_name).values("billing_address").distinct())
    
        
        company_email = company_email[0]['company_email'] if company_email else ''
        company_contact = company_contact[0]['company_contact'] if company_contact else ''
        billing_address = billing_address[0]['billing_address'] if billing_address else ''
    else:
        company_name = ""
    
   
    context = {"total_amount": total_amount,
               "job":job,
               "company_contact":company_contact,
                "company_email":company_email,
                "billing_address":billing_address             
   
               }
    logger.debug(f"AJAX context: {context}")
   
    return JsonResponse(context)




# API OF ALL Views

from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response


class JobList(APIView):
    def get(self, request):
        if request.method == "GET":
            job = Job_detail.objects.all()
            serializer = JobDetailSerializer(job, many=True)
            return Response(serializer.data)

    def post(self, request):
        job_name = request.data.get("job_name")
        new_job = request.data.get("new_job_name")

        date = request.data.get("date")
        company_name = request.data.get("company_name")
        new_company = request.data.get("new_company")
        images = request.FILES.getlist("images")

        if company_name and new_company == "":
            return Response(
                {"Error": "Please provide company Name"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        valid_extension = [".jpeg", ".jpg", ".png", ".ai"]
        for i in images:
            ext = os.path.splitext(i.name)[1]
            if ext.lower() not in valid_extension:
                return Response(
                    {
                        "Error": "Invalid file  Only .jpg, .jpeg, .png and .ai are allowed."
                    },
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if Job_detail.objects.filter(date=date, job_name=job_name).exists():
            return Response(
                {
                    "Error": "Job Name already exists on this date. Kindly update the job."
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        if not company_name:

            company_name = new_company
            if CompanyName.objects.filter(
                company_name__icontains=company_name
            ).exists():
                return Response({"Error": "Company name already Exists"})
            add_company = CompanyName.objects.create(company_name=company_name)

        if not job_name:
            job_name = new_job

        file_dic = {}
        for i, file in enumerate(images):
            _, file_extension = os.path.splitext(file.name)
            random_number = random.randint(1, 100)
            new_file_name = f"{date}_{random_number}{file_extension}"

            file.name = new_file_name
            file_key = f"{new_file_name}"
            file_dic[file_key] = (file.name, file, file.content_type)

        mutable_data = request.data.copy()
        mutable_data["company_name"] = company_name
        mutable_data["job_name"] = job_name

        serializer = JobDetailSerializer(data=mutable_data)
        if serializer.is_valid():
            job_instance = serializer.save()
            for img_key, (filename, image, content_type) in file_dic.items():
                job_image = Jobimage.objects.create(job=job_instance, image=image)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobDetailAV(APIView):
    def get(self, request, pk):
        try:
            job = Job_detail.objects.get(pk=pk)

        except Job_detail.DoesNotExist:
            return Response(
                {"Error": "Job dose not exist"}, status=status.HTTP_404_NOT_FOUND
            )

        serializer = JobUpdateSerializer(job)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.method == "PUT":
            job = Job_detail.objects.get(pk=pk)
            demo = Job_detail.objects.values("date").get(id=pk)
            date_formatte = demo["date"].strftime("%Y-%m-%d")
            new_date = request.data.get("date")
            images = request.FILES.getlist("images")

            valid_extension = [".jpeg", ".jpg", ".png", ".ai"]
            for i in images:
                ext = os.path.splitext(i.name)[1]
                if ext.lower() not in valid_extension:
                    return Response(
                        {
                            "Error": "Invalid file  Only .jpg, .jpeg, .png and .ai are allowed."
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            file_dic = {}
            for i, file in enumerate(images):
                _, file_extension = os.path.splitext(file.name)
                random_number = random.randint(1, 100)
                new_file_name = f"{date}_{random_number}{file_extension}"
                file.name = new_file_name
                file_key = f"{new_file_name}"
                file_dic[file_key] = (file.name, file, file.content_type)

            if new_date != date_formatte:
                if Job_detail.objects.filter(date=new_date).exists():
                    return Response(
                        {"Error": "A job with the same date already exists."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            serializer = JobUpdateSerializer(job, data=request.data)
            if serializer.is_valid():
                job_instance = serializer.save()
                for img_key, (filename, image, content_type) in file_dic.items():
                    job_image = Jobimage.objects.create(job=job_instance, image=image)
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        if request.method == "DELETE":
            job = Job_detail.objects.get(pk=pk)
            delete_images = job.image.all()
            for img in delete_images:
                path = img.image.path
                if os.path.isfile(path):
                    os.remove(path)
                else:
                    img.delete()

            job.delete()
            return Response(
                {"success": "Job Deleted Successfully "}, status=status.HTTP_200_OK
            )


class CDRDetailAVS(APIView):
    serializer_class = CDRDataSerializer

    def get(self, request):
        if request.method == "GET":
            cdr = CDRDetail.objects.all()
            serializer = CDRDataSerializer(cdr, many=True)
            return Response(serializer.data)

    def post(self, request):
        job_name = request.data.get("job_name")
        images = request.FILES.getlist("images")
        date = request.data.get("date")
        company_name = request.data.get("company_name")
        company_email = request.data.get("company_email")

        print(images)
        image_error = file_convert(images)
        if image_error:
            return Response(image_error, status=status.HTTP_404_NOT_FOUND)

        job_error = cdr_job_check(job_name, date)
        if job_error:
            return Response(job_error, status=status.HTTP_400_BAD_REQUEST)

        company_name_error = cdr_company_check(company_name, company_email)
        if company_name_error:
            return Response(company_name_error, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():

            cdr_instance = serializer.save()

            for i in images:
                print("This Is I  ", i)
                filename = i.name
                size_limit = 2 * 1024 * 1024
                print(size_limit)
                file_size = i.size
                # thumbnail_file = None

                _, file_extension = os.path.splitext(i.name)
                random_number = random.randint(1, 100)
                new_file_name = f"{date}_{random_number}{file_extension}"
                i.name = new_file_name

                # if file_size > size_limit:
                #     img = Image.open(i)
                #     base, ext = os.path.splitext(new_file_name)
                #     print(base)
                #     quality = 80
                #     for f in range(10):
                #         io = BytesIO()
                #         img.save(io, format="WEBP", optimize=True, quality=quality)
                #         size = io.tell()
                #         print(size)
                #         print(f"This is Size of {size:2f}")

                #         if size <= size_limit:

                #             thumbnail_file = File(io, name=f"{base}_thumbnail{ext}")
                #             break
                #         quality -= 5
                # else:
                #     img = Image.open(i)
                #     io = BytesIO()
                #     img.save(io, format="WEBP", optimize=True, quality=40)
                #     io.seek(0)
                #     base, ext = os.path.splitext(filename)
                #     thumbnail_file = File(io, name=f"{base}_thumbnail{ext}")

                
                CDRImage.objects.create(
                    cdr=cdr_instance, image=i
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CDRUpdateView(APIView):
    def get(self, request, pk):
        try:
            cdr = CDRDetail.objects.get(pk=pk)
        except Exception as e:
            logger.error(f"Something went wrong: {str(e)}", exc_info=True)
            return Response({"error": "CDR Dose not exist"})
        serializer = CDRDataSerializer(cdr)
        return Response(serializer.data)

    def put(self, request, pk):
        if request.method == "PUT":
            cdr = CDRDetail.objects.get(pk=pk)
            date = CDRDetail.objects.values("date").get(pk=pk)
            date_formatte = date["date"].strftime("%Y-%m-%d")
            images = request.FILES.getlist("image")

            image_error = file_convert(images)
            if image_error:
                return Response({"error": image_error})

