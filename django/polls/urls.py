from django.urls import include, path
from . import views

app_name = 'polls'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('<int:pk>/', views.VoteView.as_view(), name='vote'),
    path('<int:pk>/result/', views.ResultView.as_view(), name='result'),
    path('<int:poll_id>/submitvote/', views.submitvote, name='submitvote'),
]
