from django.urls import path
from user_auth.views.views import UserListView , RegisterView , LoginView , LogoutView



urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    #path('profile/', views.ProfileView, name='profile'),
    
]