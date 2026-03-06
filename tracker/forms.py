from django import forms
from .models import DailyLog


class DailyLogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make ALL fields optional — missing fields fall back to model defaults
        for field_name, field in self.fields.items():
            field.required = False

    class Meta:
        model = DailyLog
        exclude = [
            'user', 'date', 'created_at',
            'predicted_mental_load', 'mental_load_score',
            'ml_confidence', 'ai_recommendations'
        ]
        widgets = {
            # Study & Work
            'study_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 24, 'step': 0.5, 'placeholder': '0'}),
            'break_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': '0'}),
            'avg_break_duration': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': 'minutes'}),
            'tasks_completed': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': '0'}),
            'tasks_pending': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': '0'}),
            'deadline_stress': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),

            # Screen time
            'screen_time_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 24, 'step': 0.5}),
            'social_media_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 24, 'step': 0.5}),
            'productive_app_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.5}),
            'entertainment_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.5}),

            # Sleep
            'sleep_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 24, 'step': 0.5}),
            'sleep_quality': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'bedtime_hour': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 23}),
            'wake_time_hour': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'max': 23}),

            # Exercise
            'exercise_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'exercise_type': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'e.g. Running, Yoga, Gym'}),
            'steps_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': '0'}),
            'physical_fatigue': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),

            # Social
            'social_interactions': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'family_time_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'relationship_stress': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'social_satisfaction': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'conflict_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),

            # Extracurricular
            'extracurricular_hours': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'step': 0.5}),
            'hobby_time_minutes': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'club_activities': forms.CheckboxInput(attrs={'class': 'form-checkbox'}),

            # Mood
            'mood_score': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'anxiety_level': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'focus_level': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'motivation_level': forms.NumberInput(attrs={'class': 'form-input range-input', 'type': 'range', 'min': 1, 'max': 10}),
            'overthinking_episodes': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),

            # Digital behavior
            'avg_typing_speed': forms.NumberInput(attrs={'class': 'form-input', 'min': 0, 'placeholder': 'WPM'}),
            'typo_frequency': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'notification_count': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'phone_pickups': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),

            # Notes
            'journal_entry': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4, 'placeholder': "How was your day? What's on your mind?"}),
            'stressors': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 3, 'placeholder': "What's stressing you out today?"}),
        }
