from flask import Flask, render_template, request, jsonify, session
from groq import Groq
from dotenv import load_dotenv
import json
import os
import re
from datetime import datetime

load_dotenv()

app = Flask(__name__)
app.secret_key = "elisavoz-sofia-2024"

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

CURRICULUM = {
    "1":  {"name": "Greetings & Introductions",
           "category": "Core Language",
           "description": "Hello, goodbye, meeting people",
           "emoji": "👋", "roleplay": None},
    "2":  {"name": "Numbers & Time",
           "category": "Core Language",
           "description": "Count, tell time, dates, years",
           "emoji": "🔢", "roleplay": None},
    "3":  {"name": "Colors & Descriptions",
           "category": "Core Language",
           "description": "Describe people, places and things",
           "emoji": "🎨", "roleplay": None},
    "4":  {"name": "Family & Relationships",
           "category": "Core Language",
           "description": "Family members, love, friendship",
           "emoji": "👨‍👩‍👧‍👦", "roleplay": None},
    "5":  {"name": "Food & Daily Life",
           "category": "Core Language",
           "description": "Meals, cooking, daily routines",
           "emoji": "🍽️", "roleplay": None},
    "6":  {"name": "Shopping & Money",
           "category": "Core Language",
           "description": "Prices, buying, bargaining",
           "emoji": "🛍️", "roleplay": None},
    "7":  {"name": "Directions & Travel",
           "category": "Core Language",
           "description": "Navigate cities and countries",
           "emoji": "🗺️", "roleplay": None},
    "8":  {"name": "Health & Body",
           "category": "Core Language",
           "description": "Body parts, feelings, medical",
           "emoji": "❤️", "roleplay": None},
    "9":  {"name": "Work & School",
           "category": "Core Language",
           "description": "Jobs, education, professional life",
           "emoji": "💼", "roleplay": None},
    "10": {"name": "Culture & Celebrations",
           "category": "Core Language",
           "description": "Holidays, traditions, customs",
           "emoji": "🎉", "roleplay": None},
    "11": {"name": "At the Taco Shop",
           "category": "Real Life Scenarios",
           "description": "Order food, ask prices, customize meal",
           "emoji": "🌮", "roleplay": "taquero"},
    "12": {"name": "At the Restaurant",
           "category": "Real Life Scenarios",
           "description": "Reserve tables, order, complain politely",
           "emoji": "🍴", "roleplay": "waiter"},
    "13": {"name": "At the Market",
           "category": "Real Life Scenarios",
           "description": "Buy fresh produce, bargain, quantities",
           "emoji": "🥦", "roleplay": "market vendor"},
    "14": {"name": "At the Doctor",
           "category": "Real Life Scenarios",
           "description": "Describe symptoms, understand advice",
           "emoji": "🏥", "roleplay": "doctor"},
    "15": {"name": "At the Bank",
           "category": "Real Life Scenarios",
           "description": "Transactions, exchange, account help",
           "emoji": "🏦", "roleplay": "bank teller"},
    "16": {"name": "At the Airport",
           "category": "Real Life Scenarios",
           "description": "Check in, customs, finding gates",
           "emoji": "✈️", "roleplay": "airport staff"},
    "17": {"name": "At the Hotel",
           "category": "Real Life Scenarios",
           "description": "Check in, requests, complaints",
           "emoji": "🏨", "roleplay": "hotel receptionist"},
    "18": {"name": "At the Park",
           "category": "Real Life Scenarios",
           "description": "Recreation, sports, meeting locals",
           "emoji": "🌳", "roleplay": None},
    "19": {"name": "At the Gym",
           "category": "Real Life Scenarios",
           "description": "Equipment, routines, fitness talk",
           "emoji": "💪", "roleplay": "gym trainer"},
    "20": {"name": "At the Barbershop",
           "category": "Real Life Scenarios",
           "description": "Describe haircuts, grooming requests",
           "emoji": "✂️", "roleplay": "barber"},
    "21": {"name": "At the Cinema",
           "category": "Real Life Scenarios",
           "description": "Buy tickets, discuss movies",
           "emoji": "🎬", "roleplay": "ticket seller"},
    "22": {"name": "At the Bus Station",
           "category": "Real Life Scenarios",
           "description": "Buy tickets, ask routes, schedules",
           "emoji": "🚌", "roleplay": "ticket agent"},
    "23": {"name": "At the Pharmacy",
           "category": "Real Life Scenarios",
           "description": "Medications, dosage, health products",
           "emoji": "💊", "roleplay": "pharmacist"},
    "24": {"name": "At the Fiesta",
           "category": "Real Life Scenarios",
           "description": "Party conversation, toasts, dancing",
           "emoji": "🎊", "roleplay": None},
    "25": {"name": "At the Beach",
           "category": "Real Life Scenarios",
           "description": "Water activities, vendors, directions",
           "emoji": "🏖️", "roleplay": None},
    "26": {"name": "Spanish for Students",
           "category": "Professional Tracks",
           "description": "Academic vocabulary, classroom language",
           "emoji": "📚", "roleplay": "professor"},
    "27": {"name": "Spanish for Healthcare",
           "category": "Professional Tracks",
           "description": "Medical terminology, patient care",
           "emoji": "🩺", "roleplay": "patient"},
    "28": {"name": "Spanish for Business",
           "category": "Professional Tracks",
           "description": "Meetings, negotiations, presentations",
           "emoji": "📊", "roleplay": "business partner"},
    "29": {"name": "Spanish for Teachers",
           "category": "Professional Tracks",
           "description": "Classroom management, parent communication",
           "emoji": "👩‍🏫", "roleplay": "student"},
    "30": {"name": "Spanish for Travellers",
           "category": "Professional Tracks",
           "description": "Survival Spanish for any destination",
           "emoji": "🌍", "roleplay": "local guide"},
    "31": {"name": "Spanish for Parents",
           "category": "Professional Tracks",
           "description": "Talk with your child's school and community",
           "emoji": "👨‍👩‍👦", "roleplay": "teacher"},
    "32": {"name": "Spanish for Social Workers",
           "category": "Professional Tracks",
           "description": "Community support, sensitive conversations",
           "emoji": "🤝", "roleplay": "community member"},
    "33": {"name": "Spanish for Law Enforcement",
           "category": "Professional Tracks",
           "description": "Safety, rights, community policing",
           "emoji": "🚔", "roleplay": "community member"},
    "34": {"name": "Spanish for Volunteers",
           "category": "Professional Tracks",
           "description": "Community service, outreach language",
           "emoji": "🙌", "roleplay": "community member"},
    "35": {"name": "Faith & Spirituality",
           "category": "Professional Tracks",
           "description": "Prayer, worship, ministry expressions",
           "emoji": "🙏", "roleplay": None},
}

