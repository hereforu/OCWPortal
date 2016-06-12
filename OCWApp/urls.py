from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'^uploadcourse/$', views.uploadcourse, name='uploadcourse'),
	url(r'^uploadcourse/uploadresult/$', views.uploadresult, name='uploadresult'),
	url(r'^searchpage/$', views.searchpage, name='searchpage'),
	url(r'^searchresult/(?P<keyword>\w+)/$', views.searchresult, name='searchresult'),
    url(r'^home/$', views.home, name='home'),
    url(r'^classes/$', views.classes, name='classes'),
    url(r'^lecture_tree/(?P<lecture_id>\d+)/$', views.lecture_tree, name='lecture_tree'),
    url(r'^clip/(?P<clip_id>\d+)/$', views.playclip, name='playclip'),
]
