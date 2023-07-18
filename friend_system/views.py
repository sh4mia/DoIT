from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import UserProfile
from .forms import UserUpdateForm
import sweetify
# Create your views here.

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = UserProfile
    form_class = UserUpdateForm
    template_name = 'base/profile_update.html'
    success_url = reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
    
    def form_valid(self, form):
        sweetify.success(self.request, 'Profile updated succesfully.')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('tasks')