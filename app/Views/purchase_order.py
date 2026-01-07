from .common_imports import *


@custom_login_required
def purchase_order(request):
    party_names = PouchParty.objects.values('party_name')
    pouch_types =  PurchaseOrderJob.POUCH_TYPE
    polyester_unit = PurchaseOrderJob.POLYESTER_UNIT
    
    if request.method == 'POST':
        if 'create_purchase_order' in request.POST:
            delivery_date =  request.POST.get('delivery_date')
            party_name = request.POST.get('party_name')
          
            job_name = request.POST.getlist('job_name')
            pouch_open_size = request.POST.getlist('pouch_size')
            pouch_combination = request.POST.getlist('pouch_combination')
            quantity = request.POST.getlist('quantity')
            purchase_rate_per_kg = request.POST.getlist('purchase_rate_per_kg')
            no_of_pouch_kg = request.POST.getlist('no_of_pouch_kg')
            per_pouch_rate_basic = request.POST.getlist('per_pouch_rate_basic')
            pouch_charge = request.POST.getlist('pouch_charge')
            zipper_cost = request.POST.getlist('zipper_cost')
            final_rare = request.POST.getlist('final_rare')
            minimum_quantity = request.POST.getlist('minimum_quantity')
            pouch_type = request.POST.getlist('pouch_type')
            special_instruction = request.POST.getlist('special_instruction')
            delivery_address = request.POST.getlist('delivery_address')
          
            polyester_unit = request.POST.getlist('purchase_rate_unit')
            
            quantity_variation = request.POST.get('quantity_variation')
            freight = request.POST.get('freight')
            gst = request.POST.get('gst')
            note = request.POST.get('note')

            if party_name == "others":
                party_name = request.POST.get("new_party_name")
            party_details, _ = PouchParty.objects.get_or_create(
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
                    "minimum_quantity":minimum_quantity,
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
                
                
            purchase_order   = PurchaseOrder.objects.create(
                delivery_date=delivery_date,
                party_details=party_details,
                quantity_variate=quantity_variation,
                freight=freight,
                gst=gst,
                note=note,
            )
            
            for i in range(len(job_name)):
                PurchaseOrderJob.objects.create(
                    purchase_order=purchase_order,
                    job_name= job_name[i],
                    pouch_open_size=pouch_open_size[i],
                    pouch_combination=pouch_combination[i],
                    quantity=quantity[i],
                    purchase_rate_per_kg=purchase_rate_per_kg[i],
                    no_of_pouch_kg=no_of_pouch_kg[i],
                    per_pouch_rate_basic=per_pouch_rate_basic[i],
                    zipper_cost=zipper_cost[i],
                    pouch_charge=pouch_charge[i],
                    final_rare=final_rare[i],
                    minimum_quantity=minimum_quantity[i],
                    pouch_type=pouch_type[i],
                    special_instruction=special_instruction[i],
                    delivery_address=delivery_address[i],
                    
                    )
            purchase_order.save()
            messages.success(request,"Purchase Order created successfully ")
            return redirect('quotation_page')
              
    context ={
        'party_names':party_names,
        'pouch_types':pouch_types,
        'polyester_unit':polyester_unit
    }
    return render(request,"Purchase Order/purchase_order.html",context)


@custom_login_required
def view_purchase_order(request):
    purchase_orders = PurchaseOrder.objects.all().order_by('-id')
    if request.method == "POST":
        if 'delete_purchase_order' in request.POST:
            po_id = request.POST.get('delete_purchase_order')
            PurchaseOrder.objects.filter(id=po_id).delete()
            messages.success(request,'Purchase Order Delete successfully')
            return redirect('view_purchase_order')
        elif 'update_purchase_order' in request.POST:
            purchase_order_id = request.POST.get('edit_purchase_order')
            edit_purchase_order = get_object_or_404(PurchaseOrder,id=purchase_order_id)
            edit_purchase_order.delivery_date = request.POST.get("delivery_date")
            edit_purchase_order.quantity_variate = request.POST.get("quantity_variate")
            edit_purchase_order.freight = request.POST.get("freight")
            edit_purchase_order.gst = request.POST.get("gst")
            edit_purchase_order.save()
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
                    PurchaseOrderJob,
                    id=job_ids[i],
                    purchase_order=edit_purchase_order
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

            messages.success(request, 'Purchase Order Updated Successfully')
            return redirect('view_purchase_order')
                
        elif 'send_purchase_order_mail' in request.POST:
            job_ids = request.POST.getlist("job_id[]")
            party_email = request.POST.get("party_email")
            if request.method == 'POST':
                common_filed = {
                "check_delivery_date": "delivery_date",
          
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
            common_values = {}

            for checkbox, field in common_filed.items():
                if request.POST.get(checkbox):
                    value = request.POST.get(field)

                    if value in [None, "", "null"]:
                        continue

                    if field == "party_details":
                        value = Party.objects.get(id=value)

                    common_values[field] = value
            all_selected_jobs = []
            for i in range(len(job_ids)):
                selected_values = {}

                for checkbox, field in update_map.items():
                    cb_list = request.POST.getlist(f"{checkbox}[]")
                    field_list = request.POST.getlist(f"{field}[]")


                    if not cb_list or len(cb_list) <= i:
                        continue

        
                    if not cb_list[i]:
                        continue

               
                    if not field_list or len(field_list) <= i:
                        continue

                    value = field_list[i]

                    if value in (None, "", "null"):
                        continue

                    if field == "party_details":
                        value = Party.objects.get(id=value)

                    selected_values[field] = value

                PurchaseOrderJob.objects.filter(id=job_ids[i]).update(**selected_values)
                all_selected_jobs.append(selected_values)
                
            if 'send_purchase_order_mail' in request.POST:
                
                email_error = utils.email_validator(party_email)
                if email_error:
                    messages.error(request, email_error, extra_tags="custom-danger-style")
                    return redirect("view_purchase_order")
                
                receiver_email = party_email
                template_name = "Mail/purchase_order_mail.html"
                convert_to_html_content = render_to_string(
                    template_name=template_name,
                    context={"jobs": all_selected_jobs , "common_values": common_values}   
                )
                email = EmailMultiAlternatives(
                    subject='Purchase Order',
                    body= 'plain_text',
                    from_email= os.environ.get('EMAIL_HOST_USER'),
                    to=[receiver_email]
                )
                email.attach_alternative(convert_to_html_content,"text/html")
                email.send()
                messages.success(request, "Mail Send successfully")
                return redirect("view_purchase_order")

    paginator =  Paginator(purchase_orders,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages
    
    context  = {
        "pouch_types": PurchaseOrderJob.POUCH_TYPE,
        "polyester_unit": PurchaseOrderJob.POLYESTER_UNIT,
        "page_range":page_range_placeholder,
        "purchase_orders" : page_obj  }
    return render(request,"Purchase Order/view_purchase_order.html",context)
          
@custom_login_required       
def purchase_order_ajax(request):
    try:
        if request.method == "GET":
            party_name = request.GET.get('party_name')
            
            purchase_rate_per_kg = float(request.GET.get("purchase_rate_per_kg") or 0)
            no_of_pouch_kg = float(request.GET.get("no_of_pouch_kg") or 0)
            unit = request.GET.get("purchase_rate_unit")
            per_pouch_rate_basic = float(request.GET.get("per_pouch_rate_basic") or 0)
            zipper_cost =float(request.GET.get("zipper_cost") or 0)
            pouch_charge = float(request.GET.get("pouch_charge") or 0)
            
      
            total_ppb = 0
            jobs  = list(PurchaseOrderJob.objects.filter(purchase_order__party_details__party_name=party_name).values('job_name').distinct())
          
            if purchase_rate_per_kg:   
                if unit == "polyester_printed_bag":
                    total_ppb = purchase_rate_per_kg / no_of_pouch_kg
                elif unit == "polyester_printed_roll":
                    total_ppb = purchase_rate_per_kg

            total_ppb = round(total_ppb, 2)
            
            
            final_rare = int(per_pouch_rate_basic + zipper_cost + pouch_charge) 
            
            minimum_quantity  = no_of_pouch_kg * 500
          
            return JsonResponse({
                "per_pouch_rate_basic": total_ppb,
                "final_rare": final_rare,
                "jobs":jobs,
                "minimum_quantity":minimum_quantity
            })
    except Exception as e:
        messages.error(request,"Something went wrong ")
        print(e)
        

    return HttpResponse("")