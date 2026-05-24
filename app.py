"""
RemitAI — Kenya Diaspora Services Assistant
Remittances, property, dual citizenship, diaspora financial planning.
"""
import json, urllib.request, ssl
import streamlit as st

st.set_page_config(
    page_title="RemitAI — Kenya Diaspora Services",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

def get_key():
    try:
        return st.secrets.get("GOOGLE_API_KEY") or st.secrets.get("GEMINI_API_KEY")
    except Exception:
        return None

def gemini(prompt: str, key: str) -> str:
    url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
    body = {"contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {"temperature": 0.3, "maxOutputTokens": 1200}}
    req = urllib.request.Request(f"{url}?key={key}",
        data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=20, context=ctx) as r:
        d = json.loads(r.read())
    return d["candidates"][0]["content"]["parts"][0]["text"]

with st.sidebar:
    st.image("https://flagcdn.com/w40/ke.png", width=40)
    st.title("RemitAI ✈️")
    st.caption("Kenya Diaspora Services")
    st.divider()
    mode = st.radio("Service", [
        "💸 Remittance Comparison",
        "🏠 Property Investment",
        "📋 Dual Citizenship Guide",
        "💰 Diaspora Financial Planning",
        "📱 eCitizen Remote Services",
        "💬 Ask RemitAI"
    ])

key = get_key()
if not key:
    st.warning("Add GOOGLE_API_KEY to Streamlit secrets.")

if mode == "💸 Remittance Comparison":
    st.title("💸 Remittance Comparison")
    st.markdown("*Find the cheapest way to send money to Kenya*")

    col1, col2 = st.columns(2)
    with col1:
        origin = st.selectbox("Sending from", [
            "United States (USD)", "United Kingdom (GBP)",
            "Canada (CAD)", "Germany (EUR)", "United Arab Emirates (AED)",
            "Qatar (QAR)", "Saudi Arabia (SAR)", "Australia (AUD)"
        ])
        amount = st.number_input("Amount to send", min_value=10, value=500, step=50)
        urgency = st.radio("Urgency", ["Within minutes", "Same day", "1-3 days"])
    with col2:
        recipient_method = st.selectbox("Recipient collects via", [
            "M-Pesa (phone)", "Bank transfer", "Cash pickup agent", "M-Pesa Global"
        ])
        frequency = st.selectbox("How often do you send?", [
            "One-time", "Weekly", "Monthly", "Bi-monthly"
        ])
        recipient_location = st.selectbox("Recipient in", [
            "Nairobi", "Mombasa", "Kisumu", "Rural area", "Eldoret", "Nakuru"
        ])

    if st.button("💸 Compare services", type="primary") and key:
        currency = origin.split("(")[1].rstrip(")")
        with st.spinner("Comparing remittance services..."):
            prompt = f"""You are RemitAI, a Kenya diaspora financial services expert.

Sender: {origin}, sending {currency} {amount}
Delivery: {recipient_method} in {recipient_location}
Urgency: {urgency}
Frequency: {frequency}

Compare these remittance services for this specific scenario:
1. Wise (TransferWise)
2. Remitly
3. Western Union
4. M-Pesa Global (Safaricom partnership)
5. WorldRemit
6. Local Kenyan bank wire (Kenya bank draft)

For each service provide:
- Estimated total cost (fee + exchange rate spread combined)
- Delivery time
- KES received for {currency} {amount}
- Pros and cons for THIS specific scenario
- Link or where to find current rates

Then: RECOMMENDATION — which 1-2 services are best for this person and why.

Note: Exchange rates fluctuate. Always verify current rates at point of transfer.
Add practical tips for {frequency} senders to reduce costs over time."""
            resp = gemini(prompt, key)
            st.markdown(resp)
            st.info("📌 Exchange rates change daily. Always verify at point of transfer.")

elif mode == "🏠 Property Investment":
    st.title("🏠 Kenya Property Investment Guide")
    st.markdown("*Navigate Kenya real estate as a diaspora investor*")

    col1, col2 = st.columns(2)
    with col1:
        country = st.selectbox("You are based in", ["UK","USA","Canada","UAE","Qatar","Australia","Germany"])
        budget = st.number_input("Budget (KES millions)", min_value=0.5, max_value=100.0, value=5.0, step=0.5)
        prop_type = st.selectbox("Property type", [
            "1/8 acre plot (residential)", "1/4 acre plot", "1 acre (agricultural)",
            "2-3 bedroom apartment", "3 bedroom maisonette",
            "Commercial property", "Agricultural land"
        ])
    with col2:
        location = st.selectbox("Target location", [
            "Nairobi (Westlands/Kilimani)", "Nairobi (Eastlands/Ruiru)",
            "Nairobi (Satellite towns: Kitengela/Thika)", "Mombasa",
            "Kisumu", "Eldoret", "Nakuru", "Rural upcountry"
        ])
        purpose = st.radio("Purpose", ["Own use (retirement home)", "Rental income", "Land banking (future development)"])

    if st.button("🏠 Get investment guide", type="primary") and key:
        with st.spinner("Generating property guide..."):
            prompt = f"""You are RemitAI, an expert on Kenya real estate for diaspora investors.

Investor profile: Based in {country}, budget KES {budget}M, seeking {prop_type} in {location} for {purpose}.

Provide:

**1. Market Reality** — Is KES {budget}M realistic for {prop_type} in {location}? Current price ranges.

**2. Legal Process for Diaspora**
- Can a non-resident Kenyan own property? (Constitution 2010 and Land Act provisions)
- Documents required from {country}
- Steps to verify title deed remotely (Ardhisasa portal)
- Recommended conveyancing lawyers (general guidance)
- Red flags to avoid (fraud common in this segment)

**3. Financing Options**
- KCB Diaspora Mortgage (current LTV, rates)
- NCBA diaspora home loan
- ABSA Kenya diaspora products
- Cash purchase process via diaspora remittance

**4. Tax Implications**
- Capital gains tax (Kenya)
- Rental income tax (Kenya, filing requirements as non-resident)
- Double taxation agreements between Kenya and {country}

**5. Remote Management**
- How to manage property/tenants from {country}
- Recommended property management companies
- Digital tools for diaspora landlords

**6. Estimated Timeline** — From decision to title deed transfer (realistic months)

Flag scam patterns common in this market segment."""
            resp = gemini(prompt, key)
            st.markdown(resp)

elif mode == "📋 Dual Citizenship Guide":
    st.title("📋 Kenya Dual Citizenship Guide")
    st.markdown("*Understand your rights under Kenya's 2010 Constitution*")

    col1, col2 = st.columns(2)
    with col1:
        scenario = st.selectbox("Your scenario", [
            "I naturalised in another country — do I still hold Kenyan citizenship?",
            "I was born in Kenya but grew up abroad — am I Kenyan?",
            "My children were born abroad — are they Kenyan citizens?",
            "I want to reaffirm / restore my Kenyan citizenship",
            "I want to apply for a Kenyan passport from abroad",
            "Can I own property in Kenya as a dual citizen?",
            "Can I vote in Kenya as a diaspora citizen?"
        ])
        other_country = st.selectbox("Other country of citizenship/residence", [
            "United States", "United Kingdom", "Canada", "Germany",
            "United Arab Emirates", "Australia", "Sweden", "Netherlands", "Other"
        ])
    with col2:
        if st.button("📋 Get citizenship guidance", type="primary") and key:
            with st.spinner("Retrieving citizenship guidance..."):
                prompt = f"""You are RemitAI, a Kenya diaspora legal services guide (not a lawyer).

Scenario: {scenario}
Other country: {other_country}

Provide specific guidance on:

**1. Legal Position**
Kenya's position under the Constitution 2010 (Chapter 3: Citizenship), specifically:
- Article 13 (rights of citizens)
- Article 14 (citizenship by birth)
- Article 15 (citizenship by registration)
- Kenya Citizenship and Immigration Act 2011

**2. Current Status**
For this specific scenario: what is their citizenship status?

**3. Steps Required**
Specific steps to confirm/restore/register citizenship from {other_country}:
- Documents needed
- Where to apply (Kenya High Commission / Embassy in {other_country})
- eCitizen portal processes available remotely
- Processing time and costs (government fees)

**4. Rights as Dual Citizen**
- Property ownership rights
- Voting rights (diaspora voting implemented partially since 2022)
- Travel rights (Kenyan passport vs other passport — which to use when)
- Business ownership rights

**5. Limitations**
- Positions barred to dual citizens (military, certain security roles)
- Any outstanding obligations

Note: This is general guidance only. For complex situations, consult an advocate at the Law Society of Kenya."""
                resp = gemini(prompt, key)
                st.markdown(resp)

elif mode == "💰 Diaspora Financial Planning":
    st.title("💰 Diaspora Financial Planning")
    st.markdown("*Build wealth across Kenya and your country of residence*")

    col1, col2 = st.columns(2)
    with col1:
        country_res = st.selectbox("Country of residence", ["USA","UK","Canada","UAE","Germany","Australia"])
        monthly_income = st.number_input("Monthly income (local currency equivalent, USD)", value=5000, step=500)
        monthly_remit = st.number_input("Current monthly remittance to Kenya (USD)", value=300, step=50)
        goal = st.selectbox("Primary financial goal", [
            "Build retirement home in Kenya",
            "Support family members monthly",
            "School fees (siblings/children in Kenya)",
            "Buy agricultural land as investment",
            "Start a business in Kenya",
            "Return to Kenya within 5 years"
        ])
    with col2:
        horizon = st.selectbox("Time horizon", ["1-2 years","3-5 years","5-10 years","10+ years"])
        existing = st.multiselect("Existing Kenya investments", [
            "SACCO membership","NSE/stocks","Land","Rental property",
            "Kenya government bonds","Money market fund (CIC/Sanlam)","None"
        ])

    if st.button("💰 Generate financial plan", type="primary") and key:
        with st.spinner("Building your plan..."):
            prompt = f"""You are RemitAI, a Kenya diaspora financial planning advisor (not a licensed financial advisor).

Profile: Living in {country_res}, monthly income USD {monthly_income}, currently sending USD {monthly_remit}/month.
Goal: {goal}
Horizon: {horizon}
Existing Kenya investments: {", ".join(existing) if existing else "None"}

Create a practical financial plan:

**1. Remittance Strategy**
- Is USD {monthly_remit} optimal for the goal?
- Best services for this amount and frequency (Wise vs Remitly vs M-Pesa Global)
- How to minimise fees over {horizon}

**2. Kenya Investment Roadmap**
Specific products in order of priority for the goal:
- Kenya government securities (Treasury Bills/Bonds via CBK DhowCSD portal)
- NSE stocks (safest sectors for diaspora)
- SACCOs accepting diaspora members (Stima, Kenya Police, etc.)
- Money market funds (CIC, Sanlam, Britam — remote investment options)

**3. Tax Efficiency**
- {country_res} tax implications of Kenya investments
- Kenya tax on investment income for non-residents
- Double taxation agreement between Kenya and {country_res}

**4. Milestone Plan**
Year-by-year targets for {horizon} with specific KES amounts.

**5. Risk Management**
- Currency risk (KES/USD volatility)
- Political risk hedging
- Estate planning for Kenya assets

This is general guidance. Consult a certified financial planner and tax advisor for personalised advice."""
            resp = gemini(prompt, key)
            st.markdown(resp)

elif mode == "📱 eCitizen Remote Services":
    st.title("📱 eCitizen Remote Services Guide")
    st.markdown("*Kenya government services accessible from abroad*")

    services = {
        "Passport renewal / new passport": {
            "portal": "ecitizen.go.ke → Immigration",
            "remote": True,
            "docs": "Current/expired passport scan, passport photos (biometric spec), KRA PIN, payment via card",
            "time": "6-8 weeks standard, 3 weeks express",
            "cost": "KES 4,550 (32-page) / KES 7,550 (48-page)",
            "tip": "Collect at Kenya High Commission in your country or designate a trusted agent in Kenya"
        },
        "KRA PIN registration / update": {
            "portal": "itax.kra.go.ke",
            "remote": True,
            "docs": "National ID or passport, email address",
            "time": "Instant",
            "cost": "Free",
            "tip": "Required for property purchase, SACCO membership, and formal employment"
        },
        "National ID (Huduma Namba)": {
            "portal": "ecitizen.go.ke → NIIMS",
            "remote": False,
            "docs": "Birth certificate, parents' IDs",
            "time": "2-4 weeks after biometric capture",
            "cost": "Free",
            "tip": "Must be done in Kenya — biometric capture required in person"
        },
        "Business registration": {
            "portal": "ecitizen.go.ke → Business Registration Service",
            "remote": True,
            "docs": "Proposed name, directors' IDs, Memorandum of Association",
            "time": "3-5 days",
            "cost": "KES 10,650 (private limited company)",
            "tip": "Can appoint a local director or secretary; documents can be signed electronically"
        },
        "Land search (Ardhisasa)": {
            "portal": "ardhisasa.go.ke",
            "remote": True,
            "docs": "Title deed number or parcel number",
            "time": "Instant to 24 hours",
            "cost": "KES 500 per search",
            "tip": "Always do a search before any property purchase — verify ownership and encumbrances"
        },
        "NSSF registration": {
            "portal": "etims.nssf.go.ke",
            "remote": True,
            "docs": "National ID, email, phone",
            "time": "Instant",
            "cost": "Free",
            "tip": "Voluntary members can contribute from abroad via M-Pesa or bank transfer"
        },
    }

    selected = st.selectbox("Select service", list(services.keys()))
    svc = services[selected]

    col1, col2 = st.columns(2)
    with col1:
        availability = "✅ Can be done remotely" if svc["remote"] else "⚠️ Physical presence required"
        st.markdown(f"**{availability}**")
        st.markdown(f"**Portal:** [{svc['portal']}](https://ecitizen.go.ke)")
        st.markdown(f"**Documents needed:**
{svc['docs']}")
    with col2:
        st.markdown(f"**Processing time:** {svc['time']}")
        st.markdown(f"**Cost:** {svc['cost']}")
        st.info(f"💡 **Diaspora tip:** {svc['tip']}")

    if key and st.button("Get detailed step-by-step guide"):
        with st.spinner("Generating guide..."):
            prompt = f"""You are RemitAI, guiding a Kenyan in the diaspora through {selected}.

Service details:
- Portal: {svc['portal']}
- Can be done remotely: {svc['remote']}
- Required documents: {svc['docs']}
- Cost: {svc['cost']}
- Tip: {svc['tip']}

Provide a detailed step-by-step guide:
1. Pre-requirements (what to prepare before starting)
2. Step-by-step application process (specific screen-by-screen where relevant)
3. Payment process (card payment from abroad, M-Pesa Global if applicable)
4. What happens after submission (tracking, collection)
5. Common problems and how to resolve them
6. Contact for help: eCitizen helpdesk details

Keep it practical and specific to someone applying from outside Kenya."""
            resp = gemini(prompt, key)
            st.markdown(resp)

else:
    st.title("💬 Ask RemitAI")
    if "remit_chat" not in st.session_state:
        st.session_state.remit_chat = []
    for msg in st.session_state.remit_chat:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
    user_q = st.chat_input("Ask about diaspora services, remittances, property, citizenship...")
    if user_q and key:
        st.session_state.remit_chat.append({"role":"user","content":user_q})
        with st.chat_message("user"):
            st.markdown(user_q)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                history = "\n".join(f"{m['role']}: {m['content']}" for m in st.session_state.remit_chat[-6:])
                prompt = f"""You are RemitAI, a Kenya diaspora services expert. You specialise in remittances, Kenya property law, dual citizenship (Constitution 2010), eCitizen services, diaspora financial planning, and SACCO/investment products.

{history}

Respond practically. Use KES amounts and Kenya government references. Note when professional legal/financial advice is needed."""
                try:
                    resp = gemini(prompt, key)
                    st.markdown(resp)
                    st.session_state.remit_chat.append({"role":"assistant","content":resp})
                except Exception as e:
                    st.error(f"AI error: {e}")

st.divider()
st.caption("RemitAI © 2026 | [East African Decision Infrastructure](https://gabrielmahia.github.io) | contact@aikungfu.dev")
st.caption("⚠️ Financial and legal information only. Not professional advice. Always verify with qualified professionals.")
