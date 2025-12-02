from datetime import datetime
import random
import requests
import re
import os

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
    date = datetime.now()
    date_s = date.strftime("%Y-%m-%d %H:%M:%S")
    file_dic = {}
    for i, file in enumerate(files):
            _, file_extension = os.path.splitext(file.name)
            random_number = random.randint(1, 1000)
            new_file_name = f"{date_s}_{random_number}{file_extension}"
            file.name = new_file_name
            file_key = f"{new_file_name}"
            file_dic[file_key] = (file.name, file, file.content_type)
    return file_dic
        
     
        
        
        
    
    