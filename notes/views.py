# notes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note, Tag
from .forms import NoteForm
from topics.models import TopicNote
from services.gemini_service import generate_note, update_topic_note
from services.leetcode_service import fetch_problem_by_slug, slug_from_url


# ── LIST — search + filter ────────────────────────────────────────────────────
@login_required
def note_list(request):
    qs         = request.user.notes.all()
    q          = request.GET.get('q', '').strip()
    difficulty = request.GET.get('difficulty', '').strip()
    tag_id     = request.GET.get('tag', '').strip()

    if q:
        qs = qs.filter(
            Q(title__icontains=q)       |
            Q(explanation__icontains=q) |
            Q(category__icontains=q)    |
            Q(tag__name__icontains=q)
        ).distinct()

    if difficulty in ('easy', 'medium', 'hard'):
        qs = qs.filter(difficulty=difficulty)

    if tag_id.isdigit():
        qs = qs.filter(tag__id=tag_id)

    context = {
        'notes'         : qs,
        'all_tags'      : Tag.objects.all(),
        'selected_tag'  : tag_id,
        'selected_diff' : difficulty,
        'search_query'  : q,
        'total'         : request.user.notes.count(),
        'easy_count'    : request.user.notes.filter(difficulty='easy').count(),
        'medium_count'  : request.user.notes.filter(difficulty='medium').count(),
        'hard_count'    : request.user.notes.filter(difficulty='hard').count(),
    }
    return render(request, 'notes/notes_list.html', context)


# ── DETAIL ────────────────────────────────────────────────────────────────────
@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    return render(request, 'notes/notes_detail.html', {'note': note})


# ── CREATE ────────────────────────────────────────────────────────────────────
@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note      = form.save(commit=False)
            note.user = request.user

            # ── auto-fill from LeetCode if URL provided ───────────────────
            problem_url = form.cleaned_data.get('problem_link', '')
            if problem_url:
                slug    = slug_from_url(problem_url)
                lc_data = fetch_problem_by_slug(slug) if slug else None
                if lc_data:
                    note.title          = lc_data['title']
                    note.difficulty     = lc_data['difficulty']
                    note.problem_number = lc_data['problem_number']
                    note.problem_link   = problem_url

            note.save()
            form.save_m2m()  # save ManyToMany tags

            # ── get tag names for AI ──────────────────────────────────────
            tag_names = list(note.tags.values_list('name', flat=True))

            # ── call AI to generate note ──────────────────────────────────
            ai_data = generate_note(
                note.title,
                tag_names,
                note.code,
                note.explanation,
            )

            note.key_points       = ai_data.get('key_points', [])
            note.time_complexity  = ai_data.get('time_complexity', '')
            note.space_complexity = ai_data.get('space_complexity', '')
            note.core_pattern     = ai_data.get('core_pattern', '')
            note.similar_problems = ai_data.get('similar_problems', [])
            note.ai_generated     = True
            note.save()

            # ── update TopicNote for each tag ─────────────────────────────
            for tag in note.tags.all():
                topic, _ = TopicNote.objects.get_or_create(tag=tag)
                updated  = update_topic_note(
                    tag.name,
                    topic.key_tricks,
                    ai_data,
                )
                if updated:
                    topic.core_statement = updated.get('core_statement', topic.core_statement)
                    topic.key_tricks     = updated.get('key_tricks',     topic.key_tricks)
                    topic.when_to_use    = updated.get('when_to_use',    topic.when_to_use)
                    topic.save()

            messages.success(request, f'Note for "{note.title}" saved with AI insights!')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm()

    return render(request, 'notes/notes_form.html', {'form': form, 'action': 'Create'})


# ── UPDATE ────────────────────────────────────────────────────────────────────
@login_required
def note_update(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.save()
            form.save_m2m()
            messages.success(request, 'Note updated.')
            return redirect('notes:detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/notes_form.html', {'form': form, 'action': 'Update', 'note': note})


# ── DELETE ────────────────────────────────────────────────────────────────────
@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)

    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f'"{title}" deleted.')
        return redirect('notes:list')

    return render(request, 'notes/notes_delete.html', {'note': note})