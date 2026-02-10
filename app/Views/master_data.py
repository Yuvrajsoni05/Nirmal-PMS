from .common_imports import *

def master_page(request):
    pouch_party = PouchParty.objects.all()
     
    if "create_master_data" in request.POST:
        if request.method == "POST":
            party_name = request.POST.get('party_name')
            party_contact = request.POST.get('party_contact')
            party_email = request.POST.get('party_email')
            job_name = request.POST.getlist('job_name')
            pouch_open_size = request.POST.getlist('pouch_open_size')
            pouch_combination = request.POST.getlist('pouch_combination')
            purchase_rate_per_kg = request.POST.getlist('purchase_rate_per_kg')
            no_of_pouch_per_kg = request.POST.getlist('no_of_pouch_per_kg')      

            if party_name == "other":
                party_name = request.POST.get('new_party_name')
            if party_contact == "other":
                party_contact = request.POST.get('new_party_contact')
            if party_email == "other":
                party_email = request.POST.get('new_party_email')

            party_details, _ = PouchParty.objects.get_or_create(
                            party_name=party_name.strip() if party_name else None
                        )
            party_email_obj, _ = PouchPartyEmail.objects.get_or_create(
                            party=party_details ,email=party_email  )
            party_contact_obj, _ = PouchPartyContact.objects.get_or_create(
                            party=party_details ,party_number=party_contact)
         
            for i in range(len(job_name)):
                minimum_quantity = int(no_of_pouch_per_kg[i])*500
                print("minimum_quantity",minimum_quantity)
                PouchMaster.objects.create(
                    job_name=job_name[i],
                    pouch_open_size=pouch_open_size[i],
                    pouch_combination=pouch_combination[i],
                    purchase_rate_per_kg=purchase_rate_per_kg[i],
                    no_of_pouch_per_kg=no_of_pouch_per_kg[i],
                    party_details=party_details,
                    party_contact=party_contact_obj,
                    party_email=party_email_obj,
                    minimum_quantity=minimum_quantity   
          
                )
            messages.success(request, 'Master Data Created Successfully')
            return redirect('master_page')
    context = {
        'pouch_party': pouch_party,
    }
    return render(request, "MasterData/master_page.html", context)






