"""
Flask Web Server — Aria Mental Health Companion
Run: python app.py  → open http://localhost:5000
"""
from flask import Flask, request, jsonify, render_template
from agent.mental_health_agent import MentalHealthAgent
from agent.crisis_detector import detect_risk, RiskLevel
from agent.watsonx_client import RateLimitError, WatsonXError
from agent.mood_tracker import (
    log_mood, get_mood_history,
    add_journal_entry, get_journal_entries,
    generate_daily_report, log_crisis_event, get_crisis_log,
)

app = Flask(__name__)
agent = MentalHealthAgent()


# ── Pages ────────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ── Chat API ─────────────────────────────────────────────────────────────────

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip()
    if not user_message:
        return jsonify({"error": "Empty message"}), 400

    # Detect risk before sending to agent
    risk_level, keywords = detect_risk(user_message)

    # Log crisis event if detected
    if risk_level == RiskLevel.CRISIS:
        log_crisis_event(user_message, keywords)

    # Auto-log mood based on risk
    if risk_level == RiskLevel.CRISIS:
        log_mood("crisis", user_message[:80], risk_level="crisis")
    elif risk_level == RiskLevel.DISTRESS:
        log_mood("sad", user_message[:80], risk_level="distress")

    try:
        reply = agent.respond(user_message)
    except RateLimitError:
        reply = (
            "⚠️ The AI service is currently busy (rate limit reached on the free tier). "
            "Please wait 30–60 seconds and try again.\n\n"
            "If you are in crisis right now, please reach out immediately:\n"
            "• 988 Suicide & Crisis Lifeline (US): call or text **988**\n"
            "• Samaritans (UK): **116 123**\n"
            "• Crisis Text Line: text **HOME** to **741741**"
        )
    except WatsonXError as e:
        reply = (
            f"⚠️ Could not reach the AI service right now. Please check your internet connection and try again.\n"
            f"If this keeps happening, please contact support."
        )
    except Exception:
        reply = (
            "⚠️ Something went wrong on my end. Please try again in a moment.\n"
            "If you are in crisis, call **988** (US) or **116 123** (UK) immediately."
        )

    return jsonify({
        "reply": reply,
        "risk_level": risk_level.value,
        "keywords": keywords,
    })


@app.route("/new_session", methods=["POST"])
def new_session():
    agent.reset()
    return jsonify({"status": "ok"})


# ── Mood API ─────────────────────────────────────────────────────────────────

@app.route("/log_mood", methods=["POST"])
def api_log_mood():
    data = request.get_json()
    log_mood(
        mood=data.get("mood", "okay"),
        note=data.get("note", ""),
        risk_level="safe",
    )
    return jsonify({"status": "saved"})


@app.route("/mood_history")
def api_mood_history():
    return jsonify(get_mood_history(days=30))


# ── Journal API ──────────────────────────────────────────────────────────────

@app.route("/add_journal", methods=["POST"])
def api_add_journal():
    data = request.get_json()
    entry = add_journal_entry(
        title=data.get("title", "Untitled"),
        content=data.get("content", ""),
        mood=data.get("mood", "okay"),
    )
    return jsonify(entry)


@app.route("/journal_entries")
def api_journal_entries():
    return jsonify(get_journal_entries(limit=20))


# ── Reports API ──────────────────────────────────────────────────────────────

@app.route("/daily_report")
def api_daily_report():
    return jsonify(generate_daily_report())


# ── Crisis Log API ───────────────────────────────────────────────────────────

@app.route("/crisis_log")
def api_crisis_log():
    return jsonify(get_crisis_log(limit=50))


# ── Run ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n🌿 Aria Mental Health Companion is starting...")
    print("   Open your browser at: http://localhost:5000\n")
    app.run(debug=False, host="0.0.0.0", port=5000)
