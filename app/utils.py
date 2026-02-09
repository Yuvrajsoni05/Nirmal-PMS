from datetime import datetime
import random
import requests
import re
import os
from .models import *
from app.models import Registration





def email_validator(email):
 
    email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex,email):       
        return "Enter a Valid email Address"



def phone_number_check(number):
    number_regex = r"^((091|\+91)?|(\(091\)|\(+91\))|(91)?|\(91\)|0)?[ ]?[6-9]\d{9}$"
    if not re.match(number_regex,number):
        return "Enter a Valid Mobile Number"

def email_check(email):
    if Registration.objects.filter(email=email).exists():
        return "Email is Already Exist"
    

def validator_password(password):
    if len(password) < 8:
        return "Password Must be at least 8 characters long"
    
    if not any(char.isupper() for char in password):
        return "Password must contain at least one uppercase "
    if not any(char.islower() for char in password):
         return "Password must contain at least one lowercase"
     
    if not any(char.isdigit() for char in password):
        return "Password must contain at least one number"
    
    if not any(char in "!@#$%^&*()_+-={}[]\\:;\"'<>,.?/~`" for char in password):
        return "Password must contain at least one special character."
    
    
valid_extension = [".jpeg", ".jpg", ".png", ".ai",".cdr" ,".JPEG", ".JPG", ".PNG", ".AI", ".CDR"]  
def file_validation(files):

    for file in files:
        ext = os.path.splitext(file.name)[1].lower()  
        if not ext:
            return "Invalid file. File must have an extension."

        if ext not in valid_extension:
            return "Invalid file. Only .jpg, .jpeg, .png, and .ai are allowed"
        


def file_name_convert(files):
    converted_files = []

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    for file in files:
        _, ext = os.path.splitext(file.name)
        short_uuid = uuid.uuid4().hex[:4] 
        new_name = f"{timestamp}_{short_uuid}{ext}"
        
        file.name = new_name
        converted_files.append(file)

    return converted_files
    
def all_job_name_list(party_name):
    try:
        party =  Party.objects.get(party_name=party_name)
    except Party.DoesNotExist:
        return []
    
    if party:
        job_qs = Job_detail.objects.filter(party_details__party_name = party).values("job_name").distinct()
        job_qs = job_qs.union(
            ProformaJob.objects.filter(proforma_invoice__party_details__party_name=party)
            .values("job_name").distinct().union(CDRDetail.objects.filter(
                party_details__party_name=party
            ).values("job_name").distinct())
        )
    else :
        job_qs = ''
        
    return job_qs


def email_attachment_size(total_attachment_size):
    MAX_SIZE_MB =  25
    if total_attachment_size > MAX_SIZE_MB * 1024 * 1024:
        return f"Total file size exceeds {MAX_SIZE_MB}MB. Please upload smaller files."
    return None
    
    
    
    
    
    
    
def get_or_create_party(party_name, party_email, party_contact):
    party_details, _ = PouchParty.objects.get_or_create(
        party_name=party_name.strip()
    )

    party_email_obj, _ = PouchPartyEmail.objects.get_or_create(
        party=party_details,
        email=party_email
    )

    party_contact_obj, _ = PouchPartyContact.objects.get_or_create(
        party=party_details,
        party_number=party_contact
    )

    return party_details, party_email_obj, party_contact_obj