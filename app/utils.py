import requests
import re
import os

from app.models import Registration










def email_validator(email):
    email_regex = r"(?!.*([.-])\1)(?!.*([.-])$)(?!.*[.-]$)(?!.*[.-]{2})[a-zA-Z0-9_%+-][a-zA-Z0-9._%+-]*@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_regex,email):       
        return "Enter a Valid email Address"
    
    
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
    
    
    
    
    
valid_extension = [".jpeg", ".jpg", ".png", ".ai"]  
def file_validation(files):
    if len(files) > 2:
        return "You can upload only 2 files"
    
    for file in files:
        ext = os.path.splitext(file.name)[1].lower()  
        if not ext:
            return "Invalid file. File must have an extension."
        
        if ext not in valid_extension:
            return "Invalid file. Only .jpg, .jpeg, .png, and .ai are allowed"
        
        
        
    
    