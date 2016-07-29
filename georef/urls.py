from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import url
from . import views


app_name = 'georef'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^workingversion/$', views.workingVersion, name='working_version'),
    url(r'^newdeepzoom/$', views.deepzoom_new, name='new_deepzoom'),
    url(r'^deepzoomupload/(?P<inst_id>[0-9]+)/$', views.deepzoom_upload, name='upload_deepzoom'),
    url(r'^deepzoomview/(?P<inst_id>[0-9]+)/$', views.deepzoom_view, name='view_deepzoom'),
    url(r'^deepzoom/(?P<passed_slug>\b[a-z0-9\-]+\b)', views._deepzoom, name="a_deepzoom"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
