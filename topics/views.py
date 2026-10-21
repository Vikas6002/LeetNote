# topics/views.py
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import TopicNote
from notes.models import Note


@login_required
def topic_list(request):
    topics = TopicNote.objects.all().order_by('tag__name')
    return render(request, 'topics/topic_list.html', {'topics': topics})


@login_required
def topic_detail(request, pk):
    topic = get_object_or_404(TopicNote, pk=pk)

    # get all notes by this user that have this tag
    notes = Note.objects.filter(
        user=request.user,
        tags=topic.tag
    ).order_by('-created')

    return render(request, 'topics/topic_detail.html', {
        'topic': topic,
        'notes': notes,
    })