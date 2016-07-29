from __future__ import unicode_literals
from django.db import models
from deepzoom.models import DeepZoom, UploadedImage 

class MyImage(UploadedImage):
    
    mission = models.CharField(max_length = 225, null = True, blank = True)
    role  = models.CharField(max_length = 225, null = True, blank = True)
    frame  = models.CharField(max_length = 225, null = True, blank = True)
