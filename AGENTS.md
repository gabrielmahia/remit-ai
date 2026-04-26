# AGENTS.md — RemitAI

## Purpose
Smart remittance advisor for Kenyans abroad. Provider comparison, FX calculator,
and conversational AI for planning how much to send home — and when.

## Architecture
- `app.py` — Streamlit single-file app
- Gemini REST API (no SDK) — falls back across gemini-2.0-flash → 1.5-flash → 1.5-flash-8b
- Provider rates are static reference data (not live — direct users to provider sites)

## AI Behaviour Rules
- NOT a licensed financial advisor — always state this
- Provider rates are illustrative — always direct users to verify on official sites
- World Bank 5% total cost benchmark should be mentioned when relevant
- Gemini key required only for chat tab; calculator works without it
- Never recommend a specific provider without noting rate volatility

## Provider Data
Wise, Remitly, WorldRemit, Western Union, Mukuru, M-Pesa Global
Fee structures current as of early 2026 — verify before publishing

## Expansion ideas
- Live FX via open.er-api.com (free tier)
- Africa's Talking SMS alerts when KES rate hits threshold
