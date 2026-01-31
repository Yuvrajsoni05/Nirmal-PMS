from .common_imports import *





def master_page(request):
    pouch_party = PouchParty.objects.all()
    pouch_party_contact = PouchPartyContact.objects.all()
    pouch_party_email = PouchPartyEmail.objects.all()
    pouch_quotation = PouchQuotation.objects.all()
    pouch_quotation_job = PouchQuotationJob.objects.all()

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
                            party=party_details ,party_number=party_contact  )

            for i in range(len(job_name)):
                PouchMaster.objects.create(
                    job_name=job_name[i],
                    pouch_open_size=pouch_open_size[i],
                    pouch_combination=pouch_combination[i],
                    purchase_rate_per_kg=purchase_rate_per_kg[i],
                    no_of_pouch_per_kg=no_of_pouch_per_kg[i],
                    party_details=party_details,
                    party_contact=party_contact_obj,
                    party_email=party_email_obj,
                    minimum_quantity= no_of_pouch_per_kg[i]*500
                )
            messages.success(request, 'Master Data Created Successfully')
            return redirect('master_page')


    context = {
        'pouch_party': pouch_party,
        'pouch_party_contact': pouch_party_contact,
        'pouch_party_email': pouch_party_email,
        'pouch_quotation': pouch_quotation,
        'pouch_quotation_job': pouch_quotation_job,
    }
    return render(request, "MasterData/master_page.html", context)



def master_data_ajax(request):
    party_name = request.GET.get('party_name')

    party_email = list(
        PouchPartyEmail.objects
        .filter(party__party_name=party_name)
        .values_list('email', flat=True)
    )

    party_contact = list(
        PouchPartyContact.objects
        .filter(party__party_name=party_name)
        .values_list('party_number', flat=True)
    )
  
    return JsonResponse({
        'party_email': party_email,
        'party_contact': party_contact
    })


    