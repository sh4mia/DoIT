from django.views.generic.edit import UpdateView
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm
from base.models import Task

import sweetify
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    profile_form_class = ProfileUpdateForm  # Dodaj formularz dla UserProfile
    template_name = 'base/profile_update.html'
    success_url = reverse_lazy('tasks')

    def get_object(self, queryset=None):
        return self.request.user.userprofile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['form'] = self.form_class(self.request.POST, instance=self.request.user)
            context['profile_form'] = self.profile_form_class(
                self.request.POST, self.request.FILES, instance=self.request.user.userprofile
            )
        else:
            context['form'] = self.form_class(instance=self.request.user)
            context['profile_form'] = self.profile_form_class(instance=self.request.user.userprofile)
        return context

    def form_valid(self, form):
        user_form = self.form_class(self.request.POST, instance=self.request.user)
        profile_form = self.profile_form_class(
            self.request.POST, self.request.FILES, instance=self.request.user.userprofile
        )
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            sweetify.success(self.request, 'Profile updated successfully.')
        return super().form_valid(form)

    def get_success_url(self):
        return self.success_url
    

class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = UserProfile
    template_name = 'base/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        username = self.kwargs.get('username')
        return UserProfile.objects.get(user__username=username)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_profile = context['profile']

        # Pobierz ilość wykonanych zadań przez użytkownika (profil)
        completed_tasks_count = Task.objects.filter(user_id=user_profile.user_id, complete=True).count()

        context['completed_tasks_count'] = completed_tasks_count
        return context

class ProfileListView(LoginRequiredMixin, ListView):
    model = UserProfile
    template_name = 'base/profile_list.html'
    context_object_name = 'profiles'
    
    def get_queryset(self):
        search_query = self.request.GET.get('search-area')
        if search_query:
            return self.model.objects.filter(user__username__icontains=search_query)
        return self.model.objects.none()