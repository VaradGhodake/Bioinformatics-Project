from django.conf.urls import url
from . import views


app_name = 'info'

urlpatterns = [
    url(r'^$', views.index, name = "index"),
    url(r'^computational_biology/index.html$', views.cb, name = "computational_biology"),
    url(r'^genomics/index.html$', views.genomics, name = "genomics"),
    url(r'^proteinomics/index.html$', views.proteinomics, name = "proteinomics"),    
    url(r'^computational_biology/bio1.jpg$', views.cbinfo, name = "cbinfo"),
    url(r'^genomics/bio1.jpg$', views.geninfo, name = "geninfo"),
    url(r'^proteinomics/bio1.jpg$', views.proteininfo, name = "proteininfo"),
]

