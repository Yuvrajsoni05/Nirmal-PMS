from django.apps import AppConfig


class AppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'app'

    
    # def ready(self):
    #     import app.signals
    
    
    
        #  images = request.FILES.getlist('images')  # Get list of uploaded image files

        # # Save the job details first
        # serializer = JobDetailSerializer(data=mutable_data)
        # if serializer.is_valid():
        #     job_instance = serializer.save()

        #     # Save the images
        #     for img in images:
        #         Jobimage.objects.create(job=job_instance, image=img)