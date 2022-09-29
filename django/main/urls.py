"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.views.generic import TemplateView

from rest_framework import routers
from polls import api

router = routers.DefaultRouter()
router.register(r'listpolls', api.PollListView, 'listpolls')
router.register(r'polls', api.PollView, 'polls')
router.register(r'questions', api.QuestionView, 'questions')
router.register(r'choices', api.ChoiceView, 'choices')
# router.register(r'polls/<int:pk>/submitvote', api.SubmitVoteView, 'submitvote')


urlpatterns = [
    path('', TemplateView.as_view(template_name="home.html")),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/', include(router.urls)),
    path('api/polls/<int:poll_id>/submitvote/', api.submitvote, name='submitvote'),
]


admin.site.site_header = 'DjangoApp'            # default: "Django Administration"
admin.site.index_title = 'Site Administration'  # default: "Site administration"
admin.site.site_title  = 'Site Admin'           # default: "Django site admin"




