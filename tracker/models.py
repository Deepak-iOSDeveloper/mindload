from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=20, blank=True)
    occupation = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    avatar_initial = models.CharField(max_length=2, blank=True)

    def save(self, *args, **kwargs):
        if self.user and not self.avatar_initial:
            self.avatar_initial = self.user.first_name[:1].upper() if self.user.first_name else self.user.username[:1].upper()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Profile of {self.user.username}"


class DailyLog(models.Model):
    MENTAL_LOAD_CHOICES = [
        ('very_low', 'Very Low'),
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    # Study & Work
    study_hours = models.FloatField(default=0, help_text="Hours studied today")
    break_count = models.IntegerField(default=0, help_text="Number of breaks taken")
    avg_break_duration = models.IntegerField(default=0, help_text="Avg break duration in minutes")
    tasks_completed = models.IntegerField(default=0)
    tasks_pending = models.IntegerField(default=0)
    deadline_stress = models.IntegerField(default=5, help_text="1-10 scale")

    # Screen & App Usage
    screen_time_hours = models.FloatField(default=0)
    social_media_hours = models.FloatField(default=0)
    productive_app_hours = models.FloatField(default=0)
    entertainment_hours = models.FloatField(default=0)

    # Sleep
    sleep_hours = models.FloatField(default=7)
    sleep_quality = models.IntegerField(default=5, help_text="1-10 scale")
    bedtime_hour = models.IntegerField(default=23, help_text="Hour of bedtime (0-23)")
    wake_time_hour = models.IntegerField(default=7, help_text="Hour of wake time (0-23)")

    # Physical Activity
    exercise_minutes = models.IntegerField(default=0)
    exercise_type = models.CharField(max_length=50, blank=True)
    steps_count = models.IntegerField(default=0)
    physical_fatigue = models.IntegerField(default=5, help_text="1-10 scale")

    # Social & Relationships
    social_interactions = models.IntegerField(default=0, help_text="Number of meaningful conversations")
    family_time_minutes = models.IntegerField(default=0)
    relationship_stress = models.IntegerField(default=3, help_text="1-10 scale")
    social_satisfaction = models.IntegerField(default=5, help_text="1-10 scale")
    conflict_count = models.IntegerField(default=0, help_text="Number of conflicts today")

    # Extracurricular
    extracurricular_hours = models.FloatField(default=0)
    hobby_time_minutes = models.IntegerField(default=0)
    club_activities = models.BooleanField(default=False)

    # Mood & Mental State
    mood_score = models.IntegerField(default=5, help_text="1-10 scale (1=terrible, 10=amazing)")
    anxiety_level = models.IntegerField(default=3, help_text="1-10 scale")
    focus_level = models.IntegerField(default=5, help_text="1-10 scale")
    motivation_level = models.IntegerField(default=5, help_text="1-10 scale")
    overthinking_episodes = models.IntegerField(default=0)

    # Typing/Digital Behavior (proxy signals)
    avg_typing_speed = models.IntegerField(default=0, help_text="WPM average")
    typo_frequency = models.IntegerField(default=0, help_text="Typos per 100 words")
    notification_count = models.IntegerField(default=0)
    phone_pickups = models.IntegerField(default=0)

    # Notes
    journal_entry = models.TextField(blank=True)
    stressors = models.TextField(blank=True, help_text="What's stressing you out?")

    # ML Prediction
    predicted_mental_load = models.CharField(max_length=20, choices=MENTAL_LOAD_CHOICES, blank=True)
    mental_load_score = models.FloatField(null=True, blank=True, help_text="0-100 score")
    ml_confidence = models.FloatField(null=True, blank=True)
    ai_recommendations = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
        unique_together = ['user', 'date']

    def __str__(self):
        return f"{self.user.username} - {self.date} - Load: {self.predicted_mental_load}"

    def get_load_color(self):
        colors = {
            'very_low': '#10b981',
            'low': '#34d399',
            'moderate': '#f59e0b',
            'high': '#ef4444',
            'critical': '#dc2626',
        }
        return colors.get(self.predicted_mental_load, '#6b7280')

    def get_load_emoji(self):
        emojis = {
            'very_low': '😊',
            'low': '🙂',
            'moderate': '😐',
            'high': '😟',
            'critical': '😰',
        }
        return emojis.get(self.predicted_mental_load, '🤔')


class WeeklyInsight(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='weekly_insights')
    week_start = models.DateField()
    week_end = models.DateField()
    avg_mental_load_score = models.FloatField(default=0)
    dominant_stressor = models.CharField(max_length=100, blank=True)
    improvement_areas = models.TextField(blank=True)
    positive_trends = models.TextField(blank=True)
    generated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Week of {self.week_start}"


class Streak(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='streak')
    current_streak = models.IntegerField(default=0)
    longest_streak = models.IntegerField(default=0)
    last_log_date = models.DateField(null=True, blank=True)
    total_logs = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.current_streak} day streak"
