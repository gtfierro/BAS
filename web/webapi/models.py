from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Here, we extend the base Django User model so we can access/create
# additional fields. From http://blog.tivix.com/2012/01/06/extending-user-model-in-django/
class UserProfile(models.Model):
    user = models.OneToOneField(User)
    apikey = models.CharField(max_length=32, unique=True)
    #other fields here

    def __str__(self):
        return "%s's profile" % self.user

def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile, created = UserProfile.objects.get_or_create(user=instance)

post_save.connect(create_user_profile, sender=User)
