# 💸 RemitAI — Diaspora Financial Advisor

> Smart remittance planning for Kenyans abroad. FX rates, M-Pesa transaction costs, provider comparison, and a conversational AI that helps you plan how much to send home — and when.

[![License: CC BY-NC-ND 4.0](https://img.shields.io/badge/License-CC%20BY--NC--ND%204.0-lightgrey.svg)](LICENSE)
[![Streamlit](https://img.shields.io/badge/Streamlit-Live-red)](https://remit-ai.streamlit.app)
[![Gemini](https://img.shields.io/badge/Gemini-Free%20tier-blue)](https://aistudio.google.com)

## The problem

Kenya receives $4.5B+ in annual remittances. The average Kenyan diaspora member sends money home 6–8 times a year. The questions they face every time:

- Which provider has the best rate today?
- How much arrives after all fees?
- Is this a good time to send — or should I wait?
- How do I split a send between family members?
- What's the cheapest way to reach someone in a rural county?

RemitAI answers all of these in one conversation.

## What it does

| Feature | Description |
|---------|-------------|
| 💱 **Live rate comparison** | Side-by-side true cost across 7 providers including the FX margin |
| 📊 **Arrival calculator** | Exactly how many KES arrives at the other end |
| 💬 **Conversational advisor** | Ask "Should I wait to send?" or "How do I send to Turkana County?" |
| 📱 **M-Pesa delivery guide** | Which provider lands directly into M-Pesa, which requires pickup |
| 🗓️ **Rate trend alerts** | When KES is at a 3-month high — best time to send |

## Quickstart

```bash
git clone https://github.com/gabrielmahia/remit-ai
cd remit-ai
pip install -r requirements.txt
streamlit run app.py
```

## Data sources

- Live FX rates via open exchange APIs
- Provider fee schedules (Western Union, Remitly, WorldRemit, Wise, M-Pesa Global, Azimo, Mukuru)
- World Bank remittance cost benchmark (5% threshold)

## Related

- [TumaPesa](https://tumapesa.streamlit.app) — True cost comparison dashboard (the calculator)
- **RemitAI** — the conversational advisor
- [mpesa-mcp](https://github.com/gabrielmahia/mpesa-mcp) — M-Pesa MCP server

## IP & Collaboration

© 2026 Gabriel Mahia · [contact@aikungfu.dev](mailto:contact@aikungfu.dev)
License: CC BY-NC-ND 4.0
Not affiliated with M-Pesa Africa, Safaricom, or any remittance provider.
