"""RemitAI — Diaspora financial advisor for Kenyans abroad."""
import sys, os, json, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import streamlit as st

st.set_page_config(page_title="RemitAI", page_icon="💸", layout="centered")

def _get_key():
    try:
        k = st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
        if k: return k
    except: pass
    return os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY", "")

def _call_gemini(system, user, api_key):
    _BASE = "https://generativelanguage.googleapis.com"
    models = ["gemini-2.0-flash", "gemini-1.5-flash", "gemini-1.5-flash-8b"]
    payload = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"maxOutputTokens": 800, "temperature": 0.3},
    }
    for model in models:
        url = f"{_BASE}/v1beta/models/{model}:generateContent?key={api_key}"
        req = urllib.request.Request(url, data=json.dumps(payload).encode(),
              headers={"Content-Type": "application/json"}, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                data = json.loads(r.read())
            return data["candidates"][0]["content"]["parts"][0]["text"]
        except urllib.error.HTTPError as e:
            if e.code in (400, 404): continue
            raise
        except Exception: continue
    raise RuntimeError("Gemini unavailable")

PROVIDERS = {
    "Wise":         {"fee_pct": 0.45, "fx_margin": 0.0, "delivery": "M-Pesa / Bank", "time": "Same day"},
    "Remitly":      {"fee_pct": 0.00, "fx_margin": 2.1, "delivery": "M-Pesa", "time": "Minutes"},
    "WorldRemit":   {"fee_pct": 0.00, "fx_margin": 1.8, "delivery": "M-Pesa / Cash", "time": "Minutes"},
    "Western Union":{"fee_pct": 2.50, "fx_margin": 3.5, "delivery": "Cash / M-Pesa", "time": "Minutes"},
    "Mukuru":       {"fee_pct": 1.20, "fx_margin": 1.2, "delivery": "Cash / M-Pesa", "time": "Minutes"},
    "M-Pesa Global":{"fee_pct": 0.00, "fx_margin": 2.5, "delivery": "M-Pesa direct", "time": "Instant"},
}

SYSTEM = """You are RemitAI, a financial advisor for Kenyans sending money home from abroad.
You know the Kenya remittance market deeply: M-Pesa, Safaricom rates, MPGS, provider fee structures,
KES exchange rate trends, and how to reach family in rural counties.

Be concise, practical, and specific. Give KES amounts. When asked about timing, note that KES
is typically stronger in months with high diaspora flows (Dec, Aug). Recommend Wise or Remitly
for best true cost. Note M-Pesa Global for instant M-Pesa delivery.

You are not a licensed financial advisor. Always note this when giving specific recommendations."""

st.title("💸 RemitAI")
st.caption("Smart remittance planning for Kenyans abroad · Free · Powered by Gemini")

# Quick calculator
st.subheader("Quick Calculator")
col1, col2, col3 = st.columns(3)
with col1:
    currency = st.selectbox("From:", ["USD", "GBP", "EUR", "CAD", "AUD", "AED"])
with col2:
    amount = st.number_input("Amount:", min_value=10, value=200, step=50)
with col3:
    kes_rate = st.number_input("KES rate:", min_value=100, value=129, step=1)

if st.button("Compare providers", use_container_width=True):
    results = []
    for name, p in PROVIDERS.items():
        fee_amt  = amount * (p["fee_pct"] / 100)
        net_send = amount - fee_amt
        fx       = kes_rate * (1 - p["fx_margin"] / 100)
        arrives  = round(net_send * fx)
        results.append({"Provider": name, "Arrives (KES)": f"{arrives:,}",
                        "Delivery": p["delivery"], "Time": p["time"],
                        "True rate": f"{fx:.1f}"})
    import pandas as pd
    df = pd.DataFrame(results).sort_values("Arrives (KES)", ascending=False)
    st.dataframe(df, hide_index=True, use_container_width=True)
    best = results[0]["Provider"] if results else "Wise"
    st.caption(f"⚠️ Illustrative rates — verify on provider websites. World Bank benchmark: max 5% total cost.")

st.divider()

# AI advisor
st.subheader("Ask RemitAI")
api_key = _get_key()
if not api_key:
    with st.expander("Add a free Google AI key to chat with RemitAI"):
        api_key = st.text_input("Google AI key:", type="password",
                                 help="Free at aistudio.google.com — no credit card.")

if "remit_msgs" not in st.session_state:
    st.session_state.remit_msgs = []

EXAMPLES = [
    "Which provider is best for sending £300 to Kisumu?",
    "My family is in Turkana County — how do they receive M-Pesa?",
    "Is now a good time to send or should I wait for a better KES rate?",
    "How do I split a send between 3 family members?",
]
st.caption("**Try:** " + " · ".join(f"*{e}*" for e in EXAMPLES[:2]))

for role, msg in st.session_state.remit_msgs[-6:]:
    with st.chat_message(role):
        st.markdown(msg)

user_input = st.chat_input("Ask about sending money home...")
if user_input:
    st.session_state.remit_msgs.append(("user", user_input))
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        if not api_key:
            answer = "Add a free Google AI key above to get personalised advice."
        else:
            with st.spinner("Thinking..."):
                try:
                    context = f"[User currency: {currency}, typical send: {currency} {amount}, KES rate: {kes_rate}]"
                    answer = _call_gemini(SYSTEM, f"{context}\n\n{user_input}", api_key)
                except urllib.error.HTTPError as e:
                    answer = "API key not recognised." if e.code == 403 else "Too many requests — please wait."
                except Exception:
                    answer = "Something went wrong. Please try again."
        st.markdown(answer)
    st.session_state.remit_msgs.append(("assistant", answer))

st.divider()
st.caption("© 2026 Gabriel Mahia · CC BY-NC-ND 4.0 · Not financial advice · contact@aikungfu.dev")
