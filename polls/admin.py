from django.contrib import admin

from .models import Question
#なぜ.modelsなのか?


# Register your models here.
#pollsアプリはadminのインデックスページから確認できない
#Questionオブジェクトがadminのインターフェースを持つということをadminに伝えてやる必要がある
#admin.site.register(Question)
