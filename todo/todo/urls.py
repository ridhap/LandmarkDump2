from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('',include('test1.urls')),
    path('admin/', admin.site.urls),
    path('', include('todo_maker.urls',namespace='todo_maker')), 
    
]   