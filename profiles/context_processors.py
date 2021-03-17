from .models import Profile,Relationship


def ava_context(request):
    if request.user.is_authenticated:
        prof_instance=Profile.objects.get(user=request.user)
        prof_avatar=prof_instance.avatar
        return{'avatar_pic':prof_avatar}
    return {}


def invitation_recieved_count(request):
    if request.user.is_authenticated:
        prof_instance = Profile.objects.get(user=request.user)
        rel_invitation_recieved=Relationship.objects.invitation_recieved(prof_instance).count()
        return {'invitations_no':rel_invitation_recieved}
    else:
        return {}
