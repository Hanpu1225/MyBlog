from django.db import models
from django.contrib.auth.models import User


#用户拓展信息
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='profile')

    #blank=True时候填写表单不能为空
    phone = models.CharField(max_length=20,blank=True)

    avatar = models.ImageField(upload_to='avatar/%Y%m%d/', blank=True)

    bio = models.TextField(max_length=500,blank=True)

    def __str__(self):
        return 'user {}'.format(self.user.username)