from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import Poll, Question, Choice


### CHOICE INLINE
class ChoiceRowAdmin(admin.TabularInline):
    model = Choice
    extra = 1
    fields = ['choice_text','votes','choice_list_edit']
    readonly_fields = ['choice_list_edit']
    ordering = ['choice_text']

    @admin.display(description='Update')
    def choice_list_edit(self, obj):
        if not obj.id: return ''
        return format_html('<a href="{}" class="inlinechangelink">{}</a>',
                reverse('admin:polls_choice_change', args=(obj.id,)),
                'Change'
                )


### CHOICE ADMIN
class ChoiceAdmin(admin.ModelAdmin):

    list_display = ('choice_list_poll', 'choice_list_question', 'choice_list_text', 'votes')
    list_filter = ['question__poll']
    search_fields = ['choice_text']
    ordering = ['question__poll__poll_title','question__question_sort','choice_text']

    @admin.display(description='Poll', ordering='question__poll__poll_title')
    def choice_list_poll(self, obj):
        return format_html('<a href="{}">{}</a>',
                reverse('admin:polls_poll_change', args=(obj.question.poll.id,)),
                obj.question.poll.poll_title
                )

    @admin.display(description='Question', ordering='question__question_sort')
    def choice_list_question(self, obj):
        return format_html('{}) <a href="{}">{}</a>',
                obj.question.question_sort,
                reverse('admin:polls_question_change', args=(obj.question.id,)),
                obj.question.question_text
                )

    @admin.display(description='Choice', ordering='choice_text')
    def choice_list_text(self, obj):
        return format_html('<a href="{}">{}</a>',
                reverse('admin:polls_choice_change', args=(obj.id,)),
                obj.choice_text
                )

    # redirect to choice.question  on _save
    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        if "_addanother" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_choice_add') )
        elif "_continue" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_choice_change', args=(obj.id,)) )
        else:
            return HttpResponseRedirect( reverse('admin:polls_question_change', args=(obj.question.id,)) )

    # redirect to choice.question  on _save
    def response_change(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        if "_addanother" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_choice_add') )
        elif "_continue" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_choice_change', args=(obj.id,)) )
        else:
            return HttpResponseRedirect( reverse('admin:polls_question_change', args=(obj.question.id,)) )


### QUESTION INLINE
class QuestionRowAdmin(admin.TabularInline):
    model = Question
    extra = 0
    fields = ['question_sort','question_text','question_list_choices','question_list_edit']
    readonly_fields = ['question_list_choices','question_list_edit']
    ordering = ['question_sort','question_text']

    @admin.display(description='Choices')
    def question_list_choices(self, obj):
        if not obj.id: return ''
        max_choices = 3
        return obj.choices_summary(max_choices=max_choices)

    @admin.display(description='Update')
    def question_list_edit(self, obj):
        if not obj.id: return ''
        return format_html('<a href="{}" class="inlinechangelink">{}</a>',
                reverse('admin:polls_question_change', args=(obj.id,)),
                'Change'
                )


### QUESTION ADMIN
class QuestionAdmin(admin.ModelAdmin):
    fields = ['poll', 'question_sort', 'question_text']
    inlines = [ChoiceRowAdmin]

    list_display = ('question_list_poll', 'question_list_text', 'question_list_choices','cnt_votes')
    list_filter = ['poll']
    search_fields = ['question_text']
    ordering = ['poll__poll_title','question_sort']

    @admin.display(description='Poll', ordering='poll__poll_title')
    def question_list_poll(self, obj):
        return format_html('<a href="{}">{}</a>',
                reverse('admin:polls_poll_change', args=(obj.poll.id,)),
                obj.poll.poll_title
                )

    @admin.display(description='Question', ordering='question_sort')
    def question_list_text(self, obj):
        return format_html('{}) <a href="{}">{}</a>',
                obj.question_sort,
                reverse('admin:polls_question_change', args=(obj.id,)),
                obj.question_text
                )

    @admin.display(description='Choices')
    def question_list_choices(self, obj):
        max_choices = 3
        return obj.choices_summary(max_choices=max_choices)

    # redirect to question.poll  on _save
    def response_add(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        if "_addanother" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_question_add') )
        elif "_continue" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_question_change', args=(obj.id,)) )
        else:
            return HttpResponseRedirect( reverse('admin:polls_poll_change', args=(obj.poll.id,)) )

    # redirect to question.poll  on _save
    def response_change(self, request, obj, post_url_continue=None):
        from django.http import HttpResponseRedirect
        if "_addanother" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_question_add') )
        elif "_continue" in request.POST:
            return HttpResponseRedirect( reverse('admin:polls_question_change', args=(obj.id,)) )
        else:
            return HttpResponseRedirect( reverse('admin:polls_poll_change', args=(obj.poll.id,)) )


### POLL ADMIN
class PollAdmin(admin.ModelAdmin):
    fields = ['poll_title', 'poll_date']
#     fieldsets = [
#         (None,               {'fields': ['poll_title']}),
#         ('Date information', {'fields': ['poll_date']}),
#     ]
    inlines = [QuestionRowAdmin]

    list_display = ('poll_list_title', 'is_recent', 'poll_date', 'cnt_questions', 'cnt_choices', 'cnt_votes')
    list_filter = ['poll_date']
    search_fields = ['poll_title']
    ordering = ['poll_title']

    @admin.display(description='Poll', ordering='poll_title')
    def poll_list_title(self, obj):
        return format_html('<a href="{}">{}</a>',
                reverse('admin:polls_poll_change', args=(obj.id,)),
                obj.poll_title
                )


### REGISTER WITH ADMIN
admin.site.register(Poll, PollAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
