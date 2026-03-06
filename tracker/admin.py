from django.contrib import admin
from .models import DailyLog, UserProfile, WeeklyInsight, Streak


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'date', 'mental_load_score', 'predicted_mental_load', 'mood_score', 'sleep_hours', 'study_hours']
    list_filter = ['predicted_mental_load', 'date']
    search_fields = ['user__username']
    ordering = ['-date']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'age', 'gender', 'occupation']


@admin.register(Streak)
class StreakAdmin(admin.ModelAdmin):
    list_display = ['user', 'current_streak', 'longest_streak', 'total_logs']
