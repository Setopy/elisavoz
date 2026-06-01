# ElisaVoz

Find Your Spanish Voice.

---

## Live

[elisavoz.com](https://elisavoz.com)

---

## What it is

ElisaVoz is a free Spanish learning app.
It uses AI to give every learner a personal tutor 
named Sofia.

Sofia is patient, warm and bilingual. She teaches 
Spanish through
real conversation, corrects mistakes gently, and 
adapts to whoever
she is talking to — a child, a teenager, a working 
adult or a senior.

---

## What it does

- Sofia talks to you in both Spanish and English
- You can type or speak to her using your microphone
- She speaks back in Spanish with natural rhythm and 
emotion
- You control how fast or slow she speaks
- Your progress is saved between sessions
- Multiple people can use it on the same device with 
separate profiles

---

## Lessons

There are 35 lessons across three areas.

**Core Language**
Greetings, numbers, colors, family, food, shopping,
directions, health, work and culture.

**Real Life Scenarios**
At the taco shop, restaurant, market, doctor, bank, 
airport,
hotel, park, gym, barbershop, cinema, bus station,
pharmacy, fiesta and beach.

**Professional Tracks**
Spanish for students, healthcare workers, business 
professionals,
teachers, travellers, parents, social workers, law 
enforcement,
volunteers and faith ministry.

---

## How it was built

The backend is Python and Flask. The AI brain is 
Llama 3.3 running
on Groq. Voice input and output use the browser's 
built-in Web
Speech API. The app is hosted on Railway and the 
domain is
registered through Namecheap.

---

## Run it locally

```bash
git clone https://github.com/Setopy/elisavoz.git
cd elisavoz/web
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
echo "GROQ_API_KEY=your-key-here" > .env
python3.11 app.py
```

Then open your browser at localhost:8080.

You will need a free Groq API key from 
console.groq.com.

---

## What is coming next

- Android app on the Play Store
- Offline mode
- Pronunciation scoring
- Custom voice for Sofia

---

MIT License
