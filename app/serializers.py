from email.mime import image
from importlib.util import source_hash
from pyexpat import model
from django.db.models import ImageField
from rest_framework.serializers import ModelSerializer
from django.forms import fields
from rest_framework import serializers


from .models import *
from app.models import CDRImage





class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobimage
        fields = '__all__'



class JobDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False, allow_null=True)
    images = JobImageSerializer(many=True, read_only=True, source='image') 

    class Meta:
        model = Job_detail
 
        exclude = ['created_at']
        extra_kwargs = {
            'company_name': {'required': False, 'allow_blank': True},
            'date': {'required': False, 'allow_null': True},
            'bill_no': {'required': False, 'allow_blank': True},
            'job_name': {'required': False, 'allow_blank': True},
            'job_type': {'required': False, 'allow_blank': True},
            'noc': {'required': False, 'allow_blank': True},
            'prpc_purchase': {'required': False, 'allow_blank': True},
            'prpc_sell': {'required': False, 'allow_blank': True},
            'cylinder_size': {'required': False, 'allow_blank': True},
            'cylinder_made_in': {'required': False, 'allow_blank': True},
            'pouch_size': {'required': False, 'allow_blank': True},
            'pouch_open_size': {'required': False, 'allow_blank': True},
            'pouch_combination': {'required': False, 'allow_blank': True},
            'correction': {'required': False, 'allow_blank': True},
            'folder_url': {'required': False, 'allow_blank': True},
            'image_links': {'required': False, 'allow_blank': True},
            'cylinder_date': {'required': False, 'allow_null': True},
            'cylinder_bill_no': {'required': False, 'allow_blank': True},
            'job_status': {'required': False, 'allow_blank': True}
        }
        
class JobUpdateSerializer(serializers.ModelSerializer):
    images = JobImageSerializer(many=True, read_only=True, source='image') 
    class Meta:
        model= Job_detail
        
        exclude = ['id' ,'created_at','job_name','company_name','cylinder_size','pouch_size']
        
        extra_kwargs = {
            
            'date': {'required': False, 'allow_null': True},
            'bill_no': {'required': False, 'allow_blank': True},
            'job_type': {'required': False, 'allow_blank': True},
            'noc': {'required': False, 'allow_blank': True},
            'prpc_purchase': {'required': False, 'allow_blank': True},
            'prpc_sell': {'required': False, 'allow_blank': True},
            'cylinder_made_in': {'required': False, 'allow_blank': True},
            'pouch_open_size': {'required': False, 'allow_blank': True},
            'pouch_combination': {'required': False, 'allow_blank': True},
            'correction': {'required': False, 'allow_blank': True},
            'folder_url': {'required': False, 'allow_blank': True},
            'image_links': {'required': False, 'allow_blank': True},
            'cylinder_date': {'required': False, 'allow_null': True},
            'cylinder_bill_no': {'required': False, 'allow_blank': True},
            'job_status': {'required': False, 'allow_blank': True}
        }
        
        
#CDR  Serializer


class CDRImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CDRImage
        exclude = ['id']
        
        
class CDRDataSerializer(serializers.ModelSerializer):
    image = CDRImageSerializer(many=True, read_only=True,source='cdr_images')
    class Meta:
        model = CDRDetail
        exclude = ['id']


class CDRUpdateSerializer(serializers.ModelSerializer):
    image = CDRImageSerializer(many=True, read_only=True, source='image')
    class Meta:
        model = CDRDetail
        fields = '__all__'
        
        