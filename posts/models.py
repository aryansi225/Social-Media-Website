from django.db import models
from django.urls import reverse
from django.conf import settings
import markdown2
from groups.models import Group
from django.contrib.auth import get_user_model
User = get_user_model()
# Create your models here.

class Post(models.Model):
    user = models.ForeignKey(User, related_name='posts', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now=True)
    message = models.TextField()
    message_html = models.TextField(editable=False)
    group = models.ForeignKey(Group, related_name='posts', on_delete=models.PROTECT, null=True, blank=True)

    def __str__(self):
        return self.message
    def __save__(self,*args,**kwargs):
        self.message_html = markdown2.markdown(self.message)
        super().save(*args,**kwargs)
    def get_absolute_url(self):
        return reverse('posts:single', kwargs={'username':self.user.username,
                                                'pk':self.pk})
    class Meta:
        ordering = ['-created_at']
        unique_together = ['user','message']