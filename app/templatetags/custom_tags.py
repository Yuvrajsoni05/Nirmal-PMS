import os
from django import template
from datetime import datetime

register  = template.Library()


@register.filter
def indian_currency_format(value):
    try:
       
        num = float(value) 
        
        
        integer_part, decimal_part = str(num).split('.') 
        
    
        formatted_integer = ""
        
     
        formatted_integer = integer_part[-3:]  
        
        
        remaining_integer = integer_part[:-3] 
        
        while len(remaining_integer) > 0:
            if len(remaining_integer) > 2:
                formatted_integer = remaining_integer[-2:] + "," + formatted_integer
                remaining_integer = remaining_integer[:-2]
            else:
                formatted_integer = remaining_integer + "," + formatted_integer
                remaining_integer = ""

     
        if decimal_part:
            return formatted_integer + "." + decimal_part
        else:
            return formatted_integer

    except (ValueError, TypeError):
        return value

@register.filter
def split_text(value):
    return value.split('+')

@register.filter
def split_text_with_multiplications(value):
    return [int(p) for p in value.split('X')]





@register.filter
def filename(value):
    return os.path.basename(value)



@register.filter
def gst_value(value):
    if not value:
        return []

    gst_list = [g.strip() for g in value.strip("[]").replace("'", "").split(",")]



    return gst_list