def load_profile(name):
    profiles_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "profiles"
    )
    filename = os.path.join(
        profiles_dir, f"{name.lower()}.json"
    )
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return None

def save_profile(profile):
    profiles_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "profiles"
    )
    os.makedirs(profiles_dir, exist_ok=True)
    filename = os.path.join(
        profiles_dir,
        f"{profile['name'].lower()}.json"
    )
    with open(filename, "w") as f:
        json.dump(profile, f, indent=2)

def create_profile(name):
    return {
        "name": name,
        "level": "beginner",
        "sessions": 0,
        "topics_covered": [],
        "lessons_completed": [],
        "joined": datetime.now().strftime("%Y-%m-%d"),
        "last_session": "",
        "streak": 0,
        "detected_age_group": "adult",
        "total_words_learned": 0
    }

def extract_name(raw):
    text = raw.strip().lower()
    patterns = [
        r"\bmy name is\b", r"\bi am\b", r"\bi'm\b",
        r"\bme llamo\b", r"\bme llame es\b",
        r"\bme llame\b", r"\bmi nombre es\b",
        r"\bsoy\b", r"\bes\b", r"\bllamo\b",
        r"\bname is\b", r"\bname\b",
        r"\bmy\b", r"\bis\b",
    ]
    for p in patterns:
        text = re.sub(p, "", text)
    text = re.sub(r'[^\w\s]', '', text).strip()
    words = [w for w in text.split() if len(w) > 1]
    if words:
        return words[0].capitalize()
    fallback = raw.strip().split()
    return fallback[-1].capitalize() if fallback else "Amigo"

