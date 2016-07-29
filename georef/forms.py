from models import *
from django import forms

class UploadedImageForm(forms.ModelForm):
    class Meta:
        model = MyImage
        fields =  ['uploaded_image','name', 'mission', 'role', 'frame' ] 

"""    def save(self, commit = True):
        #get uploaded image
        model_instance = form.save(commit = False)
        image = get_uploaded_image_root(model_instance, model_instance.name)
        #call deep z
"""
