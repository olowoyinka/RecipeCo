from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.views.generic.base import TemplateResponseMixin, View
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.http import JsonResponse


from .models import Quiz, Question, Answer, Result
from .forms import AnswerFormSet, QuestionFormSet


def choose_difficulty(request):
    difficulty = ["easy", "medium", "hard"]
    return render(
        request, "quiz/choose_difficulty.html", {"difficulty_levels": difficulty}
    )


class QuizListView(ListView):
    model = Quiz
    template_name = "quiz/main.html"

    def get(self, request):
        level = request.GET.get("difficulty")
        if level:
            self.queryset = Quiz.objects.all().filter(difficulty=level)

        return super().get(request)


class QuizCreateView(CreateView):
    model = Quiz
    template_name = "quiz/form.html"
    success_url = reverse_lazy("quiz:main-view")
    fields = [
        "name",
        "topic",
        "number_of_questions",
        "time",
        "required_score_to_pass",
        "difficulty",
    ]

    def form_valid(self, form):
        return super().form_valid(form)


class QuizUpdateView(UpdateView):
    model = Quiz
    template_name = "quiz/form.html"
    success_url = reverse_lazy("quiz:main-view")
    fields = [
        "name",
        "topic",
        "number_of_questions",
        "time",
        "required_score_to_pass",
        "difficulty",
    ]

    def form_valid(self, form):
        return super().form_valid(form)


class QuizAnswersUpdateView(TemplateResponseMixin, View):
    template_name = "quiz/question/answers_formset.html"
    quiz = None
    questions = None

    def answer_formset(self, question, data=None):
        return AnswerFormSet(
            instance=question, data=data, prefix=f"question:{question.pk}"
        )

    def questions_and_answer_formset(self, data=None):
        return [(q, self.answer_formset(q, data)) for q in self.questions]

    def dispatch(self, request, pk):
        self.quiz = get_object_or_404(Quiz, id=pk)
        self.questions = self.quiz.question_set.all()
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):
        context = {
            "quiz": self.quiz,
            "questions_with_answer_formset": self.questions_and_answer_formset(),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        qna = self.questions_and_answer_formset(data=request.POST)

        context = {
            "quiz": self.quiz,
            "questions_with_answers_formset": qna,
        }

        for _, formset in qna:
            if not formset.is_valid():
                return self.render_to_response(context)
            else:
                formset.save()

        return redirect("quiz:main-view")


class QuizQuestionUpdateView(TemplateResponseMixin, View):
    template_name = "quiz/question/formset.html"
    quiz = None

    def question_formset(self, data=None):
        return QuestionFormSet(instance=self.quiz, data=data, prefix="questions")

    def dispatch(self, request, pk):
        self.quiz = get_object_or_404(Quiz, id=pk)
        return super().dispatch(request, pk)

    def get(self, request, *args, **kwargs):

        context = {
            "quiz": self.quiz,
            "question_formset": self.question_formset(),
        }
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        question_formset = self.question_formset(data=request.POST)

        if question_formset.is_valid():
            question_formset.save()
            return redirect("quiz:main-view")

        context = {
            "quiz": self.quiz,
            "question_formset": question_formset,
        }
        return self.render_to_response(context)


class QuizDeleteView(DeleteView):
    model = Quiz
    template_name = "quiz/delete.html"
    success_url = reverse_lazy("quiz:main-view")

    def form_valid(self, form):
        return super().form_valid(form)


def quiz_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    return render(request, "quiz/quiz.html", {"obj": quiz})


def quiz_data_view(request, pk):
    quiz = Quiz.objects.get(pk=pk)
    questions = [
        {str(q): [a.text for a in q.get_answers()]} for q in quiz.get_questions()
    ]
    # for q in quiz.get_questions():
    #     answers = [a]
    #     for a in q.get_answers():
    #         answers.append(a.text)
    #     questions.append({str(q): answers})
    return JsonResponse(
        {
            "data": questions,
            "time": quiz.time,
        }
    )


def save_quiz_view(request, pk):
    if request.is_ajax():
        questions = []
        data = request.POST
        data_ = dict(data.lists())

        data_.pop("csrfmiddlewaretoken")

        for k in data_.keys():

            question = Question.objects.get(text=k)
            questions.append(question)

        user = request.user
        quiz = Quiz.objects.get(pk=pk)

        score = 0
        multiplier = 100 / quiz.number_of_questions
        results = []
        correct_answer = None

        for q in questions:
            a_selected = request.POST.get(q.text)

            if a_selected != "":
                question_answers = Answer.objects.filter(question=q)
                for a in question_answers:
                    if a_selected == a.text:
                        if a.correct:
                            score += 1
                            correct_answer = a.text
                    else:
                        if a.correct:
                            correct_answer = a.text

                results.append(
                    {str(q): {"correct_answer": correct_answer, "answered": a_selected}}
                )
            else:
                results.append({str(q): "not answered"})

        score_ = score * multiplier
        Result.objects.create(quiz=quiz, user=user, score=score_)

        if score_ >= quiz.required_score_to_pass:
            return JsonResponse({"passed": True, "score": score_, "results": results})
        else:
            return JsonResponse({"passed": False, "score": score_, "results": results})
