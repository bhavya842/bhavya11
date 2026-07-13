# 🌿 Aria — Mental Health Awareness & Suicide Prevention Agent

An agentic AI powered by **IBM WatsonX AI** (Llama 3.3 70B) that provides compassionate, real-time mental health support and suicide prevention guidance.

---

## Features

| Feature | Description |
|---|---|
| 🧠 **Empathetic Conversation** | Multi-turn dialogue with memory, powered by Llama 3.3 70B |
| 🚨 **Crisis Detection** | Real-time keyword analysis for suicidal ideation and distress signals |
| 📞 **Crisis Resources** | Immediate hotlines for USA, UK, India, Australia, Canada, Germany |
| 🌬️ **Grounding Exercises** | Box breathing, 5-4-3-2-1 sensory grounding, safe-place visualisation |
| 💡 **Wellness Tips** | Evidence-based mental health tips |
| 🔄 **Agentic Loop** | Context-aware system prompts that adapt to the detected risk level |

---

## Project Structure

```
arirang/
├── main.py                        # CLI entry point
├── requirements.txt
└── agent/
    ├── __init__.py
    ├── watsonx_client.py          # IBM WatsonX AI + IAM auth
    ├── mental_health_agent.py     # Core agent logic & conversation loop
    ├── crisis_detector.py         # Risk level detection (SAFE / DISTRESS / CRISIS)
    └── resources.py               # Hotlines, tips, grounding exercises
```

---

## Quick Start

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the agent

```bash
python main.py
```

### 3. Interact

```
You: I've been feeling really overwhelmed lately
Aria: I hear you — feeling overwhelmed can be exhausting ...

You: /hotlines India
You: /breathe
You: /ground
You: /tip
You: /quit
```

---

## Architecture

```
User Input
    │
    ▼
┌─────────────────────────────────────┐
│         MentalHealthAgent           │
│                                     │
│  ┌──────────────────────────────┐   │
│  │  Crisis Detector             │   │
│  │  SAFE / DISTRESS / CRISIS    │   │
│  └──────────┬───────────────────┘   │
│             │ Risk Level            │
│             ▼                       │
│  ┌──────────────────────────────┐   │
│  │  System Prompt Builder       │   │
│  │  Base + Risk-specific rules  │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐   │
│  │  IBM WatsonX AI Client       │   │
│  │  IAM Token → Chat API        │   │
│  └──────────┬───────────────────┘   │
│             │                       │
│             ▼                       │
│  ┌──────────────────────────────┐   │
│  │  Response + Safety Footer    │   │
│  │  (hotlines appended on CRISIS│   │
│  └──────────────────────────────┘   │
└─────────────────────────────────────┘
    │
    ▼
Agent Response
```

---

## Risk Levels

| Level | Trigger | Agent Behaviour |
|---|---|---|
| `SAFE` | No risk keywords | Standard empathetic support |
| `DISTRESS` | Words like *hopeless*, *anxious*, *trapped* | Validation + gentle probing + grounding offer |
| `CRISIS` | Words like *suicide*, *end my life*, *kill myself* | Crisis protocol + mandatory hotlines appended |

---

## IBM WatsonX Configuration

| Parameter | Value |
|---|---|
| Endpoint | `https://eu-de.ml.cloud.ibm.com` |
| Model | `meta-llama/llama-3-3-70b-instruct` |
| Project ID | `688f364c-8a34-42d3-bcad-02e82595abc0` |
| Auth | IBM Cloud IAM API Key → Bearer Token |

---

## Commands

| Command | Action |
|---|---|
| `/help` | Show help |
| `/hotlines` | International crisis lines |
| `/hotlines USA` | Country-specific lines |
| `/breathe` | Box breathing exercise |
| `/ground` | 5-4-3-2-1 grounding technique |
| `/tip` | Random wellness tip |
| `/new` | Reset conversation |
| `/quit` | Exit |

---

## Disclaimer

> Aria is a supportive AI companion and is **not a substitute** for professional mental health care, licensed therapy, or emergency services. If you or someone you know is in immediate danger, call **911 (US)**, **999 (UK)**, **112 (EU)**, or your local emergency number immediately.
