import os
import webbrowser
from urllib.parse import quote

from flask import Flask, flash, redirect, render_template, request, session, url_for
from agent import OpenRouterAgent

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))
DEFAULT_MODEL = "tencent/hy3-preview:free"

PROFILES = {
    "assistant": "You are a helpful assistant.",
    "coder": "You are a coding expert.",
    "agent": (
        "You are a local PC assistant. "
        "If the user asks you to perform an action on their computer, respond ONLY with a JSON object in this format:\n"
        "{\"action\":\"open_url\",\"value\":\"https://example.com\"}\n"
        "Available actions: open_url, search, run_command, open_file, create_file\n"
        "For create_file, value is {\"path\":\"file.txt\",\"content\":\"text\"}\n"
        "Do not include any other text in your response when performing an action."
    )
}

@app.route("/", methods=["GET"])
def index():
    history = session.get("history", [])
    api_key = session.get("api_key", "")
    profile = session.get("profile", "agent")
    return render_template("index.html", api_key=api_key, history=history, profile=profile, profiles=PROFILES)

@app.route("/set_key", methods=["POST"])
def set_key():
    api_key = request.form.get("api_key", "").strip()
    if not api_key:
        flash("Enter a valid OpenRouter API key.")
        return redirect(url_for("index"))

    session["api_key"] = api_key
    session["history"] = []
    flash("API key saved for this browser session.")
    return redirect(url_for("index"))

@app.route("/set_profile", methods=["POST"])
def set_profile():
    profile = request.form.get("profile", "agent")
    if profile in PROFILES:
        session["profile"] = profile
        session["history"] = []  # Reset history on profile change
        flash(f"Profile set to: {profile}")
    else:
        flash("Invalid profile")
    return redirect(url_for("index"))

@app.route("/clear", methods=["POST"])
def clear():
    session.pop("history", None)
    flash("Conversation history cleared.")
    return redirect(url_for("index"))

@app.route("/chat", methods=["POST"])
def chat():
    api_key = session.get("api_key", "")
    if not api_key:
        flash("Please set your OpenRouter API key first.")
        return redirect(url_for("index"))

    user_text = request.form.get("message", "").strip()
    if not user_text:
        flash("Enter a message or task for the agent.")
        return redirect(url_for("index"))

    history = session.get("history", [])
    history.append({"role": "user", "content": user_text})

    profile = session.get("profile", "agent")
    system_prompt = PROFILES[profile]

    messages = [{"role": "system", "content": system_prompt}] + history
    agent = OpenRouterAgent(api_key=api_key, model=DEFAULT_MODEL)

    print(f"Sending to model: {messages}")
    try:
        assistant_text = agent.chat(messages).strip()
        print(f"Assistant response: {assistant_text}")
    except Exception as exc:
        print(f"Error: {exc}")
        flash(f"OpenRouter error: {exc}")
        session["history"] = history
        return redirect(url_for("index"))

    action = agent.parse_action(assistant_text)
    if action:
        result = agent.execute_action(action)
        flash(result)
    else:
        flash("No action taken. AI response:")
        flash(assistant_text)

    history.append({"role": "assistant", "content": assistant_text})
    session["history"] = history
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
