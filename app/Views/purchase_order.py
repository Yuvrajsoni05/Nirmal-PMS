from .common_imports import *


@custom_login_required
def purchase_order(request):
    party_names = PouchParty.objects.values('party_name')
    pouch_types =  PurchaseOrderJob.POUCH_TYPE
    polyester_unit = PurchaseOrderJob.POLYESTER_UNIT
    
    if request.method == 'POST':
        if 'create_purchase_order' in request.POST:
            pouch_purchase_number = request.POST.get('pouch_purchase_number')
            delivery_date =  request.POST.get('delivery_date')
            party_name = request.POST.get('party_name')
            party_contact = request.POST.get('party_contact')
            job_name = request.POST.getlist('job_name')
            pouch_open_size = request.POST.getlist('pouch_size')
            pouch_combination = request.POST.getlist('pouch_combination')
            quantity = request.POST.getlist('quantity')
            purchase_rate_per_kg = request.POST.getlist('purchase_rate_per_kg')
            no_of_pouch_kg = request.POST.getlist('no_of_pouch_kg')
            rate_basic = request.POST.getlist('per_pouch_rate_basic')
            pouch_charge = request.POST.getlist('pouch_charge')
            zipper_cost = request.POST.getlist('zipper_cost')
            final_rate = request.POST.getlist('final_rate')
            minimum_quantity = request.POST.getlist('minimum_quantity')
            pouch_type = request.POST.getlist('pouch_type')
            special_instruction = [s.strip() for s in request.POST.getlist('special_instruction')]
            delivery_address = [s.strip() for s in request.POST.getlist('delivery_address')]
            polyester_unit = request.POST.getlist('purchase_rate_unit')
            quantity_variation = request.POST.get('quantity_variation')
            freight = request.POST.get('freight')
            gst = request.POST.get('gst')
            note = request.POST.get('note')
            party_email = request.POST.get('party_email')
            new_party_email = request.POST.get('new_party_email') 
            pouch_status = request.POST.get('pouch_status')
            
            
     
            if party_name == "others":
                party_name = request.POST.get("new_party_name")

 

            
            if party_email == "others":

                if not new_party_email:
                    messages.error(request, "Party email is required")
                    return redirect("purchase_order")
                party_email = new_party_email.strip()

            if party_contact == "others":
                party_contact = request.POST.get("new_party_contact")
            
            party_number_check = utils.phone_number_check(party_contact)
            if party_number_check:
                messages.error(
                    request, party_number_check, extra_tags="custom-danger-style"
                )
                return redirect("purchase_order")
            
            email_error = utils.email_validator(party_email)
            if email_error:
                messages.error(request, email_error, extra_tags="custom-danger-style")
                return redirect("purchase_order")   



            required_fields = {
                "delivery_date":delivery_date,
                    "party_name":party_name,
                    "party_email":party_email,
                    "job_name":job_name,
                    "pouch_open_size":pouch_open_size,
                    "pouch_combination":pouch_combination,
                    "quantity":quantity,
                    "purchase_rate_per_kg":purchase_rate_per_kg,
                    "no_of_pouch_kg":no_of_pouch_kg,
                    "per_pouch_rate_basic":rate_basic,
                    "zipper_cost":zipper_cost,
                    "final_rate":final_rate,
                    "minimum_quantity":minimum_quantity,
                    "pouch_type":pouch_type,
                
                    "delivery_address":delivery_address,
           
                    "pouch_status":pouch_status,
            
            }
            for field, required in required_fields.items():
                if not required:
                    messages.error(
                        request, f"{field} is Required", extra_tags="custom-danger-style"
                    )
                    return redirect("purchase_order")


             # Party Block
            party_details, party_email_obj, party_contact_obj = utils.get_or_create_party(
                party_name,
                party_email,
                party_contact
            )
            
            purchase_order   = PurchaseOrder.objects.create(
                pouch_purchase_number=pouch_purchase_number ,
                delivery_date=delivery_date,
                party_details=party_details,
                quantity_variate=quantity_variation,
                freight=freight,
                gst=gst,
                note=note,
                party_contact=party_contact_obj,
                party_email=party_email_obj,
                pouch_status=pouch_status,
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
                    rate_basic=rate_basic[i],
                    zipper_cost=zipper_cost[i],
                    pouch_charge=pouch_charge[i],
                    final_rate=final_rate[i],
                    minimum_quantity=minimum_quantity[i],
                    pouch_type=pouch_type[i],
                    special_instruction=special_instruction[i],
                    delivery_address=delivery_address[i],
                    polyester_unit=polyester_unit[i],
                    )

            purchase_order.save()
            messages.success(request,"Purchase Order created successfully ")
            return redirect('purchase_order')
              
    context ={
        'party_names':party_names,
        'pouch_types':pouch_types,
        'polyester_unit':polyester_unit,
        'pouch_status':PurchaseOrder.POUCH_STATUS
    }
    return render(request,"Purchase Order/purchase_order.html",context)


