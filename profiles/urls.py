from django.urls import path
from .views import *

app_name = 'profiles'
urlpatterns = [
    path('myprofile', my_profile, name='myprofile'),
    path('profile_detail/<slug>/',profiles_detail_view.as_view(),name='profile_detail'),
    path('my_invites/',invite_recieved_view,name='my_invites'),
    path('all_profiles/',all_profiles,name='all_profiles'),
    path('profiles_available_for_inviting/',profiles_available_for_inviting.as_view(),name='profiles_available_for_inviting'),
    path('send_invitation/',send_invitation,name='send_invitation'),
    path('remove_friend/',remove_from_friends,name='remove_friend'),
    path('my_invites/accept/',accept_invitation,name='accept_invitation'),
    path('my_invites/reject/',reject_invitation,name='reject_invitation'),
]
