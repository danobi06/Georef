import os
import operator
from PIL import Image
from django.conf import settings
from django.core.files import File
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from deepzoom.models import DeepZoom, UploadedImage 
from georef.forms import *

def index(request):
    return render(request, 'georef/index.html')

def workingVersion(request):
    return render(request, 'georef/workingVersion.html')

def deepzoom_new(request):
    if request.POST: 
        #if post is a cancel, refresh page
        if request.POST.get("cancel"):
            return HttpResponseRedirect('/georef/newdeepzoom/')
        #else request was a save and continue
        form = UploadedImageForm(request.POST, request.FILES)
        if form.is_valid():
            model_inst = form.save() #saves image
        #    model_inst.create_deepzoom_image() #turns image into deepzoom file 
            # return deepzoom_upload(request, model_inst.id)
            #return render(request, 'georef/deepzoom_upload.html', {'model_inst': model_inst})
            return redirect('/georef/deepzoomupload/%s/' % model_inst.id)
    #form with no data
    form = UploadedImageForm() 
    return render(request, 'georef/deepzoom_new.html', {'form': form})


"""def deepzoom_new(request):
    if request.POST: 
        #if post is a cancel, refresh page
        if request.POST.get("cancel"):
            return HttpResponseRedirect('/georef/newdeepzoom/')
        #else request was a save
        form = UploadedImageForm(request.POST, request.FILES)
        if form.is_valid():
            model_instance = form.save() #saves image
            model_instance.create_deepzoom_image() #turns image into deepzoom file 
            return render(request, 'georef/deepzoom_upload.html', {'uploaded': True, 'model_instance': model_instance})
            #return deepzoom_upload(request, model_instance.id)
    #form with no data
    form = UploadedImageForm() 
    return render(request, 'georef/deepzoom_new.html', {'form': form})
"""
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

def deepzoom_upload(request, inst_id = None):
    model_inst = get_object_or_404(MyImage, id = inst_id)
    print model_inst.uploaded_image.name

#    model_inst.create_deepzoom_image()
    enhanced = False
    create_deepzoom = False
    if request.POST:
        if request.POST.get("cancel"):
            return HttpResponseRedirect('/georef/newdeepzoom/')

        if request.POST.get("auto_enhance"):
            #auto enchance model_inst
            enhanced = True
            print request.POST.get("auto_enhance")
        if request.POST.get("deepzoom"):
            create_deepzoom = True
            print request.POST.get("deepzoom")
            print create_deepzoom

        if request.POST.get("deepzoom_enhanced"):
            enhanced = True
            create_deepzoom = True
            print request.POST.get("deepzoom_enhanced")

        if request.POST.get("save"):
            print request.POST.get("save")   
            print 'created deepzoom'
            print enhanced
            print create_deepzoom
            if enhanced and not create_deepzoom:
                img = Image.open(model_inst.uploaded_image)
                enhanced_image = autoenhance(img)
                en_name = model_inst.name + "_enhanced" + ".jpg"
                img_path = settings.MEDIA_ROOT +  settings.UPLOADEDIMAGE_ROOT + "/" + en_name 
                enhanced_image.save(img_path)
                model_inst.uploaded_image = settings.UPLOADEDIMAGE_ROOT + "/" + en_name 
                model_inst.save()
                print 'saved img enhance'
            if not enhanced and create_deepzoom:
                model_inst.create_deepzoom_image()
                print "DEEPZOOM Created"

            if enhanced and create_deepzoom:
                model_inst.create_deepzoom_image()
                print 'enhance Deepzoom Created'
                #apply autoenhanced to each tile in deepzoom
                tile_path = settings.MEDIA_ROOT + "/deepzoom_images"+ model_inst.name +"/"+ model_inst.name + "_files" 

                for root, dirs, img in os.walk(tile_path):
                    enhanced_image = autoenhance(File(open(img)))
                    enhanced_image.save(img)
            return deepzoom_view(request, model_inst.id) 

    #else no request, send rendered html page
    return render(request, 'georef/deepzoom_upload.html', {'model_inst': model_inst})

def deepzoom_view(request, inst_id=None):
    model_inst = get_object_or_404(MyImage, id = inst_id)
    return render(request, 'georef/img.html', {'model_inst': model_inst})

def _deepzoom(request, passed_slug=None):

    _deepzppm_obj = get_object_or_404(DeepZoom, slug = passed_slug)

    return render(request, 'deepzoom.html', {'deepzoomobj': _deepzoom_obj})
