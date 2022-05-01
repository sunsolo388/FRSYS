from django.urls import path

from . import views

urlpatterns = [

    path('', views.index, name='index'),

    # 例如: /polls/5/
    path('<int:question_id>/', views.detail, name='detail'),

    # 例如: /polls/5/results/
    path('<int:question_id>/results/', views.results, name='results'),

    # 例如: /polls/5/vote/
    path('<int:question_id>/vote/', views.vote, name='vote'),
]