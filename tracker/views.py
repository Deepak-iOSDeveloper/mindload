from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.db.models import Avg, Count
from datetime import date, timedelta
import json

from .models import DailyLog, UserProfile, WeeklyInsight, Streak
from .forms import DailyLogForm
from ml_engine.predictor import calculate_mental_load_score, get_trend_analysis, get_weekly_summary


def home(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'tracker/home.html')


@login_required
def dashboard(request):
    today = date.today()
    user = request.user

    # Get or create streak
    streak, _ = Streak.objects.get_or_create(user=user)

    # Today's log
    today_log = DailyLog.objects.filter(user=user, date=today).first()

    # Recent logs (last 7 days)
    recent_logs = DailyLog.objects.filter(
        user=user,
        date__gte=today - timedelta(days=6)
    ).order_by('date')

    # Last 30 days for chart
    last_30 = DailyLog.objects.filter(
        user=user,
        date__gte=today - timedelta(days=29)
    ).order_by('date')

    # Chart data
    chart_labels = []
    chart_scores = []
    for log in last_30:
        chart_labels.append(log.date.strftime('%b %d'))
        chart_scores.append(log.mental_load_score or 0)

    # Stats
    trend_data = get_trend_analysis(list(last_30))

    # Weekly summary
    week_logs = list(DailyLog.objects.filter(
        user=user,
        date__gte=today - timedelta(days=6)
    ))
    weekly = get_weekly_summary(week_logs)

    # Recommendations from today
    recommendations = []
    if today_log and today_log.ai_recommendations:
        try:
            recommendations = json.loads(today_log.ai_recommendations)
        except Exception:
            recommendations = []

    # Load distribution for pie chart
    load_dist = {
        'very_low': 0, 'low': 0, 'moderate': 0, 'high': 0, 'critical': 0
    }
    for log in last_30:
        if log.predicted_mental_load:
            load_dist[log.predicted_mental_load] = load_dist.get(log.predicted_mental_load, 0) + 1

    # Streak update
    if today_log:
        if streak.last_log_date != today:
            if streak.last_log_date == today - timedelta(days=1):
                streak.current_streak += 1
            else:
                streak.current_streak = 1
            streak.last_log_date = today
            streak.total_logs += 1
            if streak.current_streak > streak.longest_streak:
                streak.longest_streak = streak.current_streak
            streak.save()

    context = {
        'today_log': today_log,
        'recent_logs': recent_logs,
        'chart_labels': json.dumps(chart_labels),
        'chart_scores': json.dumps(chart_scores),
        'trend_data': trend_data,
        'weekly': weekly,
        'recommendations': recommendations,
        'streak': streak,
        'load_dist': json.dumps(list(load_dist.values())),
        'today': today,
    }
    return render(request, 'tracker/dashboard.html', context)


@login_required
def log_today(request):
    today = date.today()
    user = request.user
    existing_log = DailyLog.objects.filter(user=user, date=today).first()

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=existing_log)
        if form.is_valid():
            log = form.save(commit=False)
            log.user = user
            log.date = today

            # Build data dict from cleaned form data for ML
            log_data = {
                'study_hours': log.study_hours,
                'break_count': log.break_count,
                'tasks_pending': log.tasks_pending,
                'deadline_stress': log.deadline_stress,
                'sleep_hours': log.sleep_hours,
                'sleep_quality': log.sleep_quality,
                'bedtime_hour': log.bedtime_hour,
                'exercise_minutes': log.exercise_minutes,
                'physical_fatigue': log.physical_fatigue,
                'screen_time_hours': log.screen_time_hours,
                'social_media_hours': log.social_media_hours,
                'phone_pickups': log.phone_pickups,
                'notification_count': log.notification_count,
                'relationship_stress': log.relationship_stress,
                'social_satisfaction': log.social_satisfaction,
                'conflict_count': log.conflict_count,
                'social_interactions': log.social_interactions,
                'mood_score': log.mood_score,
                'anxiety_level': log.anxiety_level,
                'focus_level': log.focus_level,
                'motivation_level': log.motivation_level,
                'overthinking_episodes': log.overthinking_episodes,
            }

            result = calculate_mental_load_score(log_data)

            log.mental_load_score = result['score']
            log.predicted_mental_load = result['category']
            log.ml_confidence = result['confidence']
            log.ai_recommendations = json.dumps(result['recommendations'])
            log.save()

            messages.success(request, f"✅ Log saved! Your mental load today: {result['category_label']} ({result['score']:.0f}/100)")
            return redirect('dashboard')
        else:
            # Show form errors in message
            error_msg = "Please fix the errors below: " + str(form.errors)
            messages.error(request, error_msg)
    else:
        form = DailyLogForm(instance=existing_log)

    return render(request, 'tracker/log_form.html', {
        'form': form,
        'today': today,
        'is_edit': existing_log is not None,
    })


