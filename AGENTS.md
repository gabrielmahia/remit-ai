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

<!-- coverage-adaptive-reasoning:v2 -->

## Coverage-Adaptive Reasoning v2

For consequential research, recommendations, investigations, analogy searches, forecasting, opportunity discovery, and canon building:

- A correct ranking inside an incomplete universe is still a failed answer.
- Separate candidate generation from candidate ranking.
- Materiality-gate the search: use the minimum useful set of orthogonal retrieval routes that could change the answer.
- Before closure ask what correct answer the current search method would be structurally incapable of finding.
- Treat aliases, language/geography, era, source class, format, genealogy, taxonomy, legal identity vs operational control/economic benefit, intermediaries, schema categories, null/failure cases, and negative space as potential blind spots when material.
- Maintain leading + competing + null explanations.
- Distinguish answer confidence from coverage confidence.
- “Nothing found” is not evidence of absence when coverage is low.
- Stop when additional independent search routes no longer materially change the candidate universe, hypotheses, decision, or next test.
- When an important miss occurs, repair the retrieval architecture via MISS → SENSOR REDESIGN; do not merely append the missed example.

<!-- v2 section appended 2026-10-28 from https://github.com/gabrielmahia/nairobi-stack/blob/main/docs/COVERAGE_ADAPTIVE_REASONING.md; the rest of this file is unchanged. -->
