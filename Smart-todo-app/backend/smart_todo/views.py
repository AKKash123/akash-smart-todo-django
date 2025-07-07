from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Task, Category, ContextEntry
from .serializers import TaskSerializer, CategorySerializer, ContextEntrySerializer
from .utils import generate_insight_from_context, suggest_task


# Fetch all tasks
@api_view(['GET'])
def list_tasks(request):
    tasks = Task.objects.all().order_by('-created_at')
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)


# Create a new task
@api_view(['POST'])
def create_task(request):
    try:
        category_id = request.data.get('category_id')
        category = Category.objects.get(id=category_id) if category_id else None

        task = Task.objects.create(
            title=request.data['title'],
            description=request.data.get('description', ''),
            priority_score=request.data.get('priority', 2),
            deadline=request.data.get('deadline', None),
            is_completed=request.data.get('is_completed', False),
            category=category
        )
        serializer = TaskSerializer(task)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except Category.DoesNotExist:
        return Response({"error": "Category not found."}, status=400)
    except Exception as e:
        return Response({"error": str(e)}, status=400)


# Fetch all categories
@api_view(['GET'])
def list_categories(request):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    return Response(serializer.data)


# Submit context and return AI-generated insight + save to model
@api_view(['POST'])
def create_context_entry(request):
    content = request.data.get("text", "")
    insight = generate_insight_from_context(content)
    entry = ContextEntry.objects.create(content=content, processed_insights=insight)
    serializer = ContextEntrySerializer(entry)
    return Response(serializer.data)


#  Just return insight without saving to DB
@api_view(['POST'])
def generate_insight_view(request):
    context = request.data.get("text")
    if not context:
        return Response({"error": "Missing 'text' in request body."}, status=status.HTTP_400_BAD_REQUEST)

    result = generate_insight_from_context(context)
    return Response({"insights": result}, status=status.HTTP_200_OK)


#  Return task suggestion from context
@api_view(['POST'])
def suggest_task_view(request):
    context = request.data.get("text")
    if not context:
        return Response({"error": "Missing 'text' in request body."}, status=status.HTTP_400_BAD_REQUEST)

    result = suggest_task(context)
    return Response({"task_suggestion": result}, status=status.HTTP_200_OK)