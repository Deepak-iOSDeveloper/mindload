# 🧠 MindLoad — AI Mental Load Tracker

A full-stack Django web app that tracks 30+ daily signals and uses a weighted ML engine to predict your mental load score (0-100) with personalized AI recommendations.

---

## 🚀 Quick Setup (5 minutes)

### 1. Install Python dependencies
```bash
pip install -r requirements.txt
```

### 2. Run database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 3. Create a superuser (optional, for admin access)
```bash
python manage.py createsuperuser
```

### 4. Start the development server
```bash
python manage.py runserver
```

### 5. Open in browser
```
http://127.0.0.1:8000/
```

---

## 📁 Project Structure

```
mindload/
├── mindload/          # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── tracker/           # Main app (logs, dashboard, insights)
│   ├── models.py      # DailyLog, UserProfile, Streak
│   ├── views.py       # All page views
│   ├── forms.py       # DailyLogForm
│   ├── urls.py
│   └── templates/
│       └── tracker/
│           ├── home.html
│           ├── dashboard.html
│           ├── log_form.html
│           ├── log_detail.html
│           ├── history.html
│           └── insights.html
├── accounts/          # Auth (register, login, profile)
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   └── templates/
│       └── accounts/
├── ml_engine/         # ML prediction logic
│   └── predictor.py   # Weighted scoring engine
├── templates/
│   └── base.html      # Global layout
├── requirements.txt
└── manage.py
```

---

## 🤖 How the ML Engine Works

The `ml_engine/predictor.py` file contains a weighted scoring system:

| Signal Component     | Weight |
|---------------------|--------|
| Sleep Quality        | 25%    |
| Study Stress         | 20%    |
| Mood & Mental State  | 15%    |
| Physical Wellbeing   | 15%    |
| Social Relationships | 15%    |
| Digital Behavior     | 10%    |

**Score → Category:**
- 0–20: Very Low 😊
- 21–40: Low 🙂
- 41–60: Moderate 😐
- 61–80: High 😟
- 81–100: Critical 😰

### Upgrade to Real ML:
Once you have 100+ logs, you can train a real scikit-learn model:
```python
from sklearn.ensemble import RandomForestRegressor
# Use DailyLog data as features → mental_load_score as target
```

---

## 🌐 Deployment (Railway/Render/Heroku)

1. Set `DEBUG = False` in settings.py
2. Set `SECRET_KEY` as environment variable
3. Add `whitenoise` for static files (already in requirements)
4. Run `python manage.py collectstatic`

---

## 📊 Features

- ✅ User registration & authentication
- ✅ Daily log form (30+ signals across 8 categories)
- ✅ ML mental load score (0-100) with category labels
- ✅ Personalized AI recommendations
- ✅ Dashboard with Chart.js visualizations
- ✅ 30-day trend line + load distribution pie chart
- ✅ Full history browser
- ✅ Insights page with sleep vs load scatter plot
- ✅ Streak tracking
- ✅ Mobile-responsive dark UI

---

## 🔮 Future Roadmap

- [ ] Train a real RandomForest/XGBoost model on accumulated data
- [ ] Weekly email digest
- [ ] Browser extension for auto screen time tracking
- [ ] iOS companion app (SwiftUI)
- [ ] Social sharing of insights (anonymized)
- [ ] Therapist/counselor dashboard view

---

Built with Python, Django, and ❤️ by Deepak
