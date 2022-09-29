import datetime
import logging
from django.contrib import admin
from django.core.exceptions import ObjectDoesNotExist
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

logger = logging.getLogger(__name__)


#
# POLL
# questions: Question.objects.filter(poll_id = self.pk)
# choices:   Choice.objects.filter(question__poll__pk = self.pk)
#
class Poll(models.Model):
    poll_title = models.CharField(max_length=200)
    poll_date = models.DateTimeField('date published')

    @admin.display(description='Recent?', ordering='-poll_date')
    def is_recent(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.poll_date <= now

    @admin.display(description='Questions')
    def cnt_questions(self):
        return self.question_set.count()

    @admin.display(description='Choices')
    def cnt_choices(self):
        return Choice.objects.filter(question__poll__pk = self.pk).count()

    @admin.display(description='Votes')
    def cnt_votes(self):
#         logger.debug('QUERY {}'.format(Choice.objects.filter(question__poll__pk = self.pk).query))
        return Choice.objects.filter(question__poll__pk = self.pk).aggregate(models.Sum('votes'))['votes__sum']

    class Meta:
        ordering = ['-poll_date']

    def __repr__(self):
        return '<Poll(id=%r,poll_title=%r,poll_date=%r)>' \
                % (self.id,self.poll_title,self.poll_date)

    def __str__(self):
#         return 'Poll %s: %s' % (self.id,self.poll_title)
        return '%s' % (self.poll_title)


#
# QUESTION
# choices: Choice.objects.filter(question_id = self.pk)
#
class Question(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)    # related_name='question_set'
    question_sort = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    question_text = models.CharField(max_length=200)

    class Meta:
        ordering = ['question_sort']

    @admin.display(description='Choices')
    def cnt_choices(self):
        return self.choice_set.count()

    @admin.display(description='Votes')
    def cnt_votes(self):
        return Choice.objects.filter(question__pk = self.pk).aggregate(models.Sum('votes'))['votes__sum']

    @admin.display(description='Options')
    def choices_summary(obj,max_choices=3):
        result = ''
        last_choice = ''
#         max_choices = 3
        cnt_choices = obj.cnt_choices()
        for i,c in enumerate(obj.choice_set.all().order_by('choice_text')):
            if cnt_choices > max_choices and i >= max_choices-1:
                last_choice = ', ... {}'.format(c.choice_text)
                continue
            result += '[{}] '.format(cnt_choices) if i == 0 else ', '
            result += '{}'.format(c.choice_text)
        return result + last_choice

    class Meta:
        ordering = ['question_sort']

    def __repr__(self):
        return '<Question(id=%r,question_sort=%r,question_text=%r)>' \
                % (self.id,self.question_sort,self.question_text)

    def __str__(self):
#         return 'Poll %s, Question %s: %s' % (self.poll.id,self.id,self.question_text)
        return '%s : %s' % (self.poll.poll_title,self.question_text)


#
# CHOICE
#
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)    # related_name='choice_set'
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    class Meta:
        ordering = ['choice_text']

    def __repr__(self):
        return '<Choice(id=%r,question=%r,choice_text=%r,votes=%r)>' \
                % (self.id,self.question,self.choice_text,self.votes)

    def __str__(self):
#         return 'Question %s, Choice %s: %s (%s)' % (self.question.id,self.id,self.choice_text,self.votes)
        return '%s : %s : %s' % (self.question.poll.poll_title,self.question.question_text,self.choice_text)

