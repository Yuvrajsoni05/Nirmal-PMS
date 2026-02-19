import json
import re
from .common_imports import *


@custom_login_required
def ProformaInvoiceCreate(request):
    if request.method == "POST":
        invoice_no = request.POST.get("invoice_no", "").strip()
        invoice_date = request.POST.get("invoice_date", "").strip()
        mode_payment = request.POST.get("mode_payment", "").strip()
        party_name = request.POST.get("party_name", "").strip()
        party_contact = request.POST.get("party_contact", "").strip()
        party_email = request.POST.get("party_email", "").strip()
        billing_address = request.POST.get("billing_address_select", "").strip()
        new_billing_address = request.POST.get("new_billing_address", "").strip()
   
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

        if billing_address == "" or new_billing_address != "":
            billing_address = new_billing_address.strip()
        print(billing_address)
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
            print(billing_address)
            billing_address_obj, _ = PartyBillingAddress.objects.get_or_create(
                party=party_details,
                billing_address=billing_address
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
                
                billing_state_name=billing_state_name,
                billing_gstin_no=billing_gstin_no,  
                terms_note=terms,
                bank_details=bank_instance,
                gst=gst_list,
                total=totals,
                gst_value=gst_value,
                total_taxable_value=taxable_value,
                invoice_status=invoice_status,
                party_billing_address_used=billing_address_obj,
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


@custom_login_required
def DeleteProformaInvoice(request, proforma_id):
    if request.method == "POST":
   
        item = get_object_or_404(ProformaInvoice, id=proforma_id)
        
        item.delete()
        messages.success(request, "Proforma Invoice Deleted Successfully")
        return redirect("view_proforma_invoice")
    return redirect("view_proforma_invoice")

@custom_login_required
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
            
            billing_address = list(Party.objects.filter(
                party_name__iexact=party_name,
            ).values("party_billing_addresses__billing_address").distinct())
            

        context = {
            "total_amount": total_amount,
            "job": job, 
            "contacts": party_contact_qs,
            "emails": party_email_qs,
            "billing_addresses": billing_address,
            "taxable_value": taxable_value,
            "gst_amount": gst_amount,
        }
    except Exception as e:
        messages.error(request,f"Something went wrong try again ")
        logger.error(f"something went wrong {str(e)}",exc_info=True)
        return redirect("dashboard_page") 
    return JsonResponse(context)

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
    

    if request.method == "POST":

        if 'print_proforma_invoice' in request.POST:
            proforma_id = request.POST.get("proforma_id")
            prforma_detail = ProformaInvoice.objects.get(id=proforma_id)
            jobs = prforma_detail.job_details.all()
            print(prforma_detail.terms_note)
            return render(
                request,
                "includes/proforma/print.html",
                context={"data": prforma_detail, "jobs": jobs},
            )
        
    party_id = request.GET.get("party_name", "")
    
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
    
    if party_id:
        proformaInvoice = proformaInvoice.filter(party_details__party_name__iexact=party_id)
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

    # try:
    #     for proforma in proformaInvoice:
    #         gst_value = str(proforma.gst).strip()
    #         gst_value = re.sub(r"\s+", "", gst_value)
    #         gst_value = gst_value.replace("'", '"')

    #         proforma.gst = json.loads(gst_value)
    # except (json.JSONDecodeError, TypeError):
    #     cleaned = gst_value.replace("[", "").replace("]", "").replace('"', "")
    #     proforma.gst = [x for x in cleaned.split(",") if x]

    
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
                request, "Email is Required", extra_tags="custom-danger-style"
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
        template_name = "Mail/proforma_mail.html"
        convert_to_html_content = render_to_string(
            template_name=template_name, context={"data": item_dic}
        )
        email = EmailMultiAlternatives(
            subject=f"Proforma Details",
            body="plain message",
            from_email= os.environ.get('EMAIL_HOST_USER'),
            to=[receiver_email],
        )
        email.attach_alternative(convert_to_html_content, "text/html")
        email.send()
        messages.success(request, "mail send successfully")
        return redirect("view_proforma_invoice")

    return redirect("proforma_sendmail")
