from .common_imports import *

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
            minimum_quantity = request.POST.get('minimum_quantity')
            pouch_type = request.POST.get('pouch_type')
            special_instruction = request.POST.get('special_instruction')
            delivery_address = request.POST.get('delivery_address')
            quantity_variation = request.POST.get('quantity_variation')
            freight = request.POST.get('freight')
            gst = request.POST.get('gst')
            note = request.POST.get('note')
            pouch_charge = request.POST.get('pouch_charge')
            new_party_name = request.POST.get('new_party_name')
            new_job_name = request.POST.get('new_job_name')
            
            
            if new_party_name:
                party_details = new_party_name
                
            if new_job_name:
                job_name = new_job_name
            
            
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
                minimum_quantity=minimum_quantity,
                pouch_type=pouch_type,
                special_instruction=special_instruction,
                delivery_address=delivery_address,
                quantity_variate=quantity_variation,
                freight=freight,
                gst=gst,
                note=note,    
            )
            pq.save()
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
            
            q_id = request.POST.get('edit_quotation')

            edit_quotation = get_object_or_404(PouchQuotation, id=q_id)

            edit_quotation.delivery_date = request.POST.get("delivery_date")
            edit_quotation.job_name = request.POST.get("job_name")
            edit_quotation.pouch_open_size = request.POST.get("pouch_open_size")
            edit_quotation.pouch_combination = request.POST.get("pouch_combination")
            edit_quotation.quantity = request.POST.get("quantity")
            edit_quotation.purchase_rate_per_kg = request.POST.get("purchase_rate_per_kg")
            edit_quotation.no_of_pouch_kg = request.POST.get("no_of_pouch_kg")
            edit_quotation.per_pouch_rate_basic = request.POST.get("per_pouch_rate_basic")
            edit_quotation.zipper_cost = request.POST.get("zipper_cost")
            edit_quotation.pouch_charge = request.POST.get("pouch_charge")
            edit_quotation.final_rare = request.POST.get("final_rare")
            edit_quotation.minimum_quantity = request.POST.get("minimum_quantity")
            edit_quotation.pouch_type = request.POST.get("pouch_type")
            edit_quotation.quantity_variate = request.POST.get("quantity_variate")
            edit_quotation.freight = request.POST.get("freight")
            edit_quotation.gst = request.POST.get("gst")
            edit_quotation.delivery_address = request.POST.get("delivery_address")
            edit_quotation.special_instruction = request.POST.get("special_instruction")
            edit_quotation.note = request.POST.get("note")
            edit_quotation.save()
            messages.success(request,'Quotation Updated Successfully')
            return redirect('view_quotations')           
            
        elif 'send_quotation_mail' in request.POST or 'create_purchase_order' in request.POST:
            if request.method == 'POST':
                selected_values = {}
                update_map = {
                    "chk_delivery_date": "delivery_date",
                    "chk_party_details": "party_details",
                    "chk_job_name": "job_name",
                    "chk_pouch_open_size": "pouch_open_size",
                    "chk_pouch_combination": "pouch_combination",
                    "chk_quantity": "quantity",
                    "chk_purchase_rate_per_kg": "purchase_rate_per_kg",
                    "chk_no_of_pouch_kg": "no_of_pouch_kg",
                    "chk_per_pouch_rate_basic": "per_pouch_rate_basic",
                    "chk_zipper_cost": "zipper_cost",
                    "chk_pouch_charge": "pouch_charge",
                    "chk_final_rare": "final_rare",
                    "chk_minimum_quantity": "minimum_quantity",
                    "chk_pouch_type": "pouch_type",
                    "chk_quantity_variate": "quantity_variate",
                    "chk_freight": "freight",
                    "chk_gst": "gst",
                    "chk_delivery_address": "delivery_address",
                    "chk_special_instruction": "special_instruction",
                    "chk_note": "note",
                }
              
                for checkbox, field in update_map.items():
                   
                    if request.POST.get(checkbox):
                        
                        value = request.POST.get(field)
                      
                        if value in [None, "", "null"]:
                            continue
                        
                        if field == "party_details":
                            value = Party.objects.get(id=value)

                        selected_values[field] = value
                        
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
            if unit == "polyester_printed_bug":
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

    return HttpResponse("")