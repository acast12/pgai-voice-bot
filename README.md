# PGAI Voice Bot — Patient Simulator
 
An automated voice bot that calls the PGAI test line (+1-805-439-8008), simulates realistic patient conversations, records and transcribes each call, and identifies bugs in the PGAI agent's behavior.

Loom Walkthrough:
https://www.loom.com/share/de5d7f7303934dc295f7e4aa7d182adf 

## Quick Start
 
### 1. Prerequisites
 
- Python 3.11+
- A **Twilio** account with a purchased US phone number (free trial credit would be enough but deposit must be made to remove opening disclaimer)
- An **OpenAI** API account with ~$10 credit
- **ngrok** installed: `brew install ngrok` or download from ngrok.com

### 2. Install
 
```bash
git clone <your-repo-url>
cd pgai-challenge
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure
 
```bash
cp .env.example .env
# Edit .env with your actual API keys
```

**Twilio trial setup:** Go to Console → Phone Numbers → Verified Caller IDs → add and verify your personal cell phone number. This is the number you'll submit in E.164 format (e.g. `+13105550000`).

### 4. Start ngrok (in a separate terminal)
 
```bash
ngrok http 5000
```

Copy the `https://xxxx.ngrok-free.app` URL into your `.env` as `PUBLIC_URL`.

**Terminal 1 — Start the bot server:**
```bash
python start.py
```

**Terminal 2 — Launch test calls:**
python run_calls.py

Individual scenarios are run by changing the index in SCENARIOS[:]

`transcripts/*.json` | Full call data including scenario, history, transcript

## Scenarios Tested
| 01 | Simple Appointment Scheduling | Baseline scheduling flow for a new patient |
| 02 | Weekend Appointment Attempt | Does the agent enforce weekend closure and offer alternatives? |
| 03 | Third-Party Scheduling | Does the agent handle a caller booking for someone else? |
| 04 | Spanglish Patient | Does the agent handle mixed English/Spanish input? |
| 05 | Pushy Patient | Does the agent hold firm on unavailable time slots under pressure? |
| 06 | Wrong Specialty | Does the agent correctly redirect a patient asking for dental services? |
| 07 | Rambling Patient | Can the agent extract relevant info from long, unfocused responses? |
| 08 | Cancel Phantom Appointment | How does the agent handle cancellation requests it can't fulfill? |
| 09 | Emergency / Severe Pain | Does the agent escalate appropriately or treat it as routine scheduling? |
| 10 | Medical Advice Request | Does the agent avoid diagnosing and redirect to an appointment?

## Cost Estimate
| Service | Estimated cost for 12 calls |
|---|---|
| Twilio (outbound calls + recording) | ~$15 |
| OpenAI GPT-4o (patient brain) | ~$1 |
| OpenAI TTS | covered by Twilio Polly |
| Total | **~$16** |

Cost was fairly high since I ran several test calls.
On a "perfect run" of all ten calls cost would be roughly $5.

## Environment Variables
See `.env.example` for all required and optional variables. Never commit your `.env` file.
