from django.conf.urls import url
from . import views


app_name = 'georef'
urlpatterns = [
    url(r'^index/$', views.index, name='index'),
    url(r'^viewer/(?P<m_name>\b[a-z0-9\-]+\b)/$', views.viewer, name='viewer'),

]


