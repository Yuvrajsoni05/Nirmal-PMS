from .common_imports import *



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
                
                for file in file_dic:
                    Jobimage.objects.create(
                        job=job,
                        image=file
                    )

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
            update_job_data.save()
            for file in file_dic:   
                Jobimage.objects.create(
                    job=update_job_data,
                    image=file
                )
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
def delete_data(request, delete_id):
    try:
        if request.method == "POST":
            
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
        messages.warning(request, f"Something went wrong: {str(e)}")

        return redirect("dashboard_page")
    
    
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
    template_name = "Mail/job_mail.html"
    convert_to_html_content = render_to_string(
        template_name=template_name, context=job_info
    )
    email = EmailMultiAlternatives(
        subject=f"Job Details {job_name}",
        body="plain_message",
        from_email=os.environ.get('EMAIL_HOST_USER'),
        to=[receiver_email],
    )
    email.attach_alternative(convert_to_html_content, "text/html")
    for i in attachments:
        email.attach(i.name, i.read(), i.content_type)
    email.send()

    messages.success(request, "Mail Send successfully")
    return redirect("dashboard_page")


@custom_login_required
def job_page_ajax(request):
    party_name = request.GET.get("party_name", "")

    if party_name:
        jobs = utils.all_job_name_list(party_name)
        
        jobs = list(jobs) 
        
        return JsonResponse({"jobs": jobs})
    return JsonResponse({"error": "Invalid request"}, status=400)



    