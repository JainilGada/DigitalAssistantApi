from django.conf.urls import url
from .views import FileView,ProductView
urlpatterns = [
  url(r'^upload/$', FileView.as_view(), name='file-upload'),
  url(r'^product/$', ProductView.as_view(), name='get-product')
]