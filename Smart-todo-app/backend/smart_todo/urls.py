from django.urls import path
from .views import (
    # Task Views
    create_task,
    list_tasks,

    # Category Views
    list_categories,

    # AI Context Views
    suggest_task_view,
    create_context_entry,
    generate_insight_view,
)

urlpatterns = [
    # Task Management
    path('tasks/', list_tasks, name='list_tasks'),
    path('tasks/create/', create_task, name='create_task'),

    # Category Management
    path('categories/', list_categories, name='list_categories'),

    # AI Context-Based Features
    path('context/', create_context_entry, name='create_context_entry'),  # saves context + insight to DB
    path('context/insight/', generate_insight_view, name='generate_insight_view'),  # only generates insight
    path('context/suggest/', suggest_task_view, name='suggest_task'),  # one-liner task suggestion
]
