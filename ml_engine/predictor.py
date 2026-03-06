"""
MindLoad ML Engine
Rule-based + weighted scoring mental load predictor.
Can be replaced with a trained sklearn model once enough data is collected.
"""
import math
import json
from datetime import date, timedelta


def calculate_mental_load_score(log_data: dict) -> dict:
    """
    Calculate mental load score from daily log data.
    Returns score (0-100), category, confidence, and recommendations.
    
    Score interpretation:
    0-20:  Very Low
    21-40: Low
    41-60: Moderate
    61-80: High
    81-100: Critical
    """
    score = 0.0
    factors = {}
    recommendations = []

    # ─── STUDY STRESS COMPONENT (weight: 20%) ───────────────────────────────
    study_hours = float(log_data.get('study_hours', 0))
    tasks_pending = int(log_data.get('tasks_pending', 0))
    deadline_stress = int(log_data.get('deadline_stress', 5))
    break_count = int(log_data.get('break_count', 0))

    study_score = 0
    if study_hours > 10:
        study_score += 40
    elif study_hours > 7:
        study_score += 25
    elif study_hours > 4:
        study_score += 10

    # Penalize no breaks during long study sessions
    if study_hours > 3 and break_count == 0:
        study_score += 20
        recommendations.append("📚 You studied for a long time without breaks. Try the Pomodoro technique: 25 min study, 5 min break.")
    elif study_hours > 3 and break_count < 2:
        study_score += 10

    study_score += min(tasks_pending * 5, 25)
    study_score += (deadline_stress - 5) * 3 if deadline_stress > 5 else 0
    study_score = min(study_score, 100)
    factors['study_stress'] = round(study_score, 1)

    if deadline_stress >= 8:
        recommendations.append("⏰ High deadline stress detected. Break tasks into 30-minute chunks and tackle one at a time.")

    # ─── SLEEP QUALITY COMPONENT (weight: 25%) ──────────────────────────────
    sleep_hours = float(log_data.get('sleep_hours', 7))
    sleep_quality = int(log_data.get('sleep_quality', 5))
    bedtime = int(log_data.get('bedtime_hour', 23))

    sleep_score = 0
    if sleep_hours < 5:
        sleep_score += 60
        recommendations.append("😴 Critical sleep deprivation! Less than 5 hours severely impacts cognitive function. Prioritize sleep tonight.")
    elif sleep_hours < 6:
        sleep_score += 40
        recommendations.append("😴 You're running on low sleep. Aim for at least 7-8 hours tonight.")
    elif sleep_hours < 7:
        sleep_score += 20
    elif sleep_hours >= 9:
        sleep_score += 10  # Oversleeping can also indicate low mood

    sleep_score += (10 - sleep_quality) * 4
    if bedtime >= 2 and bedtime <= 5:  # 2 AM - 5 AM
        sleep_score += 15
        recommendations.append("🌙 Late-night sleeping disrupts your circadian rhythm. Try to sleep before midnight.")

    sleep_score = min(sleep_score, 100)
    factors['sleep_quality'] = round(sleep_score, 1)

    # ─── PHYSICAL WELLBEING COMPONENT (weight: 15%) ─────────────────────────
    exercise_mins = int(log_data.get('exercise_minutes', 0))
    physical_fatigue = int(log_data.get('physical_fatigue', 5))

    phys_score = 0
    if exercise_mins == 0:
        phys_score += 25
        recommendations.append("🏃 No exercise today. Even a 15-minute walk can reduce mental load by 30%.")
    elif exercise_mins < 20:
        phys_score += 10

    phys_score += (physical_fatigue - 5) * 5 if physical_fatigue > 5 else 0
    phys_score = min(phys_score, 100)
    factors['physical_wellbeing'] = round(phys_score, 1)

    # ─── SOCIAL & RELATIONSHIP COMPONENT (weight: 15%) ──────────────────────
    relationship_stress = int(log_data.get('relationship_stress', 3))
    social_satisfaction = int(log_data.get('social_satisfaction', 5))
    conflict_count = int(log_data.get('conflict_count', 0))
    social_interactions = int(log_data.get('social_interactions', 0))

    social_score = 0
    social_score += (relationship_stress - 3) * 7 if relationship_stress > 3 else 0
    social_score += (5 - social_satisfaction) * 5 if social_satisfaction < 5 else 0
    social_score += conflict_count * 15
    if social_interactions == 0:
        social_score += 15
        recommendations.append("👥 Social isolation increases mental load. Reach out to a friend or family member today.")

    social_score = min(social_score, 100)
    factors['social_relationships'] = round(social_score, 1)

    if conflict_count > 0:
        recommendations.append(f"💬 You had {conflict_count} conflict(s) today. Try journaling to process these emotions before sleep.")

    # ─── SCREEN & DIGITAL BEHAVIOR COMPONENT (weight: 10%) ──────────────────
    screen_time = float(log_data.get('screen_time_hours', 0))
    social_media = float(log_data.get('social_media_hours', 0))
    phone_pickups = int(log_data.get('phone_pickups', 0))
    notification_count = int(log_data.get('notification_count', 0))

    digital_score = 0
    if screen_time > 10:
        digital_score += 30
        recommendations.append("📱 High screen time detected. Consider a 1-hour phone-free period before bed.")
    elif screen_time > 7:
        digital_score += 15

    if social_media > 3:
        digital_score += 25
        recommendations.append("📲 Heavy social media use increases anxiety. Try limiting to 1 hour/day.")
    elif social_media > 2:
        digital_score += 10

    digital_score += min(phone_pickups // 10, 20)
    digital_score += min(notification_count // 20, 15)
    digital_score = min(digital_score, 100)
    factors['digital_behavior'] = round(digital_score, 1)

    # ─── MOOD & MENTAL STATE COMPONENT (weight: 15%) ─────────────────────────
    mood_score = int(log_data.get('mood_score', 5))
    anxiety_level = int(log_data.get('anxiety_level', 3))
    focus_level = int(log_data.get('focus_level', 5))
    motivation_level = int(log_data.get('motivation_level', 5))
    overthinking = int(log_data.get('overthinking_episodes', 0))

    mood_component = 0
    mood_component += (10 - mood_score) * 5
    mood_component += anxiety_level * 5
    mood_component += (10 - focus_level) * 3
    mood_component += (10 - motivation_level) * 3
    mood_component += min(overthinking * 10, 30)
    mood_component = min(mood_component, 100)
    factors['mood_mental_state'] = round(mood_component, 1)

    if anxiety_level >= 7:
        recommendations.append("🧘 High anxiety detected. Try box breathing: 4s inhale, 4s hold, 4s exhale, 4s hold. Repeat 4 times.")
    if overthinking > 3:
        recommendations.append("🌀 Multiple overthinking episodes. Write down your top 3 worries and a small action for each.")

    # ─── WEIGHTED FINAL SCORE ────────────────────────────────────────────────
    weights = {
        'study_stress': 0.20,
        'sleep_quality': 0.25,
        'physical_wellbeing': 0.15,
        'social_relationships': 0.15,
        'digital_behavior': 0.10,
        'mood_mental_state': 0.15,
    }

    final_score = sum(factors[k] * weights[k] for k in factors)
    final_score = round(final_score, 1)

    # Determine category
    if final_score <= 20:
        category = 'very_low'
        category_label = 'Very Low'
    elif final_score <= 40:
        category = 'low'
        category_label = 'Low'
    elif final_score <= 60:
        category = 'moderate'
        category_label = 'Moderate'
    elif final_score <= 80:
        category = 'high'
        category_label = 'High'
    else:
        category = 'critical'
        category_label = 'Critical'

    # Positive affirmations based on score
    if final_score <= 30:
        recommendations.insert(0, "✨ You're managing your mental load really well today. Keep up the great habits!")
    elif final_score <= 50:
        recommendations.insert(0, "👍 Decent day overall. A few small tweaks can make it even better!")
    elif final_score >= 75:
        recommendations.insert(0, "🚨 Your mental load is very high. Please prioritize rest and reach out to someone you trust.")

    # Default recommendation
    if not recommendations:
        recommendations.append("💡 Keep tracking daily to see patterns in your mental load over time.")

    # Confidence (mock: based on data completeness)
    filled_fields = sum(1 for v in log_data.values() if v not in [0, '', None, False])
    confidence = min(0.95, 0.50 + (filled_fields / 40) * 0.45)

    return {
        'score': final_score,
        'category': category,
        'category_label': category_label,
        'confidence': round(confidence, 2),
        'factors': factors,
        'recommendations': recommendations[:5],  # Top 5 recommendations
        'recommendations_json': json.dumps(recommendations[:5]),
    }


def get_trend_analysis(logs_queryset) -> dict:
    """Analyze trends from multiple daily logs."""
    if not logs_queryset:
        return {}

    scores = [log.mental_load_score for log in logs_queryset if log.mental_load_score is not None]
    if not scores:
        return {}

    avg_score = sum(scores) / len(scores)
    trend = 'stable'

    if len(scores) >= 3:
        recent_avg = sum(scores[:3]) / 3
        older_avg = sum(scores[3:6]) / max(len(scores[3:6]), 1) if len(scores) > 3 else avg_score
        diff = recent_avg - older_avg
        if diff > 10:
            trend = 'worsening'
        elif diff < -10:
            trend = 'improving'

    return {
        'avg_score': round(avg_score, 1),
        'max_score': max(scores),
        'min_score': min(scores),
        'trend': trend,
        'total_days': len(scores),
    }


def get_weekly_summary(logs) -> dict:
    """Generate weekly summary insights."""
    if not logs:
        return {}

    total_sleep = sum(l.sleep_hours for l in logs) / len(logs)
    total_exercise = sum(l.exercise_minutes for l in logs)
    avg_mood = sum(l.mood_score for l in logs) / len(logs)
    avg_load = sum(l.mental_load_score or 0 for l in logs) / len(logs)
    high_load_days = sum(1 for l in logs if l.mental_load_score and l.mental_load_score > 60)

    return {
        'avg_sleep': round(total_sleep, 1),
        'total_exercise_mins': total_exercise,
        'avg_mood': round(avg_mood, 1),
        'avg_load_score': round(avg_load, 1),
        'high_load_days': high_load_days,
        'log_count': len(logs),
    }
