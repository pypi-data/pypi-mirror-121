from django.conf.urls import url

from . import views

urlpatterns = [
    url('(?P<submission_id>[0-9]+)/(?P<spam_status>spam|not-spam)/', views.classify, name='classify'),
]
