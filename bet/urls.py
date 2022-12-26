from bet import views
from django.conf import settings
from django.urls import path, include


from rest_framework_simplejwt.views import (
    TokenRefreshView,
)


urlpatterns = [
    path('token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', views.register, name='auth_register'),
    path('on_games/', views.getOnGamesView),
    path('user/', views.currentUser),
    path('match/', views.RecordMatch),
    path('send_notification/', views.Notifications),
    path('test/', views.testEndPoint),

]
