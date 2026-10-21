# notes/models.py
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Note(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy',   'Easy'),
        ('medium', 'Medium'),
        ('hard',   'Hard'),
    ]
    LANGUAGE_CHOICES = [
        ('python',     'Python'),
        ('java',       'Java'),
        ('cpp',        'C++'),
        ('javascript', 'JavaScript'),
        ('c',          'C'),
    ]

    # ── core fields (user fills these) ───────────────────────────────────────
    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notes')
    problem_number = models.IntegerField(null=True, blank=True)
    title          = models.CharField(max_length=200)
    problem_link   = models.URLField(blank=True)
    code           = models.TextField()
    language       = models.CharField(max_length=20, choices=LANGUAGE_CHOICES, default='python')
    explanation    = models.TextField(help_text="Describe your approach in your own words")
    difficulty     = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='easy')
    tags           = models.ManyToManyField(Tag, blank=True)

    # ── AI generated fields (filled automatically) ───────────────────────────
    key_points       = models.JSONField(default=list, blank=True)
    time_complexity  = models.CharField(max_length=50, blank=True)
    space_complexity = models.CharField(max_length=50, blank=True)
    core_pattern     = models.TextField(blank=True)
    similar_problems = models.JSONField(default=list, blank=True)
    ai_generated     = models.BooleanField(default=False)

    # ── meta ─────────────────────────────────────────────────────────────────
    created    = models.DateTimeField(auto_now_add=True)
    updated    = models.DateTimeField(auto_now=True)
    is_public  = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created']   # newest first by default

    def __str__(self):
        return f"#{self.problem_number} {self.title}"