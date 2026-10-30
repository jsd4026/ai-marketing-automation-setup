# AI Music Video Pipeline – Setup and Operating Guide

**For AI Essentials Roundtable members.**  
Upload this file to your Claude Project or Grok chat. The AI will then have the full steps, modules, field values, gates, and rules needed to set up and run the pipeline.

**No API keys, logins, or personal details are included.** You add those yourself in the correct places.

---

## What this pipeline does

You describe one idea. The AI researches, writes lyrics, generates a song, creates stills of your character, produces lip-synced singing clips and story cutaways, then assembles a finished 9:16 music video. You approve at four gates. Most of the work happens while you are away.

**Two paths:**
- **Claude Code path** (runs on your Mac)
- **Grok Bot path** (uses a living lock file in Google Drive)

Both use the same tools and the same four gates.

---

## Accounts you need

| Service | Purpose | Plan |
|---------|---------|------|
| Claude (or Grok) | Brain that runs the process | Pro or Max |
| Make.com | Runs every paid API call | Core (not Free) |
| Google account + Drive | File handoff between tools | Free or Workspace |
| Google AI Studio | Stills and story video | Billing enabled (pay as you go) |
| OmniaKey | Song generation (Suno) | Pay-as-you-go credits |
| Hedra | Lip-sync video | Plan with API access + credits |

Fixed monthly cost is roughly $31 (AI plan + Make Core). Per-video cost depends on mode (see below).

**API key rules (critical):**
- Store every key in a password manager.
- Never paste a key into an AI chat, a shared document, or this guide.
- You paste keys only into Make.com modules (as Bearer tokens where required).

---

## Google Drive setup (both paths)

1. In My Drive (top level), create a folder called **AI_Video_Work**.
2. Inside it, create two subfolders: **Ready** and **Done**.
3. Install Google Drive for desktop, sign in with the same account, and make the folder available offline.
4. Write down the three folder IDs from the URLs (you will need them for Make).

Keep this folder only for the pipeline.

---

## Make.com connections and scenarios

Create these connections in Make.com:
- Google Drive (OAuth sign-in) — name it something clear
- Gemini AI (paste your AI Studio key)

The AI will build these scenarios for you. You then paste the remaining keys and turn them on.

**Scenarios to build (in order):**
1. **Song** — Watches the Ready folder, calls OmniaKey, uploads the song to Drive.
2. **Stills** — Generates opening and cutaway images using Gemini + your character reference image.
3. **Clips Omni** — Generates story cutaway video clips.
4. **Hedra Submit** — Sends chest-up stills + vocal-only audio for lip-sync.
5. **Hedra Collect** — Downloads finished lip-sync clips.

**Where you paste keys (human step only):**
- OmniaKey key → Song scenario, module that sets the auth variable (as Bearer).
- Hedra key → Hedra Submit and Hedra Collect scenarios, auth variable modules (as Bearer).

After pasting keys, turn all scenarios on and run a short test (one song + one still). Confirm the files land in your Drive folder.

---

## Claude Code path

1. Create a Claude Project. Upload this guide and any checklist.
2. Turn on connectors: Google Drive, Make.com, Web Search.
3. Open the chat in the Claude desktop app and link it to a folder on your computer that points to the synced AI_Video_Work folder.
4. Ask Claude to build the Make scenarios listed above.
5. Paste the two keys into Make, turn scenarios on, run the test.

---

## Grok Bot path (living lock file required)

**Do this first:**
1. In the AI_Video_Work folder, create exactly one file named **AI_Video_Pipeline_Lock.md**.
2. Give the Grok Bot persistent access to the folder.
3. Verify before any paid steps by pasting these two prompts:
   - “Read AI_Video_Pipeline_Lock.md and list the last three rules in it.”
   - “Add this note under a new ‘Test’ section: ‘Lock file is working on [today’s date].’ Update the same file and confirm by reading it back.”

**Rules the bot must follow:**
- Read the lock file at the start of every major step.
- When you give feedback that changes a process, update the **same file ID** immediately.
- Confirm every update by reading the file back.
- Never create a new dated or versioned copy. Archive manually if you want history.

The living lock file is what keeps the process consistent across runs and chats.

---

## Production modes and approximate cost

| Mode | What you get | Approx cost |
|------|--------------|-------------|
| A – Performance | Character sings every scene in sync. Little story around them. | ~$21 |
| B – Story | Rich action and camera moves. No lip-sync. | ~$42 |
| C – Intercut | Singing close-ups cut with wide story cutaways. | ~$55 |

---

## Your first video (both paths)

Confirm setup is complete (and, for Grok, that the lock file is readable and updatable). Then paste:

```
Read the Pipeline guide and checklist. Follow the steps in order, stopping at every approval gate. Mode: C. Topic: [your idea, tone, visual feel, any must-use lines].
```

**The four approval gates:**
1. Approve the lyrics and Big Idea.
2. Approve the scene plan and prompts.
3. Approve the stills (video spend starts after this).
4. Review the final video and the spend report.

There is also a song-approval gate before any visual work.

Typical run is 2–3 hours, mostly waiting on renders. The AI can keep working while you are away.

---

## Safety rules

- Never paste API keys into any AI chat.
- No video spend before Gate 3 is approved.
- Ask for a spend report at the end.
- Keep the AI_Video_Work folder dedicated to this pipeline.

---

*End of guide. Upload this file to your Claude Project or Grok chat so the AI has everything it needs to walk you through setup and your first video.*
