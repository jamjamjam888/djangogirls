from django.test import TestCase

# Create your tests here.
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


class QuestionModelTests(TestCase):#django.test.TestCaseを継承したサブクラス。未来の日付のpub_dateを持つQuestionのインスタンスを生成するメソッドを持つ

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(days=30)#今日から30日後の日付を生成
        future_question = Question(pub_date=time)#pub_dateフィールドに30日後の日付を持つQuestionインスタンスが作成される
        self.assertIs(future_question.was_published_recently(), False)#assertIsメソッド
        #pythonの標準関数。
        #ここではfuture_question.was_published_recently()がFalseを返すことを期待しており、第二引数でFalseにしている。
        #しかし、今のコードでは未来のQuestionに対してもTrueを返すようなコードのため、実際にはTrueで返ってくる。
        #assertIs()で期待される戻り値はFalseに対し、実際の戻り値はTrueとなっているため、これはバグである。この部分を検知してくれる
    def test_was_published_recently_with_old_question(self):
        #Questionが前日より前のときFalseを返す
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        #一日以内にpublishされたQuestionに対してはTrueを返す
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

def create_question(question_text, days):#questionのショートカット関数
    #与えられたquestion_textとdaysのフィールドを持つQuestionを生成.
    #この関数を下のクラスで呼び出して使う！
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexView(TestCase):#TestCaseからの継承クラス
    def test_index_view_with_no_questions(self):#公式ドキュメントの参考コードでの関数名と説明文中での関数名が違うので注意
        #もしQuestionが存在しなければ適切なメッセージが表示される
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are avairable.")
        self.assertQuerysetEqual(response.context['latest_question_list'],[])

    def test_past_question(self):
        #過去のQuestionがindex pageに表示されるかのテスト
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )
    
    def test_future_question(self):
        #未来のQuestionをindex pageに表示しないかのテスト
        create_question(question_text='Future question.', days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are avairable.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_question(self):
        #過去と未来の質問が存在する場合、過去の質問のみを表示する
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        #
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )

class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        #publishされた日付を伴う未来のQuestionの詳細には404エラーを返す
        future_question = create_question(question_text='Future question.', days=5)
        url = reverse('polls:detail', args=(future_question.id,))#←
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        #日付を伴う過去のQuestionの詳細なview
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
