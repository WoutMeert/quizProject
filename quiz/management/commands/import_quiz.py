import json
import os
from django.core.management.base import BaseCommand
from quiz.models import Category, SubCategory, Question, AnswerOption


class Command(BaseCommand):
    help = 'Import quiz data from JSON file'

    def handle(self, *args, **options):
        file_path = 'data/hybrid_block_codec_quiz.json'
        if not os.path.exists(file_path):
            self.stderr.write(f'File {file_path} does not exist.')
            return

        with open(file_path, 'r') as f:
            data = json.load(f)

        categories = {}
        subcategories = {}
        questions_count = 0
        options_count = 0

        for item in data:
            cat_name = item['category']
            subcat_name = item['subcategory']

            # Get or create category
            if cat_name not in categories:
                cat, created = Category.objects.get_or_create(name=cat_name)
                categories[cat_name] = cat

            cat = categories[cat_name]

            # Get or create subcategory
            subcat_key = (cat.id, subcat_name)
            if subcat_key not in subcategories:
                subcat, created = SubCategory.objects.get_or_create(name=subcat_name, category=cat)
                subcategories[subcat_key] = subcat

            subcat = subcategories[subcat_key]

            # Create question
            question, created = Question.objects.get_or_create(
                id=item['id'],
                defaults={
                    'subcategory': subcat,
                    'question': item['question'],
                    'explanation': item['explanation'],
                    'difficulty': item['difficulty']
                }
            )
            if created:
                questions_count += 1

            # Delete existing options for the question to avoid duplicates
            AnswerOption.objects.filter(question=question).delete()

            # Create answer options
            for opt in item['options']:
                is_correct = (opt == item['correct_answer'])
                option, created = AnswerOption.objects.get_or_create(
                    question=question,
                    option_text=opt,
                    defaults={'is_correct': is_correct}
                )
                if created:
                    options_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully imported {len(categories)} categories, '
                f'{len(subcategories)} subcategories, '
                f'{questions_count} questions, '
                f'{options_count} answer options.'
            )
        )
