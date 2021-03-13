from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class Author(AbstractUser):
    following = models.ManyToManyField('Author',related_name="followieng",null=True,blank=True)
    followers = models.ManyToManyField('Author',related_name="followees",null=True,blank=True)
    profile  = models.ImageField(null=True,blank=True)
    # image

class Blog(models.Model):
    title       = models.CharField(max_length=300)
    content     = models.TextField()
    creator     = models.ForeignKey(Author,on_delete=models.CASCADE,related_name="blogs")
    published   = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)
    # tag
    

    class Meta:
        ordering = ['-created_at']