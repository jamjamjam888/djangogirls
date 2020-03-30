import datetime

from django.db import models
from django.utils import timezone
#djangoのタイムゾーン関連ユーティリティを参照する
# Create your models here.
"""
pollsアプリケーションでは
Question
Choice
の2つのモデルを作成する

Pollにはquestionとpublication dateの情報がある

Choiceには選択肢のテキストとvoteという2つのフィールドがある
各Choiceは一つのQuestion関連づいている
"""

#tutorialを実装
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        #strメソッド
        return self.question_text
        #
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    #ForeignKey:外部キー
    #on_delite=models.CASCADE:多対1のリレーション。リレーションシップフィールドと呼ぶ。
    def __str__(self):
        #strメソッド
        return self.choice_text

"""
-memo-
各モデルは一つのクラスで表現され、いずれもdjango.db.models.Modelのサブクラス
各フィールドはFieldクラスのインスタンスとして表現されている
ex)
CharField:文字のフィールド。※max_lengthを必須の引数として持つので注意！
DateTimeField:日時のフィールド
IntegerField:整数のフィールド。オプションとして引数を持たせることができる。今回はvotesのdefault値を0としている

Fieldインスタンスそれぞれの名前(question_text,pub_date)は機械可読なフィールド。人間可読なフィールドにしても問題はない。


"""