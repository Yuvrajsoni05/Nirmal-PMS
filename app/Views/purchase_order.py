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
    paginator =  Paginator(purchase_orders,10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    page_range_placeholder = "a" * page_obj.paginator.num_pages
    
    context  = {
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
            
            print(party_name)
            total_ppb = 0
            jobs  = list(PurchaseOrderJob.objects.filter(purchase_order__party_details__party_name=party_name).values('job_name'))
            print(jobs)
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