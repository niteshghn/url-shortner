from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class UrlKeyHash(models.Model):
    key = models.CharField(max_length=16, db_index=True, primary_key=True)
    url = models.TextField()
    user = models.ForeignKey(User, on_delete=models.PROTECT,null=True)
    created_on = models.DateTimeField(auto_now_add=True)
    is_private = models.BooleanField(default=False)
    hits = models.IntegerField(default=0)


class UrlHitLog(models.Model):
    url = models.ForeignKey(UrlKeyHash, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
