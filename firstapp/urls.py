
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    # path('contactus/', views.contactus2, name = 'contact'),
    path('contactus/', views.ContanctUs.as_view(), name= 'contactclass'),
    path('signup/',views.RegisterView.as_view(), name = "signup"),
]