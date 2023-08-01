from django.urls import path
from .views import ProfileUpdateView, ProfileDetailView, ProfileListView

urlpatterns = [
    path('profile/update', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile/<str:username>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile/search', ProfileListView.as_view(), name='profile-search'),
]