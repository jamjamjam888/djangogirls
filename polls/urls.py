#2020/03/27

#ビューを呼ぶためにURLを対応付けする
#そのためのURLconf
#urls.pyファイルを作成する

from django.urls import path

from . import views


app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]

#次のステップはルートのURLconfにpolls.urlsモジュールの記述を反映させること