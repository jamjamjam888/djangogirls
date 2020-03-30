"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
#↑リファレンス参照

urlpatterns = [
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
]
"""
-memo-
include()関数は他のURLconfへの参照尾することができる。Djangoがinclude()に遭遇すると、そのポイントまで一致した
URL部分を切り落とし、次の処理のためにの残りの文字列をインクルードされたURLconfを渡す

#この状態で
>python manage.py runserver
をして、
https://localhost:8000/polls/
にアクセスすると表示画面が遷移する

path()関数について
path()関数は4つの引数を受け取る。引数のうちrouteとviewsの2つは必須。kwargs,nameの2つは省略可能
引数➀route
routeはURLを含む文字列。
リクエストを処理するとき、Djangoはurlpatternsのはじめのパターンから開始し、リストを上から順に見ていく(それ以外しらん)
要求されたURLと一致するものを見つけるまで各パターンと比較していく
ただし、パターンはGETやPOSTのパラメータ、そしてドメイン名は見ない

引数➁views
Djangoがマッチする正規表現を見つけると、Djangoは指定されたビュー関数を呼び出す。
その際HttpRequestオブジェクトを第一引数に、そしてキーワード引数としてrouteから「キャプチャされた」値を呼び出す
※キャプチャ:コンピュータにデータを取り込むこと
(正規表現とは？→DBからデータを取得する際に使う。「いくつかの文字列を一つの形式で表現するための方法」。まあ要するに検索をかけやすくするための表現方法。メタ文字を使用する。
参照:https://userweb.mnet.ne.jp/nakama/)

引数➂kwargs
任意のキーワード引数を辞書として対象のビューに渡す
※チュートリアルでは使用しない

引数➃name
URLに名前付けしておけばDjangoのどこからでも明確に参照可能。
特にテンプレートの中で有効
"""