#coding...
#↑これpython2だと日本語入力のとき必要だがpython3ではいらんらしい

#importできなくてerrorになっていた
from django.conf import settings
from django.db import models
from django.utils import timezone


class Post(models.Model):#今回のモデルを定義する
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):#ブログを公開するメソッド
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
# Create your models here.
