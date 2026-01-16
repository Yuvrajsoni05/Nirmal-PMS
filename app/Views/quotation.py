import email
from .common_imports import *


def quotation_page(request):
    
    
    party_names = PouchParty.objects.values('party_name')
    pouch_types =  PouchQuotationJob.POUCH_TYPE
    
    if request.method == 'POST':
        if 'save_quotation' in request.POST:
            pouch_quotation_number = request.POST.get('pouch_quotation_number')
            delivery_date = request.POST.get('delivery_date')
            party_name = request.POST.get('party_name')
            new_party_name = request.POST.get('new_party_name') or None
            quantity_variation = request.POST.get('quantity_variation')
            freight = request.POST.get('freight')
            gst = request.POST.get('gst')
            note = request.POST.get('note')
            job_names = request.POST.getlist('job_name[]')

            pouch_open_size = request.POST.getlist('pouch_size[]')
            pouch_combination = request.POST.getlist('pouch_combination[]')

            quantities = request.POST.getlist('quantity[]')
            purchase_rate_per_kg = request.POST.getlist('purchase_rate_per_kg[]')
            no_of_pouch_kg = request.POST.getlist('no_of_pouch_kg[]')
            per_pouch_rate_basic = request.POST.getlist('per_pouch_rate_basic[]')
            zipper_costs = request.POST.getlist('zipper_cost[]')
            final_rates = request.POST.getlist('final_rare[]')
            min_quantities = request.POST.getlist('minimum_quantity[]')
            pouch_types = request.POST.getlist('pouch_type[]')
            special_instructions = [s.strip() for s in request.POST.getlist('special_instruction[]')]
            delivery_addresses = [s.strip() for s in request.POST.getlist('delivery_address[]')]
            pouch_charges = request.POST.getlist('pouch_charge[]')
            party_email = request.POST.get('party_email')
            new_party_email = request.POST.get('new_party_email') 
            
            
            
            if new_party_name:
                party_name = new_party_name
                
            
            if new_party_email:
                party_email = new_party_email
       
            email_error = utils.email_validator(party_email)
            if email_error:
                messages.error(request, email_error, extra_tags="custom-danger-style")
                return redirect("view_quotations")
            
            party_details, _ = PouchParty.objects.get_or_create(
                    party_name=party_name.strip() if party_name else None
                )
            
            party_email_obj, _ = PouchPartyEmail.objects.get_or_create(
                    party=party_details ,email=party_email  )
            
            
            
            required_fields = {
                "pouch_quotation_number":pouch_quotation_number,
                "delivery_date":delivery_date,
                "party_email":party_email,
                    "party_name":party_name,
                    "job_name":job_names,
                    "pouch_open_size":pouch_open_size,
                    "pouch_combination":pouch_combination,
                    "quantity":quantities,
                    "purchase_rate_per_kg":purchase_rate_per_kg,
                    "no_of_pouch_kg":no_of_pouch_kg,
                    "per_pouch_rate_basic":per_pouch_rate_basic,
                    "zipper_cost":zipper_costs,
                    "final_rare":final_rates,
                    "minimum_quantity":min_quantities,
                    "pouch_type":pouch_types,
                    "special_instruction":special_instructions,
                    "delivery_address":delivery_addresses,
                    "quantity_variation":quantity_variation,
                    
                                
            }
            for field, required in required_fields.items():
                if not required:
                    messages.error(
                        request, f"{field} is Required", extra_tags="custom-danger-style"
                    )
                    return redirect("quotation_page")
            
            quotation = PouchQuotation.objects.create(
                pouch_quotation_number=pouch_quotation_number,
                    delivery_date=delivery_date,
                party_details=party_details,
                party_email=party_email_obj,
                quantity_variate=quantity_variation,
                freight=freight,
                gst=gst,
                note=note,
            )
            for i in range(len(job_names)):
                PouchQuotationJob.objects.create(
                    quotation=quotation,
                    job_name=job_names[i],
                    pouch_open_size=pouch_open_size[i],
                    pouch_combination=pouch_combination[i],
                    quantity=quantities[i],
                    purchase_rate_per_kg=purchase_rate_per_kg[i],
                    no_of_pouch_kg=no_of_pouch_kg[i],
                    per_pouch_rate_basic=per_pouch_rate_basic[i],
                    zipper_cost=zipper_costs[i],
                    pouch_charge=pouch_charges[i],
                    final_rare=final_rates[i],
                    minimum_quantity=min_quantities[i],
                    pouch_type=pouch_types[i],
                    special_instruction=special_instructions[i],
                    delivery_address=delivery_addresses[i],
                )
            
            messages.success(request,"Quotation created successfully ")
            return redirect('quotation_page')
            
        
    context = {
        'pouch_types':pouch_types,
        'party_names':party_names
    }
    
    return render(request, "Quotation/quotation.html",context)

