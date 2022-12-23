from django.contrib import admin
from django.urls import path, include, re_path
import notifications_rest.urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bet.urls')),
    re_path('^notifications/', include(notifications_rest.urls)),
]
