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

## Phase 1: Manual AI Content Generation

### Brand Foundations (/phase1/docs/)

- brand-style-guide-core-foundations.md  
  Logo, palette (obsidian #333333, titanium #FFFFFF, teal pulse #00A0FA), Vireo Sans, tone rules, pillars list, narrative.

- visual-identity-photography-guidelines.md  
  Isolation shots, floating device, no hands/people, ARRI cinematic specs, teal accent once per frame.

- campaign-content-templates.md  
  Phases (Teaser/Reveal/Deepen/Evergreen), social/video/ad templates, poetic brevity.

- usage-rules-restrictions.md  
  Logo usage, trademark, color/typography, imagery, tone/copy restrictions.

- target-audience-personas.md  
  Creative Professionals, Tech Minimalists, Early AI Adopters, shared psychographics.

### Daily Content Generation

Use the prompt in /prompts/daily-content-prompt.md  
Paste brand documents above it each session. Replace [CURRENT DATE].

### Sample Daily Package

/phase1/samples/2026-02-02-vireo-tech-package.md  
Contains complete example: blog, social, influencers, competitive summary, events, ads, emails.

## Phase 2: API Automation

Scripts to publish Phase 1 outputs.

### Folder Structure (/phase2/)

- hubspot/  
  - post_blog.py  
  - send_email.py  

- google-ads/  
  - create_ad_copy.py  

- social/  
  - linkedin_post.py  
  - twitter_post.py  
  - meta_ads.py  

- wordpress/  
  - publish_post.py  

- utils/  
  - brand_compliance_check.py  
  - content_formatter.py  

### Example Script: HubSpot Blog Post

phase2/hubspot/post_blog.py

```python
import requests
import json

HUBSPOT_API_KEY = "your-key"
HEADERS = {"Authorization": f"Bearer {HUBSPOT_API_KEY}", "Content-Type": "application/json"}

def publish_blog(title, body, meta_description):
    payload = {
        "name": title,
        "html_title": title,
        "body": body,
        "meta_description": meta_description,
        "publish_date": "now",
        "state": "PUBLISHED"
    }
    r = requests.post("https://api.hubapi.com/content/api/v4/pages/blog-posts", headers=HEADERS, json=payload)
    return r.json()

# Parse Phase 1 markdown → extract title/body/meta → call function
