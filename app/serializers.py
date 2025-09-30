from django.db.models import ImageField
from rest_framework import serializers


from .models import *



class JobImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Jobimage
        fields = '__all__'



class JobDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(required=False, allow_null=True)
    images = JobImageSerializer(many=True, read_only=True, source='image')

    class Meta:
        model = Job_detail
        # fields = '__all__'
        exclude = ['id' ,'created_at']
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
    # def create(self, validated_data):
    #     uploaded_images = validated_data.pop('uploaded_images', [])
    #     job_instance = Job_detail.objects.create(**validated_data)
        
    #     for image in uploaded_images:
    #         Jobimage.objects.create(job=job_instance, image=image)
        
    #     return job_instance
    # def validate_job_name(self,data):
    #     job_name = data
    #     date = self.initial_data.get('date')
        
    #     # if Job_detail.objects.filter(job_name__icontains=job_name, date__icontains=date).exists():
    #     #     raise serializers.ValidationError("Job Name already exists on this date. Kindly update the job.")
    #     # else:
    #     #     return data
    
    # def update(self, instance, validated_data):

    #     restricted_fields = ['job_name']  
        
    #     for field in restricted_fields:
    #         if field in validated_data:
    #             validated_data.pop(field)
 
 
    #     for field, value in validated_data.items():
    #         setattr(instance, field, value)
    #     instance.save()
    #     return instance
    
    
    
