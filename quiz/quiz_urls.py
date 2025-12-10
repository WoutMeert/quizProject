from django.urls import path
from . import views

urlpatterns = [
    path('', views.CategoryListView.as_view(), name='category_list'),
    path('<int:category_id>/', views.QuizView.as_view(), name='quiz_page'),
    path('<int:category_id>/submit/', views.SubmitQuizView.as_view(), name='submit_quiz'),
]
