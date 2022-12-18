import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Poll, Question, Choice

### utils
def create_poll(poll_title, days):
    """
    Create poll with given `poll_title`, published +/- `days` from now
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Poll.objects.create(
            poll_title=poll_title,
            poll_date=time
            )

def create_question(poll_id, question_sort, question_text):
    """
    Create question with given `poll_id`, `question_sort` and `question_text`
    """
    return Question.objects.create(
            poll_id=poll_id,
            question_sort=question_sort,
            question_text=question_text,
            )

def create_choice(question_id, choice_text):
    """
    Create choice with given `question_id` and `choice_text`
    """
    return Choice.objects.create(
            question_id=question_id,
            choice_text=choice_text,
            )

### POLL
class PollModelTests(TestCase):

    def test_is_recent_with_future_poll(self):
        """
        is_recent() returns False for polls with future poll_date
        """
        time = timezone.now() + datetime.timedelta(days=30)
        p = Poll(poll_title="FUTURE POLL", poll_date=time)
        self.assertIs(p.is_recent(), False)

    def test_is_recent_with_past_poll(self):
        """
        is_recent() returns False for polls with past poll_date
        """
        time = timezone.now() + datetime.timedelta(days=-30)
        p = Poll(poll_title="PAST POLL", poll_date=time)
        self.assertIs(p.is_recent(), False)

    def test_is_recent_with_current_poll(self):
        """
        is_recent() returns True for polls within past day
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        p = Poll(poll_title="CURRENT POLL", poll_date=time)
        self.assertIs(p.is_recent(), True)


class QuestionModelTests(TestCase):

    def test_create_poll_question(self):
        p = Poll(poll_title="P1")
        q = Question(poll_id=p.id, question_text="Q1", question_sort=1)
        self.assertIs(p.id, q.poll_id)
        self.assertIs(q.question_sort, 1)
#         self.assertIs(q.poll.poll_title, "P1")


class ChoiceModelTests(TestCase):

    def test_create_question_choice(self):
        q = Question(question_text="Q1")
        c = Choice(question_id=q.id, choice_text="C1", votes=1)
        self.assertIs(q.id, c.question_id)
        self.assertIs(c.votes, 1)


class PollIndexViewTests(TestCase):
    def test_no_polls(self):
        """
        If no polls exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(
            response.context['poll_list'],
            []
        )

    def test_future_poll(self):
        """
        Polls with a poll_date in the future aren't displayed on the index page.
        """
        create_poll(poll_title="FUTURE POLL", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(
            response.context['poll_list'],
            []
        )

    def test_past_poll(self):
        """
        Polls with a poll_date in the past are displayed on the index page.
        """
        poll = create_poll(poll_title="PAST POLL", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['poll_list'],
            [poll]
        )

    def test_future_and_past_poll(self):
        """
        Only polls with a poll_date in the past are displayed on the index page.
        """
        poll = create_poll(poll_title="PAST POLL", days=-30)
        create_poll(poll_title="FUTURE POLL", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['poll_list'],
            [poll]
        )

    def test_poll_sort(self):
        """
        The polls index page may display multiple questions.
        """
        poll1 = create_poll(poll_title="PAST POLL", days=-30)
        poll2 = create_poll(poll_title="PAST POLL", days=-10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['poll_list'],
            [poll2, poll1]
        )


# class QuestionModelTests(TestCase):
#
#     def test_is_recent_with_future_question(self):
#         """
#         is_recent() returns False for questions with future poll_date
#         """
#         time = timezone.now() + datetime.timedelta(days=30)
#         q = Question(question_text="Future question.", poll_date=time)
#         self.assertIs(q.is_recent(), False)
#
#     def test_is_recent_with_past_question(self):
#         """
#         is_recent() returns False for questions whose poll_date is older than 1 day.
#         """
#         time = timezone.now() - datetime.timedelta(days=1, seconds=1)
#         q = Question(question_text="Past question.", poll_date=time)
#         self.assertIs(q.is_recent(), False)
#
#     def test_is_recent_with_recent_question(self):
#         """
#         is_recent() returns True for questions whose poll_date is within the last day.
#         """
#         time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
#         q = Question(question_text="Recent question.", poll_date=time)
#         self.assertIs(q.is_recent(), True)


# class QuestionIndexViewTests(TestCase):
#     def test_no_questions(self):
#         """
#         If no questions exist, an appropriate message is displayed.
#         """
#         response = self.client.get(reverse('polls:index'))
#         self.assertEqual(response.status_code, 200)
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(
#             response.context['question_list'],
#             []
#         )
#
#     def test_future_question(self):
#         """
#         Questions with a poll_date in the future aren't displayed on the index page.
#         """
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertContains(response, "No polls are available.")
#         self.assertQuerysetEqual(
#             response.context['question_list'],
#             []
#         )
#
#     def test_past_question(self):
#         """
#         Questions with a poll_date in the past are displayed on the index page.
#         """
#         question = create_question(question_text="Past question.", days=-30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['question_list'],
#             [question],
#         )
#
#     def test_future_and_past_question(self):
#         """
#         Even if both past and future questions exist, only past questions are displayed.
#         """
#         question = create_question(question_text="Past question.", days=-30)
#         create_question(question_text="Future question.", days=30)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['question_list'],
#             [question],
#         )
#
#     def test_two_past_questions(self):
#         """
#         The questions index page may display multiple questions.
#         """
#         question1 = create_question(question_text="Past question 1.", days=-30)
#         question2 = create_question(question_text="Past question 2.", days=-5)
#         response = self.client.get(reverse('polls:index'))
#         self.assertQuerysetEqual(
#             response.context['question_list'],
#             [question2, question1],
#         )