def build_system_prompt(profile, mode, lesson=None):
    topics = (profile['topics_covered']
              if profile['topics_covered'] else ["none yet"])
    completed = profile.get('lessons_completed', [])
    completed_names = [CURRICULUM[l]['name']
                       for l in completed if l in CURRICULUM]
    age_group = profile.get('detected_age_group', 'adult')

    base = f"""You are Sofia, the AI tutor of ElisaVoz.
You are warm, patient, encouraging and world class.

STUDENT PROFILE:
- Name: {profile['name']}
- Level: {profile['level']}
- Age group: {age_group}
- Sessions: {profile['sessions']}
- Lessons completed: {', '.join(completed_names)
  if completed_names else 'none yet'}
- Topics covered: {', '.join(topics)}

FORMATTING RULES:
Always put Spanish on one line,followed by space , then English directly below.
Example:
¡Muy bien, {profile['name']}!
Well done, {profile['name']}!

NEVER mix Spanish and English on the same line.
NEVER use parentheses like: ¡Hola! (Hello!)
ALWAYS Spanish first, English directly below.
One blank line between different thoughts.

TEACHING STYLE:
- Address student as {profile['name']} only
- Correct gently: "great try, we say it like this..."
- Never say "wrong" or "incorrect"
- Celebrate every small win
- Ask only ONE question at a time
- Adapt to age group naturally

TRACKING:
Age detected: include once as [AGE: child/teen/adult/senior]
New topics: include as [TOPIC: topic_name]

SIGN OFF: Always as: Con cariño, Sofia"""

    if mode == "free":
        base += f"""
MODE: Free conversation with {profile['name']}.
Natural flowing Spanish conversation.
Follow their interests. Correct gently."""

    elif mode == "continue":
        recent = topics[-3:] if len(topics) >= 3 else topics
        base += f"""
MODE: Continue from recent topics: {', '.join(recent)}
Build confidence then advance gently."""

    elif mode == "lesson" and lesson:
        roleplay = lesson.get('roleplay')
        if roleplay:
            base += f"""
MODE: Lesson with roleplay.
Topic: {lesson['name']} — {lesson['description']}
Also play role of: {roleplay}
Label switches clearly:
*As {roleplay}*:
Spanish dialogue
English below
*As Sofia*:
Teaching point
Build simple to complex."""
        else:
            base += f"""
MODE: Structured lesson.
Topic: {lesson['name']} — {lesson['description']}
Build simple to complex.
End with 5 key phrases learned."""

    return base

@app.route('/')
def index():
    session.clear()
    return render_template('index.html',
                           curriculum=CURRICULUM)

@app.route('/api/start', methods=['POST'])
def start():
    data = request.json
    raw_name = data.get('name', 'Amigo')
    name = extract_name(raw_name)
    profile = load_profile(name)

    if profile:
        today = datetime.now().strftime("%Y-%m-%d")
        last = profile.get('last_session', '')
        if last != today:
            profile['streak'] = (
                profile.get('streak', 0) + 1
            )
        profile['sessions'] += 1
        profile['last_session'] = today
        is_returning = True
    else:
        profile = create_profile(name)
        profile['sessions'] = 1
        profile['streak'] = 1
        profile['last_session'] = (
            datetime.now().strftime("%Y-%m-%d")
        )
        is_returning = False

    save_profile(profile)
    session['profile'] = profile
    session['history'] = []
    session['mode'] = 'free'
    session['lesson'] = None

    return jsonify({
        'name': name,
        'is_returning': is_returning,
        'profile': profile
    })

