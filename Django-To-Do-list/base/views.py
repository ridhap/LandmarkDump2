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

from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    

    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username == '':
            messages.add_message(request, messages.ERROR,
                                 'Username is required')
            context['has_error'] = True
        if password == '':
            messages.add_message(request, messages.ERROR,
                                 'Password is required')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password)

        if not user and not context['has_error']:
            messages.add_message(request, messages.ERROR, 'Invalid login! Please enter the right password')
            context['has_error'] = True

        if context['has_error']:
            return render(request, 'base/linker2.html', status=401, context=context)
        login(request, user)
        return redirect('tasks')
        
    def get_success_url(self):
        return reverse_lazy('tasks')

    

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')
    
    def post(self, request):
        context = {
            'data': request.POST,
            'has_error': False
        }

        # email = request.POST.get('email')
        username = request.POST.get('username')
        print(username)
        # full_name = request.POST.get('name')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        # password=str(password)
        print( 'password',password)
        print('password2',password2)
        if len(password2) < 6:
            messages.add_message(request, messages.ERROR,
                                 'passwords should be atleast 6 characters long')
            context['has_error'] = True
        if password != password2:
            messages.add_message(request, messages.ERROR,
                                 'passwords dont match')
            context['has_error'] = True
        user = authenticate(request, username=username, password=password2)     

        try:
            if User.objects.get(username=username):
                messages.add_message(
                    request, messages.ERROR, 'Username is taken')
                context['has_error'] = True

        except Exception as identifier:
            pass
        if context['has_error']:
            return render(request, 'base/linker.html',status=401, context=context)
        user = User.objects.create_user(username=username,password=password2)
        user= user.save()
        return redirect('tasks')

        
    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        else:
            return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated :
            return redirect('tasks')
        else:
            return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
