from django.forms.models import inlineformset_factory
from .models import Quiz, Question, Answer


QuestionFormSet = inlineformset_factory(
    Quiz,
    Question,
    fields=["text"],
    extra=3,
    can_delete=True,
)

AnswerFormSet = inlineformset_factory(
    Question,
    Answer,
    fields=["text", "correct"],
    extra=4,
    can_delete=True,
    max_num=4,
    absolute_max=4,
)