@app.route('/api/set_lesson', methods=['POST'])
def set_lesson():
    data = request.json
    lesson_id = data.get('lesson_id')
    mode = data.get('mode', 'lesson')
    session['mode'] = mode
    session['history'] = []

    if lesson_id and lesson_id in CURRICULUM:
        session['lesson'] = CURRICULUM[lesson_id]
        session['lesson_id'] = lesson_id
    else:
        session['lesson'] = None
        session['lesson_id'] = None

    return jsonify({'status': 'ok'})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    profile = session.get('profile', {})
    history = session.get('history', [])
    mode = session.get('mode', 'free')
    lesson = session.get('lesson', None)

    system_prompt = build_system_prompt(
        profile, mode, lesson
    )

    history.append({
        "role": "user",
        "content": user_message
    })

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": system_prompt},
            *history
        ]
    )

    reply = response.choices[0].message.content
    display = re.sub(
        r'\[TOPIC:[^\]]+\]|\[LESSON_COMPLETE\]'
        r'|\[AGE:[^\]]+\]'
        r'|AGE:\s*(adult|teen|child|senior)',
        '', reply, flags=re.IGNORECASE
    ).strip()

    history.append({
        "role": "assistant",
        "content": reply
    })

    if "[TOPIC:" in reply:
        found = re.findall(r'\[TOPIC: ([^\]]+)\]', reply)
        for t in found:
            if t not in profile.get('topics_covered', []):
                profile.setdefault(
                    'topics_covered', []
                ).append(t)

    if "[AGE:" in reply:
        age_found = re.findall(
            r'\[AGE:\s*([^\]]+)\]', reply
        )
        if age_found:
            profile['detected_age_group'] = (
                age_found[-1].strip().lower()
            )

    session['history'] = history
    session['profile'] = profile
    save_profile(profile)

    return jsonify({'response': display})

@app.route('/api/end_lesson', methods=['POST'])
def end_lesson():
    profile = session.get('profile', {})
    history = session.get('history', [])
    lesson = session.get('lesson', None)
    lesson_id = session.get('lesson_id', None)
    lesson_completed = False

    if lesson and lesson_id:
        lessons_done = profile.setdefault(
            'lessons_completed', []
        )
        if lesson_id not in lessons_done:
            lessons_done.append(lesson_id)
            lesson_completed = True

    summary = ""
    if len(history) >= 2:
        prompt = f"""Create a warm session summary
for {profile['name']} including:
1. THREE phrases practiced — Spanish line then English line
2. TWO corrections — wrong then correct then English
3. ONE encouraging observation
4. THREE phrases to review — Spanish then English
5. ONE closing — Spanish line then English line
Sign off as: Con cariño, Sofia
Never use [Your Name] placeholder."""

        sum_response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                *history,
                {"role": "user", "content": prompt}
            ]
        )
        summary = sum_response.choices[0].message.content

    save_profile(profile)
    session['profile'] = profile

    return jsonify({
        'summary': summary,
        'lesson_completed': lesson_completed,
        'lesson_name': lesson['name'] if lesson else '',
        'progress': len(
            profile.get('lessons_completed', [])
        ),
        'profile': profile
    })

@app.route('/api/profile', methods=['GET'])
def get_profile():
    name = request.args.get('name', '')
    profile = load_profile(name)
    if profile:
        completed = profile.get('lessons_completed', [])
        completed_lessons = [
            {
                'id': k,
                'name': CURRICULUM[k]['name'],
                'emoji': CURRICULUM[k]['emoji'],
                'category': CURRICULUM[k]['category']
            }
            for k in completed if k in CURRICULUM
        ]
        return jsonify({
            'profile': profile,
            'completed_lessons': completed_lessons,
            'total_lessons': len(CURRICULUM)
        })
    return jsonify({'error': 'Profile not found'}), 404

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(debug=False, port=port, host='0.0.0.0')
