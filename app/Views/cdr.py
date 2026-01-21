
from .common_imports import *



@custom_login_required
def cdr_page(request):
    search = request.GET.get("search", "").strip()
    date = request.GET.get("date", "").strip()
    end_date = request.GET.get("end_date", "").strip()
    party_name_sorting = request.GET.get("party_name_sorting", "")
    job_name_sorting = request.GET.get("job_name_sorting", "")
    date_sorting = request.GET.get("date_sorting", "")
    sorting = request.GET.get("sorting", "")
    

    if request.method == "POST":
        if "cdr_print" in request.POST:
            cdr_id = request.POST.get("cdr_id", "").strip()
            if cdr_id:
                cdr_data = CDRDetail.objects.get(id=cdr_id)
            
            return render(request, "includes/cdr_page/print.html", context={"cdr_details": cdr_data})
            
        

    
    filters = Q()

    if search:
        filters &= Q(job_name__icontains=search) | Q(party_details__party_name__icontains=search)

    if date and end_date:
        filters &= Q(date__range=[date, end_date])
    elif date:
        filters &= Q(date__icontains=date)

    cdr_data = CDRDetail.objects.filter(filters)


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

    paginator = Paginator(cdr_data, 10)
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
        cdr_files = request.FILES.getlist("cdr_files")
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
                return redirect("cdr_page")
            
        if not cdr_files:
            messages.error(
                request, "CDR File is Required", extra_tags="custom-danger-style")
            return redirect("cdr_page")

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
                return redirect("cdr_page")
        
        party_number_check = utils.phone_number_check(party_contact_used)
        if party_number_check:
            messages.error(
                request, party_number_check, extra_tags="custom-danger-style"
            )
            return redirect("cdr_page")
            
            
        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("cdr_page")
        
    
        file_error = utils.file_validation(cdr_files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-danger-style")
            return redirect("cdr_page")
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

            for file in file_dic:
                
                CDRImage.objects.create(cdr=cdr_data, image=file)

            cdr_data.save()
            messages.success(request, "CDR Upload Successfully ")
            return redirect("cdr_page")
        except Exception as e:
            logger.error(f"Something went wrong: {str(e)}", exc_info=True)
            messages.error(request, f"Something went wrong {e}")
            return redirect("cdr_page")
        
        
@custom_login_required
def cdr_update(request, update_id):
    id = update_id
    if request.method == "POST":
        date = request.POST.get("cdr_upload_date")

        party_email = request.POST.get("party_email", "").strip()
        party_number = request.POST.get("party_number", "").strip()
        cdr_files = request.FILES.getlist("files")
        job_names = request.POST.get("job_name", "").strip()
        
        cdr_corrections = request.POST.get("cdr_corrections")

        
      
        email_error = utils.email_validator(party_email)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("cdr_page")
        

        file_error = utils.file_validation(cdr_files)
        if file_error:
            messages.error(request, file_error, extra_tags="custom-danger-style")
            return redirect("cdr_page")
        file_dic = utils.file_name_convert(cdr_files)
        party_email = str(party_email).strip()
        update_details = get_object_or_404(CDRDetail, id=id)
        
        
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
            return redirect("cdr_page")
        
      
        contact_exists = PartyContact.objects.filter(
            party=party_id, party_number=party_number
        ).exclude(id=update_details.party_contact_used.id).exists()
        if contact_exists:
            messages.error(
                request,
                "This contact number is already exists.",
                extra_tags="custom-danger-style")
            return redirect("cdr_page")
        update_details.cdr_corrections = cdr_corrections
        update_details.job_name = job_names
        update_details.date = date
        update_details.save()
        update_details.party_email_used.email = party_email
        update_details.party_email_used.save()
        update_details.party_contact_used.party_number = party_number
        update_details.party_contact_used.save()
      
        for file_obj in file_dic:
            CDRImage.objects.create(cdr=update_details, image=file_obj) 

        messages.success(request, "CDR Updated Successfully")
        return redirect("cdr_page")
    return redirect("cdr_page")



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
    messages.success(request, "CDR Data Delete successfully")
    return redirect("cdr_page")


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
            return redirect("cdr_page")


        email_error = utils.email_validator(cdr_party_address)
        if email_error:
            messages.error(request, email_error, extra_tags="custom-danger-style")
            return redirect("cdr_page")

        CDR_INFO = {
            "date": date,
            "Party_Email": cdr_party_address,
            "Party_Name": cdr_party_name,
            "cdr_job_name": cdr_job_name,
            "cdr_corrections": cdr_corrections,
            "notes": cdr_notes,
        }

        receiver_email = cdr_party_address
        template_name = "Mail/cdr_mail.html"
        convert_to_html_content = render_to_string(
            template_name=template_name, context=CDR_INFO
        )
        email = EmailMultiAlternatives(
            subject=f"CDR Details {cdr_job_name}",
            body="plain_message",
            from_email= os.environ.get('EMAIL_HOST_USER'),
            to=[receiver_email],
        )
        email.attach_alternative(convert_to_html_content, "text/html")
        for i in attachments:
            email.attach(i.name, i.read(), i.content_type)
        email.send()
        messages.success(request, "Mail Send successfully")
        return redirect("cdr_page")
      
    return redirect("cdr_page")




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
