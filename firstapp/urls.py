
from django.urls import path
from . import views

urlpatterns = [
    path('', views.Index.as_view(), name = 'index'),
    # path('contactus/', views.contactus2, name = 'contact'),
    path('contactus/', views.ContanctUs.as_view(), name= 'contactclass'),
    path('signup/',views.RegisterView.as_view(), name = "signup"),
    path('signup/', views.RegisterView.as_view(), name="signup"),
    path('login/', views.LoginViewUser.as_view(), name="login"),
    path('logout/', views.LogoutViewUser.as_view(), name="logout"),
    path('signupseller/', views.RegisterViewSeller.as_view(), name= "login1"),
]