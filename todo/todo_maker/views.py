from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from todo_maker.models import Task
from todo_maker.forms import TaskCreateForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.models import User



from django.shortcuts import render, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Imports for Reordering Feature
from django.views import View
from django.shortcuts import redirect
from django.db import transaction

from .models import Task
from .forms import PositionForm




# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'todo_maker/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('tasks')


class RegisterPage(FormView):
    template_name = 'todo_maker/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)



class List(View):
    template = "todo_maker/list.html"
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__contains=search_input)

        context['search_input'] = search_input

    # def get(self, request, *args, **kwargs):
    #     instance = None
    #     if kwargs.get('pk', None):
    #         try:
    #             instance = Task.objects.filter(pk=kwargs.get('pk', None))[0]
    #         except Exception:
    #             instance = None

    #     # delete_id = kwargs.get('delete_id', None)
        
    #     if kwargs.get('pk', None):
    #         try:
    #             obj = Task.objects.filter(pk=kwargs.get('pk', None))[0]
    #             obj.delete()
    #             messages.add_message(request, messages.SUCCESS, "Task removed successfully.")
    #         except Exception:
    #             pass
                
    #     form = TaskCreateForm(instance=instance)
    #     context = {
    #         "tasks" : Task.objects.filter().order_by('task_accomplished'),
    #         "form" : form,
    #     }

    #     return render(request, self.template, context)
    
    def post(self, request, *args, **kwargs):
        instance = None
        post  = request.POST.copy()
        pk = post.get('id', None)
        
        msg = "New Task Created..."
        if pk:
            try:
                msg = "Task Updated..."
                instance = Task.objects.filter(pk=pk)[0]
            except Exception:
                instance = None

        form = TaskCreateForm(post, instance=instance)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.save()
            messages.add_message(request, messages.SUCCESS, msg)
        else:
            messages.add_message(request, messages.ERROR, "Please fill * marked fields")
            
        # url = reverse("todo_maker:list-todo")
        return redirect("todo_maker:list-todo")


# def registerPage(request):
#     return render(request, 'content.html')



# def next(request):
#         name=request.POST['name']
#         email=request.POST['email']
#         password=request.POST['pwd']
#         user = User.objects.create_user(name, email, password)
#         user.last_name = request.POST['lname']
#         user.save()
#         return render(request,'todo_maker/list.html',{'name':name})