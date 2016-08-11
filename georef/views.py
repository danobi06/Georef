import os
import operator
from PIL import Image
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from deepzoom.models import DeepZoom, UploadedImage 
from georef.forms import *


def autoenhance(im): 
    h = im.convert("L").histogram()
    lut = []
    for b in range(0, len(h), 256):
        # step size
        step = reduce(operator.add, h[b:b+256]) / 255
        # create equalization lookup table
        n = 0
        for i in range(256):
            lut.append(n / step)
            n = n + h[i+b]
        # map image through lookup table
        return im.point(lut*im.layers)

def index(request):
    if request.POST: 
        #if post is a cancel, refresh page
        if request.POST.get("cancel"):
            return HttpResponseRedirect('/georef/newdeepzoom/')
        #else request was a save
        form = UploadedImageForm(request.POST, request.FILES)
        if form.is_valid():
            print 'valid'
            model_inst = form.save() #saves form
            #change fields for enhanced deepzoom
            model_inst_enh = MyImage(uploaded_image = model_inst.uploaded_image.path, name = model_inst.name + '_enh', mission = model_inst.mission + '_enh'
                    , role = model_inst.role + '_enh', frame = model_inst.frame + '_enh')
            model_inst_enh.save()

            model_inst.create_deepzoom_image() #creates ordinary deepzoom
            model_inst_enh.create_deepzoom_image() # creates deepzoom for enhancement of tiles

            #apply autoenhanced to each tile in deepzoom
            tile_path = settings.MEDIA_ROOT + "deepzoom_images/"+ model_inst_enh.name +"/"+ model_inst_enh.name + "_files" 
            print tile_path
            for root, dirs, tiles in os.walk(tile_path):
                for tile in tiles: # we want to enhance each tile in the list of tiles
                   # print os.path.join(root, tile)
                    enhanced_image = autoenhance(Image.open(os.path.join(root, tile)))
                    enhanced_image.save(tile)

            return redirect('/georef/viewer/%s/' % model_inst.name) 
    #form with no data
    form = UploadedImageForm() 
    return render(request, 'georef/index.html', {'form': form})

def viewer(request, m_name=None):
    model_inst = get_object_or_404(MyImage, name = m_name)
    model_inst_enh = get_object_or_404(MyImage, id = model_inst.id + 1) #the enhanced model is the follwing model from the original

    return render(request, 'georef/viewer.html', {'model_inst': model_inst, 'model_inst_enh': model_inst_enh})




