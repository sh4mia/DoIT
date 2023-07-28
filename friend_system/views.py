from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserUpdateForm, ProfileUpdateForm

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