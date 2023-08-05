from django.shortcuts import redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from friend_system.models import UserProfile
from django.contrib.auth.models import User

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login, authenticate

from django.views import View
from django.db import transaction
from .models import Task
from .forms import PositionForm, TaskForm, CustomUserForm, LoginForm

import sweetify


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    form_class = LoginForm
    redirect_authenticated_user = True

    def form_invalid(self, form):
        sweetify.error(self.request, 'Something went wrong.')
        return self.render_to_response(self.get_context_data(form=form, login_failed=True))
    
    def form_valid(self, form):
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
        if user is not None:
            login(self.request, user)
            sweetify.success(self.request, 'Login successful.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks')
    
class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CustomUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            sweetify.success(self.request, 'Registered successfully.')
        return super(RegisterPage, self).form_valid(form)
    
    def form_invalid(self, form):
        sweetify.error(self.request, 'Something went wrong.')
        return self.render_to_response(self.get_context_data(form=form))

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

from datetime import timedelta
from django.utils import timezone

def update_user_profile_points(user):
    user_profile = user.userprofile
    last_completed_task = Task.objects.filter(user=user, complete=True).latest('created')
    last_task_completed_at = last_completed_task.created if last_completed_task else None

    if last_task_completed_at:
        time_since_last_task = timezone.now() - last_task_completed_at
        if time_since_last_task < timedelta(minutes=30):
            return

    user_profile.points += 3  
    if last_task_completed_at and timezone.now() - last_task_completed_at <= timedelta(days=1):
        user_profile.streak += 1
        if user_profile.streak >= 5:
            user_profile.points += 15
        elif user_profile.streak >= 2:
            user_profile.points += 5
    else:
        user_profile.streak = 1

    user_profile.save()
    
class TaskList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'tasks'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, archived=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        archive_list = ArchiveList()
        archive_list.request = self.request  
        archived_tasks = archive_list.get_queryset().filter(user=self.request.user)
        context['archived_tasks'] = archived_tasks
        
        context['count1'] = archived_tasks.filter(complete=True).count()
        context['count_sum'] = context['count'] + context['count1']
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context

class ArchiveList(LoginRequiredMixin, ListView):
    model = Task
    context_object_name = 'archived_tasks'
    template_name = 'base/archive_list.html'

    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user, archived=True)
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['archived_tasks'] = context['archived_tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        return context
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = 'task'
    template_name = 'base/task.html'

class TaskCreate(LoginRequiredMixin, CreateView):
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    template_name = 'base/task_form.html'
    def form_valid(self, form):
        form.instance.user = self.request.user
        if form.instance.complete:
            form.instance.archived = True
            update_user_profile_points(self.request.user)
        sweetify.success(self.request, 'Task created succesfully.')
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'base/task_form.html'
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        if form.instance.complete:
            form.instance.archived = True
            update_user_profile_points(self.request.user)
        sweetify.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)

class DeleteView(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)
    def form_valid(self, form):
        sweetify.success(self.request, 'Task deleted successfully.')
        return super().form_valid(form)

class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('tasks'))
    