def view_master_data(request):    
  
    pouch_master_data = PouchMaster.objects.select_related(
    "party_details",
    "party_email",
    "party_contact").all().order_by('id')
    party_name = PouchParty.objects.all()
    job_name = pouch_master_data.values_list('job_name', flat=True).distinct()
    if request.method == "GET":
        if "search_pouch_master" in request.GET:
            search_party_name = request.GET.get('search_party_name')
            search_job_name = request.GET.get('search_job_name')
            
            
            if search_job_name:
                pouch_master_data = pouch_master_data.filter(job_name__icontains=search_job_name)
            if search_party_name:
                pouch_master_data = pouch_master_data.filter(party_details__party_name__icontains=search_party_name)
        
    if request.method == "POST":

        if "create_quotation" in request.POST:
            create_quotation_id = request.POST.getlist('create_quotation_id')
            party_names = PouchParty.objects.all()
            jobs = PouchMaster.objects.filter(
                id__in=create_quotation_id
            ).values(
                
                'job_name',
                'pouch_open_size',
                'pouch_combination',
                'purchase_rate_per_kg',
                'no_of_pouch_per_kg',
                'party_details__party_name',
    
                )
            
            party_ids = jobs.values_list('party_details_id', flat=True).distinct()
            if party_ids.count() > 1:
                messages.warning(
                    request,
                    "You have selected jobs from different parties. "
                    "Please select jobs from only one party to create a quotation."
                )
                return redirect('view_master_data')
            context={
                "party_names": party_names,
                "pouch_types": PouchQuotationJob.POUCH_TYPE,
                "polyester_units": PouchQuotationJob.POLYESTER_UNIT,
                'pouch_status':PouchQuotation.POUCH_STATUS,
                'master_data': jobs,
            }
            return render(request, "Quotation/quotation.html", context)


        if 'create_purchase_order' in request.POST:
            create_quotation_id = request.POST.getlist('create_quotation_id')
            party_names = PouchParty.objects.all()
            jobs = PouchMaster.objects.filter(
                id__in=create_quotation_id
            ).values(
          
                'job_name',
                'pouch_open_size',
                'pouch_combination',
                'purchase_rate_per_kg',
                'no_of_pouch_per_kg',
                'party_details__party_name',

                )
            party_ids = jobs.values_list('party_details_id', flat=True).distinct()
            if party_ids.count() > 1:
                messages.warning(
                    request,
                    "You have selected jobs from different parties. "
                    "Please select jobs from only one party to create a quotation."
                )
                return redirect('view_master_data')
            context={
                "party_names": party_names,
                "pouch_types": PurchaseOrderJob.POUCH_TYPE,
                "polyester_units": PurchaseOrderJob.POLYESTER_UNIT,
                'pouch_status':PurchaseOrder.POUCH_STATUS,
                'master_data': jobs,
            }
            return render(request, "Purchase Order/purchase_order.html", context)
            




        if "download_data" in request.POST:
            wb = Workbook()
            ws = wb.active
            ws.title = "Pouch Master"

            ws.append([
            "Party Name",
                "Party Email",
                "Party Contact",
                "Job Name",
                "Pouch Open Size",
                "Pouch Combination",
                "Purchase Rate / KG",
                "No. of Pouch / KG",
                "Minimum Quantity",
        ])


            for obj in pouch_master_data:
                ws.append([
                    obj.party_details.party_name if obj.party_details else "",
                    obj.party_email.email if obj.party_email else "",
                    obj.party_contact.party_number if obj.party_contact else "",
                    obj.job_name,
                    obj.pouch_open_size,
                    obj.pouch_combination,
                    obj.purchase_rate_per_kg,
                    obj.no_of_pouch_per_kg,
                    obj.minimum_quantity,
                ])

            response = HttpResponse(
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            response["Content-Disposition"] = 'attachment; filename="pouch_master.xlsx"'
            wb.save(response)
            return response
        
            
    

    if request.method == "POST":
        if 'delete_pouch_master' in request.POST:
            try:
                with transaction.atomic():
                    pouch_master_id = request.POST.get('delete_pouch_master')
                    PouchMaster.objects.filter(id=pouch_master_id).delete()
                    messages.success(request, 'Master Data Deleted Successfully')
                    return redirect('view_master_data')
            except Exception as e:
                messages.error(request, str(e))
                return redirect('view_master_data')

        if 'edit_master_data' in request.POST:
            try:

                pouch_master_id = request.POST.get('edit_pouch_master')

                pouch = get_object_or_404(PouchMaster, id=pouch_master_id)
                minimum_quantity = int(request.POST.get('no_of_pouch_per_kg'))*500
                pouch.job_name=request.POST.get('job_name')
                pouch.pouch_open_size=request.POST.get('pouch_open_size')
                pouch.pouch_combination=request.POST.get('pouch_combination')
                pouch.purchase_rate_per_kg=request.POST.get('purchase_rate_per_kg')
                pouch.no_of_pouch_per_kg=request.POST.get('no_of_pouch_per_kg')
                pouch.minimum_quantity=minimum_quantity
                
                pouch.save()
                    
                
                messages.success(request, 'Master Data Updated Successfully')
                return redirect('view_master_data')
            except Exception as e:
                messages.error(request, str(e))
                print("Exception",e)
                return redirect('view_master_data')

    
    paginator = Paginator(pouch_master_data, 10)
    page = request.GET.get('page')
    pouch_master_data = paginator.get_page(page)
   
    context = {
        'pouch_master_data': pouch_master_data,
        'party_name': party_name,
        'job_name': job_name,
    }
    return render(request, "MasterData/view_master_data.html", context)


def master_data_ajax(request):
    party_name = request.GET.get('party_name')
    


    jobs = list(PouchMaster.objects.filter(party_details__party_name=party_name).values_list('job_name', flat=True))
    party_email = list(
        PouchPartyEmail.objects
        .filter(party__party_name=party_name)
        .values_list('email', flat=True)
    )
    print("jobs",jobs)
    party_contact = list(
        PouchPartyContact.objects
        .filter(party__party_name=party_name)
        .values_list('party_number', flat=True)
    )
  
    return JsonResponse({
        'party_email': party_email,
        'party_contact': party_contact,
        'jobs': jobs
    })


    