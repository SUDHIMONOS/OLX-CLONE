from django.urls import path
from olx import views

urlpatterns = [
    path("register",views.SignUpView.as_view(),name='signup'),
    path("",views.LoginView.as_view(),name="signin"),
    path("home",views.IndexView.as_view(),name="home"),
    path("profile",views.UserProfileView.as_view(),name="profile"),
    path("products/add",views.ProductCreateView.as_view(),name='add'),
    path('Edit_profile', views.Edit_profile,name='Edit_profile'),
    path("product/detail/<int:id>",views.ProductDetailView.as_view(),name="product-detail"),
    path("olx/signout",views.logout_view,name="signout"),


   
    
   
]
