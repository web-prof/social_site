from django.db.models.signals import post_save,pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Profile, Relationship

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Relationship)
def post_save_add_to_friends(sender, instance, created, **kwargs):
    sender_ = instance.sender
    reciever_ = instance.reciever
    if instance.status == 'accepted':
        sender_.friends.add(reciever_.user)
        reciever_.friends.add(sender_.user)
        sender_.save()
        reciever_.save()
@receiver(pre_delete,sender=Relationship)
def pre_delete_remove_from_friends(sender,instance,**kwargs):
    sender_=instance.sender
    reciever_=instance.reciever
    sender_.friends.remove(reciever_.user)
    reciever_.friends.remove(sender_.user)
    sender_.save()
    reciever_.save()
