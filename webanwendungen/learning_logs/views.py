from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import Topic, Entry
from .forms import TopicForm, EntryForm


def index(request):
    """The home page for Learning Log"""
    title = 'Learning Log Main'
    return render(request, 'learning_logs/index.html', {'title': title})


@login_required
def topics(request):
    """Show all topics."""
    topics = Topic.objects.filter(owner=request.user).order_by('date_added')
    title = 'Fachgebiete'
    context = {'topics': topics, 'title': title}
    return render(request, 'learning_logs/topics.html', context)


@login_required
def topic(request, topic_id):
    """Show a single topic and it's entries."""
    title = 'Einträge'
    topic = Topic.objects.get(id=topic_id)
    # Überprüft, ob das Fachgebiet dem aktuellen Benutzer gehört.
    if topic.owner != request.user:
        raise Http404

    entries = topic.entry_set.order_by('-date_added')
    context = {'entries': entries, 'topic': topic, 'title': title}
    return render(request, 'learning_logs/topic.html', context)


@login_required
def new_topic(request):
    """Add a new topic"""
    if request.method != 'POST':
        # Keine Daten übermittelt; es wird ein leeres Formular erstellt.
        form = TopicForm()
    else:
        # POST-Daten übermittelt; Daten werden verarbeitet.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            new_topic.save()
            return redirect('learning_logs:topics')
    # Zeigt ein leeres oder ein als ungültig erkanntes Formular an.
    title = 'Neues Fachgebiet'
    context = {'form': form, 'title': title}
    return render(request, 'learning_logs/new_topic.html', context)


@login_required
def new_entry(request, topic_id):
    """Add a new entry for a particular topic"""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Keine Daten übermittelt; es wird ein leeres Formular erstellt.
        form = EntryForm()
    else:
        # POST-Daten übermittelt; Daten werden verarbeitet.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('learning_logs:topic', topic_id=topic_id)

    # Zeigt ein leeres oder ein als gültig erkanntes Formular an.
    title = 'Neuer Eintrag'
    context = {'topic': topic, 'form': form, 'title': title}
    return render(request, 'learning_logs/new_entry.html', context)


@login_required
def edit_entry(request, entry_id):
    """Edit an existing entry"""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic
    if topic.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Ursprüngliche Anforderung; das mit dem jetzigen Eintrag vorab
        # ausgefüllte Formular wird angezeigt.
        form = EntryForm(instance=entry)
    else:
        # POST-Daten übermittelt; Daten werden verarbeitet.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('learning_logs:topic', topic_id=topic.id)
    title = 'Bearbeite Eintrag'
    context = {'entry': entry, 'title': title, 'topic': topic, 'form': form}
    return render(request, 'learning_logs/edit_entry.html', context)
