import os
import webbrowser
from urllib.parse import quote

from flask import Flask, flash, redirect, render_template, request, session, url_for
from agent import OpenRouterAgent

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", os.urandom(24))
DEFAULT_MODEL = "gpt-4o-mini"

SYSTEM_PROMPT = (
    "You are a local PC assistant. "
    "When you want to perform a local action, respond with a JSON object only in the exact format:\n"
    "{\"action\":\"open_url\",\"value\":\"https://example.com\"}\n"
    "or\n"
    "{\"action\":\"search\",\"value\":\"best coffee shops near me\"}\n"
    "Do not include any extra text outside the JSON object. "
    "If no action is required, answer as normal text."
)

@app.route("/", methods=["GET"])
def index():
    history = session.get("history", [])
    api_key = session.get("api_key", "")
    return render_template("index.html", api_key=api_key, history=history)

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

    messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history
    agent = OpenRouterAgent(api_key=api_key, model=DEFAULT_MODEL)

    try:
        assistant_text = agent.chat(messages).strip()
    except Exception as exc:
        flash(f"OpenRouter error: {exc}")
        session["history"] = history
        return redirect(url_for("index"))

    action = agent.parse_action(assistant_text)
    if action:
        if action["action"] == "open_url":
            webbrowser.open(action["value"], new=2)
            flash(f"Opened URL: {action['value']}")
        elif action["action"] == "search":
            search_url = f"https://www.google.com/search?q={quote(action['value'])}"
            webbrowser.open(search_url, new=2)
            flash(f"Opened search for: {action['value']}")
        else:
            flash(f"Unsupported action: {action['action']}")

    history.append({"role": "assistant", "content": assistant_text})
    session["history"] = history
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
