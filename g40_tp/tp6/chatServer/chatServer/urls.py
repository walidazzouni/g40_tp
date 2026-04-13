from django.contrib import admin
from django.urls import path, include

handler404 = 'g40aChat.views.page_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('chat/', include('g40aChat.urls')),
]