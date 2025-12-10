from django.shortcuts import render, get_object_or_404
from django.views import View
from .models import Category, SubCategory, Question, AnswerOption


class CategoryListView(View):
    def get(self, request):
        categories = Category.objects.all()
        return render(request, 'quiz/category_list.html', {'categories': categories})


class QuizView(View):
    def get(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        subcategories = SubCategory.objects.filter(category=category).prefetch_related('questions__options')
        return render(request, 'quiz/quiz_page.html', {'category': category, 'subcategories': subcategories})


class SubmitQuizView(View):
    def post(self, request, category_id):
        category = get_object_or_404(Category, pk=category_id)
        score = 0
        total_questions = 0
        results = []

        for key, value in request.POST.items():
            if key.startswith('question_'):
                question_id = int(key.split('_')[1])
                option_id = int(value)
                question = get_object_or_404(Question, pk=question_id)
                selected_option = get_object_or_404(AnswerOption, pk=option_id, question=question)
                correct_option = AnswerOption.objects.filter(question=question, is_correct=True).first()
                is_correct = selected_option.is_correct
                if is_correct:
                    score += 1
                total_questions += 1
                results.append({
                    'question': question,
                    'selected': selected_option,
                    'correct': correct_option,
                    'is_correct': is_correct,
                    'explanation': question.explanation,
                })

        return render(request, 'quiz/quiz_results.html', {
            'category': category,
            'score': score,
            'total': total_questions,
            'results': results,
        })