@custom_login_required
def view_purchase_order(request):
    purchase_orders = PurchaseOrder.objects.all().order_by('-id')
    party_names = PouchParty.objects.all()
    job_names = PurchaseOrderJob.objects.all().distinct('job_name')

    party_id = request.GET.get('party_id')
    job_id = request.GET.get('job_id')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
  
    if party_id:
        purchase_orders = purchase_orders.filter(party_details_id=party_id)

    if job_id:
        purchase_orders = purchase_orders.filter(purchase_order_jobs__id=job_id)

    if start_date and end_date:
        purchase_orders = purchase_orders.filter(delivery_date__range=[start_date, end_date])
    elif start_date:
        purchase_orders = purchase_orders.filter(delivery_date=start_date)
 
    
    if request.method == "GET":
        if 'download_purchase_order' in request.GET:
          
            purchase_order = PurchaseOrder.objects.all()
            wb = Workbook()
            ws = wb.active
            ws.title = "Pouch Master"

            ws.append([
            "Pouch Purchase Number",
            "Delivery Date",
            "Party Name",
            "Party Email",
            "Party Contact",
            "Job Name",
            "Pouch Open Size",
            "Pouch Combination",
            "Quantity",
            "Purchase Rate / KG",
            "No. of Pouch / KG",
            "Rate Basic",
            "Zipper Cost",
            "Pouch Charge",
            "Final Rate",
            "Minimum Quantity",
            "Pouch Type",
            "Special Instruction",
            "Delivery Address",
            "Polyester Unit",
            "Freight",
            "GST",
            "Note",
            "Pouch Status",
        ])


            for obj in purchase_order:
                jobs = obj.purchase_order_jobs.all()

                for job in jobs:
                    ws.append([
                        obj.pouch_purchase_number,
                        obj.delivery_date,
                obj.party_details.party_name if obj.party_details else "",
                obj.party_email.email if obj.party_email else "",
                obj.party_contact.party_number if obj.party_contact else "",

                job.job_name,
                job.pouch_open_size,
                job.pouch_combination,
                job.quantity,
                job.purchase_rate_per_kg,
                job.no_of_pouch_kg,
                job.rate_basic,
                job.zipper_cost,
                job.pouch_charge,
                job.final_rate,
                job.minimum_quantity,
                job.pouch_type,
                job.special_instruction,
                job.delivery_address,
                job.polyester_unit,
                obj.freight,
                obj.gst,
                obj.note,
                obj.pouch_status,
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="purchase_order.xlsx"'
            wb.save(response)
            return response

            


    if request.method == "POST":
        if 'delete_purchase_order' in request.POST:
            if request.method == "POST":

                po_id = request.POST.get('delete_purchase_order')

                purchase_order = get_object_or_404(
                    PurchaseOrder,
                    id=po_id,
                )
                purchase_order.delete()
                messages.success(request, "Purchase Order deleted successfully")
                return redirect("view_purchase_order")

        elif 'update_purchase_order' in request.POST:
            purchase_order_id = request.POST.get('edit_purchase_order')
            party_email_id = request.POST.get('party_email_id')
            party_email = request.POST.get('party_email')
            if party_email:
                email_error = utils.email_validator(party_email)
                if email_error:
                    messages.error(request, email_error, extra_tags="custom-danger-style")
                    return redirect("view_purchase_order")
                if party_email_id:
                    PouchPartyEmail.objects.filter(id=party_email_id).update(email=party_email)
            edit_purchase_order = get_object_or_404(PurchaseOrder,id=purchase_order_id)
            edit_purchase_order.pouch_purchase_number = request.POST.get("pouch_purchase_number") 
            edit_purchase_order.delivery_date = request.POST.get("delivery_date")
            edit_purchase_order.quantity_variate = request.POST.get("quantity_variate")
            edit_purchase_order.freight = request.POST.get("freight")
            edit_purchase_order.gst = request.POST.get("gst")
            edit_purchase_order.note = request.POST.get("note")
            edit_purchase_order.pouch_status = request.POST.get("pouch_status")
            edit_purchase_order.save()

            job_ids = request.POST.getlist("job_id")
            pouch_open_sizes = request.POST.getlist("pouch_open_size")
            pouch_combinations = [s.strip() for s in request.POST.getlist("pouch_combination")]
            quantities = request.POST.getlist("quantity")
            purchase_rates = request.POST.getlist("purchase_rate_per_kg")
            no_of_pouch_kgs = request.POST.getlist("no_of_pouch_kg")
            per_pouch_rates = request.POST.getlist("per_pouch_rate_basic")
            zipper_costs = request.POST.getlist("zipper_cost")
            pouch_charges = request.POST.getlist("pouch_charge")
            final_rates = request.POST.getlist("final_rate")
            minimum_quantities = request.POST.getlist("minimum_quantity")
            pouch_types = request.POST.getlist("pouch_type")
            special_instructions = request.POST.getlist("special_instruction")
            delivery_addresses = request.POST.getlist("delivery_address")
            polyester_units = request.POST.getlist("polyester_units")
            for i in range(len(job_ids)):
                total_ppb = 0

                if polyester_units[i]:
                    if polyester_units[i]:
                        if polyester_units[i] == 'polyester_printed_bag':

                            total_ppb = float(purchase_rates[i]) /  float(no_of_pouch_kgs[i])
                        else:
                            total_ppb = float(purchase_rates[i])
                            print(purchase_rates)

                print(total_ppb)
                mq = float(no_of_pouch_kgs[i]) * 500
                zipper_cost = float(zipper_costs[i] or 0)
                pouch_charge = float(pouch_charges[i] or 0)
               

                final_rate = round(total_ppb + zipper_cost + pouch_charge, 3)
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
                job.rate_basic = total_ppb
                job.zipper_cost = zipper_costs[i]
                job.pouch_charge = pouch_charges[i]
                job.final_rate = final_rate
                job.minimum_quantity = mq
                job.pouch_type = pouch_types[i]
                job.special_instruction = special_instructions[i]
                job.delivery_address = delivery_addresses[i]
                job.save()

            messages.success(request, 'Purchase Order Updated Successfully')
            return redirect('view_purchase_order')
                
        elif (
            "send_purchase_order_mail" in request.POST
            or "print_purchase_order" in request.POST
           
            ):
            

            job_ids = request.POST.getlist("job_id[]")
            party_email = request.POST.get("party_email")
            # ---------- COMMON FIELDS ----------
            common_filed = {
                "check_pouch_purchase_number": "pouch_purchase_number",
                "check_party_email": "party_email",
                "check_kind_attention": "kind_attention",
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
                "check_final_rate": "final_rate",
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
            if 'print_purchase_order' in request.POST:
                print(all_selected_jobs)
                print(common_values)
                context={"jobs": all_selected_jobs , "common_values": common_values}  
                return render(request, "Includes/purchase_order/print.html", context)

                

    paginator =  Paginator(purchase_orders,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages
    
    context  = {
        "pouch_types": PurchaseOrderJob.POUCH_TYPE,
        "polyester_unit": PurchaseOrderJob.POLYESTER_UNIT,
        "page_range":page_range_placeholder,
        "purchase_orders" : page_obj,
        "party_names":party_names,
        "pouch_status":PurchaseOrder.POUCH_STATUS,
    "job_names":job_names,  }
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
            
            party_contacts = list(PouchPartyContact.objects.filter(party__party_name=party_name).values('party_number'))

            total_ppb = 0
            jobs  = list(PurchaseOrderJob.objects.filter(purchase_order__party_details__party_name=party_name).values_list('job_name', flat=True).distinct())
          
            if purchase_rate_per_kg:   
                if unit == "polyester_printed_bag":
                    total_ppb = purchase_rate_per_kg / no_of_pouch_kg
                elif unit == "polyester_printed_roll":
                    total_ppb = purchase_rate_per_kg

            total_ppb = round(total_ppb, 2)
            
            party_emails = list(PouchPartyEmail.objects.filter(party__party_name=party_name).values('email'))
       
            final_rate = round(total_ppb + zipper_cost + pouch_charge,3) 
            minimum_quantity  = no_of_pouch_kg * 500

         
            
            return JsonResponse({
                "per_pouch_rate_basic": total_ppb,
                "final_rate": round(final_rate or 0, 2),
                "jobs":jobs,
                "party_contacts":party_contacts,
                "party_emails":party_emails,
                "minimum_quantity":round(minimum_quantity or 0, 2),
            })
    except Exception as e:
        print(e)
        
    return HttpResponse("")