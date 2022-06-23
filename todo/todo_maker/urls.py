
from django.urls import path, include
from todo_maker import views 
from django.contrib.auth.views import LogoutView
app_name='todo_maker'

urlpatterns = [

    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', views.RegisterPage.as_view(), name='register'),

    # path('', views.List.as_view(),name="list-todo"),
    # path('save', views.List.as_view(),name="save-todo"),
    # path('edit/<int:pk>/', views.List.as_view(),name="edit-todo"),
    # path('remove/<int:pk>/', views.List.as_view(),name="remove-todo"),
    # path('task-completed', views.List.as_view(),name="todo-task-completed"),
   
]   