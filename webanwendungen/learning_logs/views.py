from django.shortcuts import render, redirect
from .models import Topic
from .forms import TopicForm


def index(request):
    """The home page for Learning Log"""
    title = 'Learning Log Main'
    return render(request, 'learning_logs/index.html', {'title': title})


def topics(request):
    """Show all topics."""
    topics = Topic.objects.order_by('date_added')
    title = 'Fachgebiete'
    context = {'topics': topics, 'title': title}
    return render(request, 'learning_logs/topics.html', context)


def topic(request, topic_id):
    """Show a single topic and it's entries."""
    title = 'Einträge'
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'entries': entries, 'topic': topic, 'title': title}
    return render(request, 'learning_logs/topic.html', context)

def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # Keine Daten übermittelt; es wird ein leeres Formular erstellt.
        form = TopicForm()
    else:
        # POST-Daten übermittelt; Daten werden verarbeitet.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topics')
    # Zeigt ein leeres oder ein als ungültig erkanntes Formular an.
    context = {'form': form}
    return render(request, 'learning_logs/new_topic.html', context)