from django.urls import path
from . import views

app_name = "quiz"

urlpatterns = [
    path("", views.QuizListView.as_view(), name="main-view"),
    path("create/", views.QuizCreateView.as_view(), name="create"),
    path("<pk>/create/", views.QuizUpdateView.as_view(), name="update"),
    path("<pk>/delete/", views.QuizDeleteView.as_view(), name="delete"),
    path(
        "<pk>/questions/update/",
        views.QuizQuestionUpdateView.as_view(),
        name="question_update",
    ),
    path(
        "<pk>/answers/update/",
        views.QuizAnswersUpdateView.as_view(),
        name="answers_update",
    ),
    path("<pk>/", views.quiz_view, name="quiz-view"),
    path("<pk>/save/", views.save_quiz_view, name="save-view"),
    path("<pk>/data/", views.quiz_data_view, name="quiz-data-view"),
]
