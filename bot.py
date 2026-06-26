from flask import Flask, request, Response, jsonify
from openai import OpenAI
from pathlib import Path
from twilio.rest import Client
from scenarios import SCENARIOS
import os
import json
import datetime
import uuid

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
active_calls = {}
openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
NGROK_URL = os.getenv('NGROK_URL')

twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# def get_patient_reply(conversation_history, scenario) — GPT-4o logic
def get_patient_reply(conversation_history, scenario):
    system_prompt = f"""IMPORTANT: You are ONLY a patient. You are NOT a doctor, receptionist, or office staff of any kind.
    You are {scenario['persona'].split(',')[0]}, a patient who called a medical office.
    THEY answered YOUR call. You need THEIR help.

    Persona: {scenario['persona']}
    Goal: {scenario['goal']}

    Rules:
    - You called them. You need help. You are the one seeking assistance.
    - Never say "how can I help you" or "thank you for calling" — that's what THEY say.
    - If you catch yourself acting like staff, immediately correct back to being a patient.
    - Short responses only, 1-2 sentences.
    - React to what the agent says as a real patient would.
    """
    response = openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": system_prompt}] + conversation_history,
        max_tokens=100,
        temperature=0.8,
    )

    return response.choices[0].message.content.strip()

@app.route("/launch", methods=["POST"])
def launch():
    data = request.get_json()
    scenario_id = data["scenario_id"]

    scenario = next(s for s in SCENARIOS if s["id"] == scenario_id)
    
    call_id = str(uuid.uuid4()) # uuid4() does not rely on the MAC address or timestamps, more suitable for privacy-sensitive applications
    active_calls[call_id] = {
        "scenario": scenario,
        "history": [],
        "transcript": []
    }

    call = twilio_client.calls.create(
        to=os.getenv('TARGET_NUMBER'),
        from_=os.getenv('TWILIO_FROM_NUMBER'),
        url=f"{NGROK_URL}/incoming/{call_id}",
        status_callback=f"{NGROK_URL}/status/{call_id}",
        status_callback_event=["completed"],
        record=True
    )
    return jsonify({"call_id": call_id})


@app.route("/incoming/<call_id>", methods=["POST"])
def incoming(call_id):
    # clear prior convo
    active_calls[call_id]["history"] = []
    active_calls[call_id]["transcript"] = []
    scenario = active_calls[call_id]["scenario"]
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather input="speech" action="{NGROK_URL}/gather/{call_id}" method="POST" timeout="10" speechTimeout="3">
        </Gather>
    </Response>"""
    return Response(twiml, mimetype="text/xml")


@app.route("/gather/<call_id>", methods=["POST"])
def gather(call_id):
    if call_id not in active_calls:
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
        <Response><Hangup/></Response>"""
        return Response(twiml, mimetype="text/xml")
    
    agent_said = request.form.get("SpeechResult", "")

    scenario = active_calls[call_id]["scenario"]
    history = active_calls[call_id]["history"]

    # Add agent reply to history
    active_calls[call_id]["history"].append({
        "role": "user",
        "content": agent_said
    })
    active_calls[call_id]["transcript"].append({
        "speaker": "AGENT", 
        "text": agent_said})

    patient_reply = get_patient_reply(history, scenario)

    # Add patient reply to history
    active_calls[call_id]["history"].append({
        "role": "assistant",
        "content": patient_reply
    })
    active_calls[call_id]["transcript"].append({
        "speaker": "PATIENT", 
        "text": patient_reply})
    
    patient_reply = get_patient_reply(history, scenario)
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Gather input="speech" action="{NGROK_URL}/gather/{call_id}" method="POST" timeout="10" speechTimeout="2">
            <Say voice="Polly.Stephen-Neural">{patient_reply}</Say>
        </Gather>
    </Response>"""

    return Response(twiml, mimetype="text/xml")

@app.route("/status/<call_id>", methods=["POST"])
def status(call_id):
    call_status = request.form.get("CallStatus")
    print(f"[{call_id}] Call ended with status: {call_status}")
    if call_id in active_calls:
        save_transcript(call_id)
    return ("", 204)



def save_transcript(call_id):
    call_data = active_calls[call_id]
    scenario_id = call_data["scenario"]["id"]
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"transcripts/{scenario_id}_{timestamp}.json"

    Path("transcripts").mkdir(exist_ok=True)
    with open(filename, "w") as f:
        json.dump(call_data, f, indent=2)




if __name__ == "__main__":
    app.run(port=5000, debug=True)