import logging

from django.db import connection
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from .models import Poll, Question, Choice

logger = logging.getLogger(__name__)


# REQUEST-TEMPLATE VIEWS

# def index(request):
# #     return HttpResponse("Hello, world. You're at the polls index.")
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {'latest_question_list': latest_question_list}
#     return render(request, 'polls_index.html', context)




# CLASS-BASED VIEWS

# dflt : template_name = 'poll_list.html'
# dflt : context_object_name = 'poll_list'
class IndexView(generic.ListView):
    model = Poll
    template_name = 'polls_index.html'

    # log request
    def get(self, request, *args, **kwargs):
        logger.debug('IndexView {}'.format(request.GET))
        return super().get(request, *args, **kwargs)

    # various ways to get/mess with the poll_list
    # limit to most recent 5 polls
    queryset = Poll.objects.filter(poll_date__lte=timezone.now()).order_by('-poll_date')[:5]
#     def get_queryset(self):
#         return Poll.objects.filter(poll_date__lte=timezone.now()).order_by('-poll_date')[:5]
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         #context['poll_list'] = Poll.objects.all()[:5]
#         context['poll_list'] = self.object_list[:5]
#         context['xtra'] = 'hello there'
#         return context



# dflt : template_name = 'poll_detail.html'
# dflt : context_object_name = 'poll'
class VoteView(generic.DetailView):
    model = Poll
    template_name = 'polls_vote.html'

    # log request
    def get(self, request, *args, **kwargs):
        logger.debug('VoteView {}'.format(request.GET))
        return super().get(request, *args, **kwargs)

    # Record the last accessed date
#     def get_object(self):
#         obj = super().get_object()
#         obj.last_accessed = timezone.now()
#         obj.save()
#         return obj


# dflt : template_name = 'poll_detail.html'
# dflt : context_object_name = 'poll'
class ResultView(generic.DetailView):
    model = Poll
    template_name = 'polls_result.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['sql'] = "{}".format(connection.queries)
#         return context


# from django.db import connections
# connections['default'].queries


# POST: {'question-2': ['9'], 'question-5': ['6'], 'question-1': ['4']}
def submitvote(request, poll_id):
    logger.debug('submitvote {}'.format(request.POST))
    valid = True
    poll = get_object_or_404(Poll, pk=poll_id)

    votes = []
    for question in poll.question_set.all():
        key = 'question-{}'.format(question.id)
        logger.debug('submitvote : key={}'.format(key))
        try:
            selected_choice = question.choice_set.get(pk=request.POST[key])
        except (KeyError, Choice.DoesNotExist):
            msg = 'Question {} is required'.format(question.question_sort)
            messages.add_message(request, messages.ERROR, msg)
            valid = False
        else:
            #logger.debug('submitvote : selected_choice={}'.format(selected_choice))
            selected_choice.votes += 1
            votes.append(selected_choice)

    if not valid:
        context = {'poll': poll,}
        return render(request, 'polls_vote.html', context)

    logger.debug('submitvote : votes={!r}'.format(votes))
    for v in votes:
        #logger.debug('submitvote : vote={!r}'.format(v))
        v.save()
    messages.add_message(request, messages.SUCCESS, 'Your votes have been recorded.')
    return HttpResponseRedirect(reverse('polls:result', args=(poll.id,)))



