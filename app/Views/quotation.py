from .common_imports import *

def quotation_page(request):
    
    
    party_names = Party.objects.values('party_name')
    pouch_types =  PouchQuotation.POUCH_TYPE
    
    if request.method == 'POST':
        if 'save_quotation' in request.POST:
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
            special_instructions = request.POST.getlist('special_instruction[]')
            delivery_addresses = request.POST.getlist('delivery_address[]')
            pouch_charges = request.POST.getlist('pouch_charge[]')
           
            
            
           
            
            
            if new_party_name:
                party_details = new_party_name
                
          
            
            
            party_details, _ = Party.objects.get_or_create(
                    party_name=party_name.strip() if party_name else None
                )
            
            required_fields = {
                "delivery_date":delivery_date,
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
                delivery_date=delivery_date,
                party_details=party_details,
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
    quotations = PouchQuotation.objects.all().order_by('-id')

    if request.method == "POST":
        if 'delete_quotation' in request.POST:
            q_id = request.POST.get('delete_quotation')
            PouchQuotation.objects.filter(id=q_id).delete()
            messages.success(request,'Quotation Delete successfully')
            return redirect('view_quotations')

        elif 'edit_quotation' in request.POST:

            q_id = request.POST.get('quotation_id')
            edit_quotation = get_object_or_404(PouchQuotation, id=q_id)

            # ---- Update Parent Quotation ----
            edit_quotation.delivery_date = request.POST.get("delivery_date")
            edit_quotation.quantity_variate = request.POST.get("quantity_variate")
            edit_quotation.freight = request.POST.get("freight")
            edit_quotation.gst = request.POST.get("gst")
            edit_quotation.save()

            # ---- Get Lists of Job Fields ----
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
            
        elif 'send_quotation_mail' in request.POST or 'create_purchase_order' in request.POST:
            if request.method == 'POST':
                selected_values = {}
                update_map = {
                    "check_delivery_date": "delivery_date",
                    "check_party_details": "party_details",
                    "check_job_name": "job_name",
                    "check_pouch_open_size": "pouch_open_size",
                    "check_pouch_combination": "pouch_combination",
                    "check_quantity": "quantity",
                    "check_purchase_rate_per_kg": "purchase_rate_per_kg",
                    "check_no_of_pouch_kg": "no_of_pouch_kg",
                    "check_per_pouch_rate_basic": "per_pouch_rate_basic",
                    "check_zipper_cost": "zipper_cost",
                    "check_pouch_charge": "pouch_charge",
                    "check_final_rate": "final_rate",
                    "check_minimum_quantity": "minimum_quantity",
                    "check_pouch_type": "pouch_type",
                    "check_quantity_variate": "quantity_variate",
                    "check_freight": "freight",
                    "check_gst": "gst",
                    "check_delivery_address": "delivery_address",
                    "check_special_instruction": "special_instruction",
                    "check_note": "note",
                }

              
                selected_values = {}

                for checkbox, field in update_map.items():
                    if request.POST.get(checkbox):
                        value = request.POST.get(field)

                        if value in [None, "", "null"]:
                            continue

                        if field == "party_details":
                            value = Party.objects.get(id=value)

                        selected_values[field] = value

                print(selected_values)

                        
            if 'send_quotation_mail' in request.POST:
                # print(selected_values)
                receiver_email = 'soniyuvraj9499@gmail.com'
                template_name = "Mail/quotation_mail.html"
                convert_to_html_content = render_to_string(
                    template_name=template_name, context=selected_values
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
            
            elif "create_purchase_order" in request.POST:
                quotation_id = request.POST.get("quotation_id")
                quotation = PouchQuotation.objects.get(id=quotation_id)
                # print(selected_values)
                context = {
                    "selected_values": selected_values,  
                    "quotation": selected_values,
                    "party_names": Party.objects.values("party_name"),
                    "pouch_types": PurchaseOrder.POUCH_TYPE,
                    "polyester_unit": PurchaseOrder.POLYESTER_UNIT,
                }
                return render(request, "Purchase Order/purchase_order.html", context)
                
            
    paginator =  Paginator(quotations,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages
    
    context  = {
        "page_range":page_range_placeholder,
        "quotations" : page_obj
    }
    return render(request,"Quotation/view_quotation.html",context)


@custom_login_required
def quotation_page_ajax(request):
    if request.method == "GET":
        party_name = request.GET.get('party_name')
        
        purchase_rate_per_kg = float(request.GET.get("purchase_rate_per_kg") or 0)
        no_of_pouch_kg = float(request.GET.get("no_of_pouch_kg") or 0)
        unit = request.GET.get("purchase_rate_unit")
        per_pouch_rate_basic = float(request.GET.get("per_pouch_rate_basic") or 0)
        zipper_cost =float(request.GET.get("zipper_cost") or 0)
        pouch_charge = float(request.GET.get("pouch_charge") or 0)
        jobs = list(utils.all_job_name_list(party_name))
        
        total_ppb = 0
        
        if purchase_rate_per_kg:   
            if unit == "polyester_printed_bag":
                total_ppb = purchase_rate_per_kg / no_of_pouch_kg
            elif unit == "polyester_printed_roll":
                total_ppb = purchase_rate_per_kg

        total_ppb = round(total_ppb, 2)
        
        
        final_rare = int(per_pouch_rate_basic + zipper_cost + pouch_charge) 
        
        minimum_quantity  = no_of_pouch_kg * 500
        print(jobs)
        return JsonResponse({
            "per_pouch_rate_basic": total_ppb,
            "final_rare": final_rare,
            "jobs":jobs,
            "minimum_quantity":minimum_quantity
        })

    return HttpResponse("")