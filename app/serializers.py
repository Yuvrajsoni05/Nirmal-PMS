from rest_framework import serializers
from .models import *



class JobDetailSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Job_detail
        # fields = '__all__'
        exclude = ['id' ,'created_at']
        
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