@custom_login_required
def view_quotations(request):


    party_names = PouchParty.objects.all().distinct()
    job_names = PouchQuotationJob.objects.values('job_name').distinct()
    quotations = PouchQuotation.objects.all().order_by('-id')
 
    pouch_types =  PouchQuotationJob.POUCH_TYPE


    if request.method == "GET":

        party_id = request.GET.get('party_id')
        job_id = request.GET.get('job_id')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
      
        if party_id:
            quotations = quotations.filter(party_details_id=party_id)
        if job_id:
            quotations = quotations.filter(pouch_quotation_jobs__job_name=job_id)


        if start_date:
            quotations = quotations.filter(delivery_date=start_date)

        if start_date and end_date:
            quotations = quotations.filter(delivery_date__range=[start_date, end_date])
    if request.method == "POST":
        if 'delete_quotation' in request.POST:
            q_id = request.POST.get('delete_quotation')
            PouchQuotation.objects.filter(id=q_id).delete()
            messages.success(request,'Quotation Delete successfully')
            return redirect('view_quotations')

        elif 'edit_quotation' in request.POST:

            q_id = request.POST.get('quotation_id')
            party_email_id = request.POST.get('party_email_id')
            party_email = request.POST.get('party_email')
            if party_email:
                email_error = utils.email_validator(party_email)
                if email_error:
                    messages.error(request, email_error, extra_tags="custom-danger-style")
                    return redirect("view_quotations")
                if party_email_id:
                    PouchPartyEmail.objects.filter(id=party_email_id).update(email=party_email)

            edit_quotation = get_object_or_404(PouchQuotation, id=q_id)
            edit_quotation.pouch_quotation_number = request.POST.get("pouch_quotation_number")
            edit_quotation.delivery_date = request.POST.get("delivery_date")
            edit_quotation.quantity_variate = request.POST.get("quantity_variate")
            edit_quotation.freight = request.POST.get("freight")
            edit_quotation.gst = request.POST.get("gst")
            edit_quotation.save()
            job_ids = request.POST.getlist("job_id")
            pouch_open_sizes = request.POST.getlist("pouch_open_size")
            pouch_combinations = request.POST.getlist("pouch_combination")
            quantities = request.POST.getlist("quantity")
            purchase_rates = request.POST.getlist("purchase_rate_per_kg")
            no_of_pouch_kgs = request.POST.getlist("no_of_pouch_kg")
            per_pouch_rates = request.POST.getlist("per_pouch_rate_basic")
            zipper_costs = request.POST.getlist("zipper_cost")
            pouch_charges = request.POST.getlist("pouch_charge")
            final_rates = request.POST.getlist("final_rare")
            minimum_quantities = request.POST.getlist("minimum_quantity")
            pouch_types = request.POST.getlist("pouch_type")
            special_instructions = request.POST.getlist("special_instruction")
            delivery_addresses = request.POST.getlist("delivery_address")

     
            for i in range(len(job_ids)):

                job = get_object_or_404(
                    PouchQuotationJob,
                    id=job_ids[i],
                    quotation=edit_quotation
                )
                job.pouch_open_size = pouch_open_sizes[i]
                job.pouch_combination = pouch_combinations[i]
                job.quantity = quantities[i]
                job.purchase_rate_per_kg = purchase_rates[i]
                job.no_of_pouch_kg = no_of_pouch_kgs[i]
                job.per_pouch_rate_basic = per_pouch_rates[i]
                job.zipper_cost = zipper_costs[i]
                job.pouch_charge = pouch_charges[i]
                job.final_rare = final_rates[i]
                job.minimum_quantity = minimum_quantities[i]
                job.pouch_type = pouch_types[i]
                job.special_instruction = special_instructions[i]
                job.delivery_address = delivery_addresses[i]
               
                job.save()

            messages.success(request, 'Quotation Updated Successfully')
            return redirect('view_quotations')
            
        elif (
            "send_quotation_mail" in request.POST
            or "print_quotation" in request.POST
            or "create_purchase_order" in request.POST
        ):

            job_ids = request.POST.getlist("job_id[]")
            party_email = request.POST.get("party_email")
            # ---------- COMMON FIELDS ----------
            common_filed = {
                "check_party_email": "party_email",
                "check_kind_attention": "kind_attention",
                "check_pouch_quotation_number": "pouch_quotation_number",
                "check_delivery_date": "delivery_date",
                "check_party_details": "party_details",
                "check_note": "note",
                "check_gst": "gst",
                "check_quantity_variate": "quantity_variate",
                "check_freight": "freight",
            }   

            update_map = {
                "check_job_name": "job_name",
                "check_pouch_open_size": "pouch_open_size",
                "check_pouch_combination": "pouch_combination",
                "check_quantity": "quantity",
                "check_purchase_rate_per_kg": "purchase_rate_per_kg",
                "check_no_of_pouch_kg": "no_of_pouch_kg",
                "check_per_pouch_rate_basic": "per_pouch_rate_basic",
                "check_zipper_cost": "zipper_cost",
                "check_pouch_charge": "pouch_charge",
                "check_final_rare": "final_rare",
                "check_minimum_quantity": "minimum_quantity",
                "check_pouch_type": "pouch_type",
                "check_delivery_address": "delivery_address",
                "check_special_instruction": "special_instruction",
            }

            # ---------- COMMON VALUES ----------
            common_values = {}

            for checkbox, field in common_filed.items():
                if request.POST.get(checkbox):
                    value = request.POST.get(field)

                    if value in (None, "", "null"):
                        continue

                    if field == "party_details":
                        value = PouchParty.objects.get(id=value)

                    common_values[field] = value

            # ---------- JOB WISE VALUES ----------
            all_selected_jobs = []

            for job_id in job_ids:
                selected_values = {}

                for checkbox, field in update_map.items():
                    checkbox_name = f"{checkbox}_{job_id}"
                    field_name = f"{field}_{job_id}"

                    if checkbox_name not in request.POST:
                        continue

                    value = request.POST.get(field_name)

                    if value in (None, "", "null"):
                        continue

                    selected_values[field] = value

                if selected_values:
                    PouchQuotationJob.objects.filter(id=job_id).update(**selected_values)
                    selected_values["job_id"] = job_id
                    all_selected_jobs.append(selected_values)
            
                        
            if 'send_quotation_mail' in request.POST:
                email_error = utils.email_validator(party_email)
                if email_error:
                    messages.error(request, email_error, extra_tags="custom-danger-style")
                    return redirect("view_quotations")
                receiver_email = party_email
                template_name = "Mail/quotation_mail.html"  

                convert_to_html_content = render_to_string(
                    template_name=template_name,
                    context={"jobs": all_selected_jobs , "common_values": common_values}   
                )
                email = EmailMultiAlternatives(
                    subject='Quotation',
                    body= 'plain_text',
                    from_email= os.environ.get('EMAIL_HOST_USER'),
                    to=[receiver_email]
                )
                email.attach_alternative(convert_to_html_content,"text/html")
                email.send()
                messages.success(request, "Mail Send successfully")
                return redirect("view_quotations")
            
            
            elif "print_quotation" in request.POST:
                print(all_selected_jobs)
                context={"jobs": all_selected_jobs , "common_values": common_values}  
                return render(request, "Includes/quotation/print.html", context)

            
            elif "create_purchase_order" in request.POST:
                quotation_id = request.POST.get("quotation_id")
                job_ids = request.POST.getlist("job_id[]")
                
                quotation = PouchQuotation.objects.get(id=quotation_id)
                jobs = PouchQuotationJob.objects.filter(id__in=job_ids, quotation=quotation).all()
      
                                
                party_names = PouchParty.objects.all()
           
              
                context = {
                    "jobs": jobs,
                    "quotation": quotation,
                    "party_names": party_names,
                    "pouch_types": PurchaseOrderJob.POUCH_TYPE,
                    "polyester_unit": PurchaseOrderJob.POLYESTER_UNIT,
                }
                return render(request, "Purchase Order/purchase_order.html", context)
            
                
            
    paginator =  Paginator(quotations,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages

    context  = {
        "page_range":page_range_placeholder,
        "quotations" : page_obj,
        "pouch_types":pouch_types,
        "party_names":party_names,
        "job_names":job_names
    }
    return render(request,"Quotation/view_quotation.html",context)


@custom_login_required
def quotation_page_ajax(request):
    try:
        if request.method == "GET":
            party_name = request.GET.get('party_name').strip()
            
            purchase_rate_per_kg = float(request.GET.get("purchase_rate_per_kg") or 0)
            no_of_pouch_kg = float(request.GET.get("no_of_pouch_kg") or 0)
            unit = request.GET.get("purchase_rate_unit")
            per_pouch_rate_basic = float(request.GET.get("per_pouch_rate_basic") or 0)
            zipper_cost =float(request.GET.get("zipper_cost") or 0)
            pouch_charge = float(request.GET.get("pouch_charge") or 0)
            
            jobs  = list(PouchQuotationJob.objects.filter(quotation__party_details__party_name=party_name).values('job_name').distinct())
            party_emails = list(PouchPartyEmail.objects.filter(party__party_name=party_name).values('email'))
            total_ppb = 0
            
            if purchase_rate_per_kg:   
                if unit == "polyester_printed_bag":
                    total_ppb = purchase_rate_per_kg / no_of_pouch_kg
                elif unit == "polyester_printed_roll":
                    total_ppb = purchase_rate_per_kg

            total_ppb = round(total_ppb, 2)
            
       
            final_rare = int(per_pouch_rate_basic + zipper_cost + pouch_charge) 
            
            minimum_quantity  = no_of_pouch_kg * 500
            # print("This No of KG ",no_of_pouch_kg)
            # print(jobs)
            print(jobs)
            return JsonResponse({
                "per_pouch_rate_basic": total_ppb,
                "final_rare": final_rare,
                "jobs":jobs,
                "minimum_quantity":minimum_quantity,
                "party_emails":party_emails
            })
    except Exception as e:
        # messages.error(request,"Something went wrong ")
        print(e)
        

    return HttpResponse("")