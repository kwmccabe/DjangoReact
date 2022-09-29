import logging
from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets, permissions
from rest_framework.decorators import api_view, permission_classes, schema
from rest_framework.response import Response

from .models import Poll, Question, Choice

logger = logging.getLogger(__name__)

# SERIALIZERS

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ('id', 'question', 'choice_text', 'votes')

class QuestionSerializer(serializers.ModelSerializer):
    choice_set = ChoiceSerializer(many=True)

    class Meta:
        model = Question
        fields = ('id', 'poll', 'question_sort', 'question_text', 'cnt_votes', 'cnt_choices', 'choice_set')

class PollSerializer(serializers.ModelSerializer):
    question_set = QuestionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ('id', 'poll_title', 'poll_date', 'is_recent', 'cnt_votes', 'cnt_questions', 'question_set')

class PollListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ('id', 'poll_title', 'poll_date', 'is_recent', 'cnt_votes', 'cnt_questions')


# VIEWSETS

class ChoiceView(viewsets.ModelViewSet):
    serializer_class = ChoiceSerializer
    queryset = Choice.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

class QuestionView(viewsets.ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

class PollView(viewsets.ModelViewSet):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
#     permission_classes = [permissions.IsAuthenticated]

class PollListView(viewsets.ModelViewSet):
    serializer_class = PollListSerializer
    queryset = Poll.objects.all()
#     permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
# @schema(None)
@permission_classes((permissions.AllowAny,))
def submitvote(request, poll_id):
    logger.debug('submitvote {} {}'.format(poll_id, request.data))

    valid = True
    poll = get_object_or_404(Poll, pk=poll_id)

    messages = []
    votes = []
    for question in poll.question_set.all():
        key = 'question-{}'.format(question.id)
        logger.debug('submitvote : key={}'.format(key))
        try:
            selected_choice = question.choice_set.get(pk=request.data[key])
        except (KeyError, Choice.DoesNotExist):
            msg = 'Question {} is required'.format(question.question_sort)
            messages.append(msg)
            valid = False
        else:
            #logger.debug('submitvote : selected_choice={}'.format(selected_choice))
            selected_choice.votes += 1
            votes.append(selected_choice)

    if valid:
        logger.debug('submitvote : votes={!r}'.format(votes))
        for v in votes:
            #logger.debug('submitvote : vote={!r}'.format(v))
            messages.append('{}'.format(v))
            v.save()

    return Response({'messages': messages,})
