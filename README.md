# ai-marketing-automation-setup

Tools and templates to build efficient, brand-consistent marketing automation using large language models (LLMs) and APIs.

**Purpose**  
Enable brands to generate high-quality, on-brand marketing content daily (Phase 1) and automate distribution to HubSpot, Google Ads, social platforms, WordPress, and more (Phase 2) — all while preserving strict brand voice, tone, and visual rules.

**Example Brand**  
This repository uses Vireo Tech (premium AI-native device / Nexus One) as a working case study. All documents and prompts are built from real outputs created for that brand in February 2026: minimalist design, instinct-driven AI, quiet confidence, pillars like "Intelligence isn't code. It's instinct." and "No apps. Just now."

**Two Phases**

- **Phase 1** — Manual content generation with strict brand alignment. Use LLMs (Grok, Claude, GPT, etc.) to produce blog posts, social, emails, etc. Review and post manually.
- **Phase 2** — API automation. Turn Phase 1 outputs into scheduled/ triggered posts, ads, emails, and blog articles.

## Prerequisites

- Access to an LLM with long context (Claude, Grok, GPT-4o, etc.)
- API keys / access tokens for:
  - HubSpot (Marketing Hub or CRM)
  - Google Ads
  - LinkedIn API (or third-party tools like Buffer/Ayrshare)
  - Meta Ads (Facebook/Instagram)
  - X / Twitter API v2
  - WordPress REST API (with authentication)
- Python 3.10+ or Node.js (for Phase 2 scripts)
- Basic command-line comfort

## Generating Brand Reference Documents

Most LLMs need reference files to stay on-brand. If you do not already have them:

1. Collect inputs
   - Website URL (or about page text if fictional/concept brand)
   - Logo image (PNG/SVG – describe or link)
   - Mission / narrative text
   - Desired tone keywords (e.g., quiet confidence, poetic brevity, second person)
   - Target audience description
   - Core pillars / taglines

2. Use the template prompts below with your LLM of choice.
   Paste your inputs at the top, then run each prompt one by one.

### Prompt Templates (copy each into your LLM)

**1. Brand Style Guide & Core Foundations**
