from django.urls import path
from users import views

urlpatterns = [
    path('',views.profiles,name="profiles"),
    path('profile/<str:pk>/',views.userProfile,name="user-profile"),
    path('login/',views.loginUser,name="login"),
    path('logout/',views.logoutUser,name="logout"),
]