@login_required
def history(request):
    user = request.user
    logs = DailyLog.objects.filter(user=user).order_by('-date')[:60]

    # Monthly averages
    monthly_data = {}
    for log in logs:
        month_key = log.date.strftime('%b %Y')
        if month_key not in monthly_data:
            monthly_data[month_key] = []
        if log.mental_load_score:
            monthly_data[month_key].append(log.mental_load_score)

    monthly_avgs = {k: round(sum(v)/len(v), 1) for k, v in monthly_data.items() if v}

    return render(request, 'tracker/history.html', {
        'logs': logs,
        'monthly_avgs': monthly_avgs,
    })


@login_required
def log_detail(request, pk):
    log = get_object_or_404(DailyLog, pk=pk, user=request.user)
    recommendations = []
    if log.ai_recommendations:
        try:
            recommendations = json.loads(log.ai_recommendations)
        except Exception:
            pass

    return render(request, 'tracker/log_detail.html', {
        'log': log,
        'recommendations': recommendations,
    })


@login_required
def insights(request):
    user = request.user
    today = date.today()

    all_logs = list(DailyLog.objects.filter(user=user).order_by('-date'))
    trend_data = get_trend_analysis(all_logs)

    # Best & worst days
    scored_logs = [l for l in all_logs if l.mental_load_score is not None]
    best_day = min(scored_logs, key=lambda x: x.mental_load_score) if scored_logs else None
    worst_day = max(scored_logs, key=lambda x: x.mental_load_score) if scored_logs else None

    # Averages
    avg_sleep = sum(l.sleep_hours for l in all_logs) / max(len(all_logs), 1)
    avg_exercise = sum(l.exercise_minutes for l in all_logs) / max(len(all_logs), 1)
    avg_mood = sum(l.mood_score for l in all_logs) / max(len(all_logs), 1)
    avg_study = sum(l.study_hours for l in all_logs) / max(len(all_logs), 1)

    # Chart: sleep vs load
    sleep_chart_data = [
        {'sleep': l.sleep_hours, 'load': l.mental_load_score or 0}
        for l in all_logs[:30]
    ]

    streak, _ = Streak.objects.get_or_create(user=user)

    return render(request, 'tracker/insights.html', {
        'trend_data': trend_data,
        'best_day': best_day,
        'worst_day': worst_day,
        'avg_sleep': round(avg_sleep, 1),
        'avg_exercise': round(avg_exercise, 1),
        'avg_mood': round(avg_mood, 1),
        'avg_study': round(avg_study, 1),
        'total_logs': len(all_logs),
        'streak': streak,
        'sleep_chart_data': json.dumps(sleep_chart_data),
    })


@login_required
def api_quick_log(request):
    """API endpoint for quick mood check-in."""
    if request.method == 'POST':
        data = json.loads(request.body)
        mood = int(data.get('mood', 5))
        anxiety = int(data.get('anxiety', 3))
        today = date.today()

        log, created = DailyLog.objects.get_or_create(
            user=request.user, date=today,
            defaults={'mood_score': mood, 'anxiety_level': anxiety}
        )
        if not created:
            log.mood_score = mood
            log.anxiety_level = anxiety
            log.save()

        return JsonResponse({'status': 'ok', 'message': 'Quick check-in saved!'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def api_chart_data(request):
    """API for dynamic chart data."""
    days = int(request.GET.get('days', 7))
    today = date.today()
    logs = DailyLog.objects.filter(
        user=request.user,
        date__gte=today - timedelta(days=days-1)
    ).order_by('date')

    data = {
        'labels': [l.date.strftime('%b %d') for l in logs],
        'scores': [l.mental_load_score or 0 for l in logs],
        'moods': [l.mood_score for l in logs],
        'sleep': [l.sleep_hours for l in logs],
    }
    return JsonResponse(data)