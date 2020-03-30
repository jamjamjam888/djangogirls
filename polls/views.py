from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.http import HttpResponseRedirect
#from django.template import loader
#from django.http import Http404
from django.urls import reverse
from django.views import generic

from .models import Choice, Question

#汎用ビューを使う
class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #例外処理
    except (KeyError, Choice.DoesNotExist):
        #Resdisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing
        #with Postdata. This prevents data from being posted twice if a user hit the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))


"""
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('polls/index.html')
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html',context)
#このコードは、polls/index.htmlというテンプレートをロードしそこにコンテキストを渡す


def detail(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
    return render(request, 'polls/detail.html', {'question' : question_id})
    #※ %s:str型

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html",{'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    #例外処理
    except (KeyError, Choice.DoesNotExist):
        #Resdisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        #Always return an HttpResponseRedirect after successfully dealing
        #with Postdata. This prevents data from being posted twice if a user hit the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

"""
#2020/03/27
#そもそもビューとは?
"""
Djangoアプリケーションにおいて特定の機能を提供するウェブページの型であり、各々のテンプレートを持つ
例えばブログアプリケーションなら
・Blogホームページ
・エントリー詳細
・年ごとのアーカイブ
・月ごとのアーカイブ
・コメント投稿
など

投票アプリケーションでは
・質問"インデックスページ"-最新の質問をいくつか表示
・質問詳細ページ
・質問結果ぺーじ
・投票ページ
など
"""

#インクリメント、ディクリメント:それぞれ変数の値を1増やす、1減らすという意味。カウンタとか。