# AI Music Video Engine: Setup and First Video (Claude Code edition)

**Version:** 1.0, 2026-10-29. **Source:** Tableland Partners' AI Video Content Engine (guide v7.1), the system that produced "Trust Me (Mon Chéri)" and "Go Touch Something Real".
**Who this is for:** an AI Essentials Roundtable member setting the system up in their own accounts, run from **Claude Code** on a Mac.
**What you get:** a vertical 9:16, 1080p music video in your Google Drive. It has an original song, a consistent character who lip-syncs the vocals, story cutaways, animated on-screen text, and an end card. You give Claude the idea and approve 4 checkpoints. Claude does the rest.

---

## 0. How to use this document

**For the human (you):** read sections 1–3 before you start. The setup takes about 2 hours, once. Steps marked **👤 YOU** need your logins, payment details or API keys, so only you can do them. Steps marked **🤖 CLAUDE** are done by Claude Code.

**For Claude Code (the operator):** this file is your only source of truth. Nobody from Tableland is available to answer questions.
1. Save this file as `ENGINE_GUIDE.md` in the project folder (section 4.3), and keep it updated when something changes.
2. Work through the sections in this order: **4 → 5 → 6.1–6.2 (human steps) → 7 (connect Make) → the 🤖 part of 6.2 → 6.3–6.7 → 8 → 9**. Don't skip a verification step. Each one exists because that step failed once before.
3. **Never ask the user to paste an API key into the chat, and never write a key into any file, request JSON, log or this guide.** Keys are typed by the human straight into Make (section 6.5).
4. **Never call OmniaKey, Gemini or Hedra directly**, even though Claude Code could reach them. Every paid API call goes through the Make scenarios, so there's one place to see costs, logs and keys.
5. Stop at every ⛔ GATE and wait for the user's explicit approval. **No video spend (Omni or Hedra) before Gate 3 is approved.**
6. When a step fails, check section 11 (Troubleshooting) before inventing a fix. Then add what you learned to section 11.

### 0.1 The system on one page

```
YOU: idea ──► CLAUDE CODE (your Mac): research, lyrics, timing, scene plan, prompts, QA, assembly (ffmpeg)
                 │  writes request files into the synced Drive folder and calls Make through the Make MCP server
                 ▼
             MAKE.COM (5 scenarios): the only thing that calls the paid APIs
                 1 Song ........ OmniaKey (Suno v4.5) ──► Song.mp3
                 2 Stills ...... Gemini image model + your character's reference image ──► opening and cutaway stills
                 3 Clips Omni .. Gemini Omni video ──► story cutaway clips
                 4 Hedra Submit / 5 Hedra Collect .. Hedra Character-3 lip-sync ──► singing clips
                 ▼
             GOOGLE DRIVE folder "Claude AI Video Videos" (synced to your Mac by Google Drive for desktop)
                 ▼
CLAUDE CODE: assemble.py (cuts every scene to the song clock) ► kinetic.py (animated text) ► final MP4
```

**Production mode used in this guide: Mode C, "Intercut".** Each scene opens with the character singing (Hedra lip-sync), cuts to a story cutaway from a different camera angle (Omni), and goes back to the singing. This is the mode that made both reference videos. Mode A (Hedra only) is cheaper. Mode B (Omni only) has no lip-sync.

---

## 1. Plans and accounts (👤 YOU)

| # | Service | What it does here | Plan to buy | Why this plan | Cost (Oct 2026) |
|---|---|---|---|---|---|
| 1 | **Claude** (claude.ai) | Claude Code is the operator | **Pro** works. **Max** is recommended for full videos | A full video is a long session with many tool calls. Pro can hit usage limits partway through | Pro $20/mo, Max from $100/mo |
| 2 | **Make.com** | Runs every API call | **Core** (or higher). **Not Free** | Free allows 2 active scenarios, 5-min runs and 5 MB files, and it pauses when you hit its limits. The Song run alone takes up to 5 min, and clips are bigger than 5 MB | Core $10.59/mo ($9/mo billed yearly), 10,000 credits |
| 3 | **Google account + Google Drive** | All files, shared between Make and your Mac | Free 15 GB is enough for a first video. Google One 100 GB for regular use | One video's working files (clips, stills, drafts) come to about 1–3 GB | Free, or about $2/mo |
| 4 | **Google AI Studio (Gemini API)** | Stills (image model) and story clips (Gemini Omni video) | **Paid tier** (turn billing on) | The image and video models need a billed key. Free-tier keys get refused or rate-limited | Pay as you go: about $0.15–0.25 per 2K still, about $1 per Omni clip |
| 5 | **OmniaKey** (omniakey.com) | Song generation through Suno v4.5 | Pay-as-you-go credits | Gives API access to Suno. Suno has no public API | A $10–20 top-up covers several songs |
| 6 | **Hedra** (hedra.com) | Lip-sync video (Character-3) | A plan **that includes API access** (Starter or higher). Then buy credits | Free plans have no API key | Our 1080p run: about $13 for 32 clips (a 3:22 song) |

**Total cost per 3–4 min video, Mode C:** about **$30–45** (Gemini stills + Omni about $15–25, Hedra about $12–15, song under $2, Make credits covered by Core). **A 60–90 s first test** (section 9 recommends this) costs about **$10–15**.

**Computer:** a Mac (macOS 13 or newer) with about 20 GB free. Section 5.3 reads Drive file IDs with a macOS-only method. On Windows, see section 11, row "No Drive ID on Windows".

---

## 2. Get your API keys (👤 YOU; do these as you reach section 6.5)

Store each key in a password manager. **Never paste a key into Claude, a chat, a file in the project folder, or a Drive file.** You'll paste each key exactly once, into Make.

| Key | Where to get it | What it looks like | Where it goes (section 6.5) |
|---|---|---|---|
| **Gemini API key** | aistudio.google.com → **Get API key** → **Create API key** (in a Google Cloud project). Then **Set up billing** on that project | starts `AIza…` | Make → Connections → **Gemini AI** connection |
| **OmniaKey key** | omniakey.com → sign up → Dashboard → **Billing** (add $10–20) → **API Keys** → **Create** | starts `sk-…` | Make → Song scenario → module **20** (Set variable `omnia_auth`) as `Bearer <key>` |
| **Hedra key** | hedra.com → sign in → choose a plan with API access → profile menu → **API** (API Profile page) → **Create API key**. Buy credits on the same page | a long key string | Make → Hedra Submit module **1** and Hedra Collect module **1** (Set variable `hedra_auth`) as `Bearer <key>` |
| **Google Drive** | No key. You sign in with OAuth inside Make | n/a | Make → Connections → **Google Drive** |
| **Make (for Claude Code)** | No key. OAuth when you run `/mcp` (section 7) | n/a | Claude Code MCP |

---

## 3. What Claude Code needs on your Mac (overview)

- **Google Drive for desktop**, signed in to the same Google account Make uses. Claude reads and writes files in the synced folder, and Make sees them in Drive.
- **Homebrew, ffmpeg (with libass), Python 3.10+** and a few Python packages: numpy, pillow, librosa, opencv-python-headless, audio-separator.
- **Three fonts:** Anton, Oswald Bold, Pacifico.
- **The kit folder:** this guide, the 9 scripts in Appendix B, and the 5 blueprints in Appendix A.
- **The Make MCP server** connected to Claude Code.

---

## 4. Computer setup (🤖 CLAUDE runs the commands; 👤 YOU approve installs)

### 4.1 Install tools
**👤 YOU, in Terminal** (the Homebrew installer asks for your Mac password and a RETURN key press, so Claude Code can't run it):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"   # skip if `brew -v` works
echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile && eval "$(/opt/homebrew/bin/brew shellenv)"   # Apple Silicon; on Intel Macs brew is already in /usr/local/bin
```
**🤖 CLAUDE** (or you):
```bash
brew install ffmpeg python@3.12 node
python3.12 -m venv ~/vera-venv
~/vera-venv/bin/pip install --upgrade pip
~/vera-venv/bin/pip install numpy pillow librosa "opencv-python-headless<5" "audio-separator[cpu]" audioread
echo 'export PATH="$HOME/vera-venv/bin:$PATH"' >> ~/.zshrc
```
The venv is the only Python this engine uses: Homebrew's Python refuses global `pip install`, and macOS's own Python is too old. Because `~/vera-venv/bin` is first on PATH, `python3` and `audio-separator` in every later command mean the venv versions. **Open a new Terminal window (and restart `claude`) after this step** so the PATH change applies.

### 4.2 Verify (in a new shell; all must pass)
```bash
which python3            # must print /Users/<you>/vera-venv/bin/python3
ffmpeg -hide_banner -filters | grep -E " ass |subtitles"   # must list "ass" (libass). If missing: brew reinstall ffmpeg
python3 -c "import numpy, PIL, librosa, cv2; print('py ok', cv2.__version__); print(hasattr(cv2,'CascadeClassifier'))"   # must print True
audio-separator --version
```

### 4.3 Project folder (the kit)
```bash
mkdir -p ~/VeraEngine/{scripts/fonts,blueprints,runs,models}
```
- Save this guide as `~/VeraEngine/ENGINE_GUIDE.md`.
- **🤖 CLAUDE:** write every file in **Appendix B** to `~/VeraEngine/scripts/<name>` exactly as printed (copy the code blocks byte for byte, with no "improvements"). Write every blueprint in **Appendix A** to `~/VeraEngine/blueprints/<name>`.
- Create `~/VeraEngine/CLAUDE.md` with the text in section 7.3, so every Claude Code session in this folder loads the operator rules.

### 4.4 Fonts
```bash
cd /tmp && npm pack @expo-google-fonts/anton @expo-google-fonts/oswald @expo-google-fonts/pacifico
for f in expo-google-fonts-*.tgz; do tar -xzf "$f"; done
find package* -name "Anton_400Regular.ttf" -o -name "Oswald_700Bold.ttf" -o -name "Pacifico_400Regular.ttf" | xargs -I{} cp {} ~/VeraEngine/scripts/fonts/
ls ~/VeraEngine/scripts/fonts    # must show exactly: Anton_400Regular.ttf  Oswald_700Bold.ttf  Pacifico_400Regular.ttf
```
If `npm pack` unpacks into the same `package/` folder each time, unpack them one at a time (`tar -xzf <file> && find package -name "*.ttf" …` per font). kinetic.py looks for these fonts by family name ("Anton", "Oswald", "Pacifico") in `scripts/fonts/`.

---

## 5. Google Drive (👤 YOU, then 🤖 CLAUDE verifies)

### 5.1 Folders
In **My Drive** (top level, not inside a shared drive or a shortcut), create:
```
Claude AI Video Videos/          ← every output: songs, stills, clips, finals
    Ready/                   ← song request files (the Song scenario watches this folder)
    Done/                    ← run logs (song logs, Hedra job files, Hedra cost logs)
```
**Keep this folder for this engine only.** Other tools or agents writing here will confuse the scenarios.

Write down 3 folder IDs. Open each folder in drive.google.com: the ID is the last part of the URL, `https://drive.google.com/drive/folders/<THIS_PART>`.
- `VIDEOS_FOLDER_ID` = Claude AI Video Videos
- `READY_FOLDER_ID` = Ready
- `DONE_FOLDER_ID` = Done

### 5.2 Google Drive for desktop
1. Install it from google.com/drive/download and sign in with the **same Google account** you'll connect to Make.
2. Settings (gear) → Preferences → Google Drive: either choice works. **Mirror files** is the more reliable one. With **Stream files**, right-click `Claude AI Video Videos` in Finder → **Available offline**, so files aren't cloud-only when Claude reads them.
3. The folder appears at `~/Library/CloudStorage/GoogleDrive-<you@gmail.com>/My Drive/Claude AI Video Videos`. **🤖 CLAUDE:** find the exact name and make `$VV` a permanent shell variable (every later command uses it):
```bash
ls ~/Library/CloudStorage                      # shows e.g. GoogleDrive-you@gmail.com
echo 'export VV="$HOME/Library/CloudStorage/GoogleDrive-<you@gmail.com>/My Drive/Claude AI Video Videos"' >> ~/.zshrc
zsh -ic 'ls "$VV"'                             # must list Ready and Done
```
   Also write the path into CLAUDE.md (section 7.3). If a command ever shows paths like `/Ready/...`, `$VV` is empty in that shell: run `source ~/.zshrc` or use the full path.
4. **Give Claude Code access:** macOS System Settings → Privacy & Security → **Full Disk Access** (or Files and Folders) → enable your terminal app (Terminal, iTerm or the Claude desktop app). Without this, reads in `~/Library/CloudStorage` fail with "Operation not permitted".

### 5.3 Drive file IDs (how Claude finds a file's ID)
Make addresses files by Drive ID. Drive for desktop stores each file's ID as a macOS extended attribute once the upload finishes. `scripts/drive_id.py` reads it:
```bash
python3 ~/VeraEngine/scripts/drive_id.py "$VV/some file.jpg"      # prints: <ID>  some file.jpg
```
**Verify now:** put any small file in `$VV`, wait 10–20 s, and run the command. Then compare the ID with the file's link in drive.google.com (Share → Copy link: `/file/d/<ID>/`). They must match. A brand-new file shows `MISSING` until it has uploaded; the script waits up to 120 s.

### 5.4 Your character's hero reference image
The whole look depends on **one reference image** of your character. Every still is generated with it attached.
1. Create it in the Gemini app or AI Studio (image model). Use the lock text in section 10.1 with your own details, or bring your own artwork or photo **that you have the rights to**. Make it a clear, front-facing, chest-up portrait, 9:16, in even light.
2. Save it as `Hero.jpg` in `Claude AI Video Videos`.
3. Get its ID with drive_id.py. That's `HERO_IMAGE_ID`.
4. Optional (style library): add 3–10 more looks of the same character (different hair accent color, accessory or art style) and record their IDs. Each video can use a different one as `ref_id`.

---

## 6. Make.com (👤 YOU for account, connections and keys; 🤖 CLAUDE builds the scenarios)

**Order:** do 6.1 and 6.2 (👤), then section 7 (connect Claude Code to Make), then come back for the 🤖 step of 6.2 and 6.3–6.7.

### 6.1 Account
make.com → sign up → Organization → **Subscription → Core** (or higher). Note your **zone** from the browser URL (e.g. `us2.make.com`) and your **team** (Team → the ID is in the URL).

### 6.2 Connections (👤 YOU; they need your logins)
In Make → left menu **Connections** → **Add**:
1. **Google Drive** (app "Google Drive") → sign in with the Drive account from section 5 → allow all requested scopes. Name it `AI Video Drive`.
2. **Gemini AI** (app "Gemini AI", by Make) → paste your **Gemini API key** → Save. Name it `AI Video Gemini`.

**🤖 CLAUDE:** once Make MCP is connected (section 7), run `connections_list` for the team and record both connection IDs (numbers): `GDRIVE_CONN_ID` and `GEMINI_CONN_ID`.

### 6.3 Build the 5 scenarios (🤖 CLAUDE, through Make MCP)
Appendix A holds 5 blueprint files. Each one has `blueprint` (name, flow, metadata), `scheduling` and, for 4 of them, `interface`.

**Step 1: placeholders.** Before creating anything, replace these values in a copy of each blueprint:

| Placeholder in the blueprint | Replace with |
|---|---|
| `111111` (every `"__IMTCONN__": 111111`) | `GDRIVE_CONN_ID` (number) |
| `222222` (every `"__IMTCONN__": 222222`) | `GEMINI_CONN_ID` (number) |
| the tokens `VIDEOS_FOLDER_ID`, `READY_FOLDER_ID`, `DONE_FOLDER_ID` | each token, **wherever it appears**, with that folder's real ID. Keep the slashes, so `/VIDEOS_FOLDER_ID/READY_FOLDER_ID` becomes `/<videos ID>/<ready ID>` |
| `HERO_IMAGE_ID` | your hero image's Drive ID |
| `PASTE_OMNIAKEY_KEY_HERE`, `PASTE_HEDRA_KEY_HERE` | **leave them as they are.** The human replaces them in section 6.5 |

The folder value is a **path of folder IDs from the top of My Drive**. That's why section 5.1 puts the folder at the top of My Drive. If your folder is nested, the path has to list every parent ID in order, e.g. `/<parent ID>/<VIDEOS_FOLDER_ID>`.

**Step 2: create.** For each file, in order 1 → 5:
1. `scenarios_create` with `teamId`, `blueprint` = the file's `blueprint`, and `scheduling` = the file's `scheduling`.
2. If the file has `interface`: `scenarios_set-interface` with `{"input": <file.interface>, "output": []}`.
3. Record the new scenario ID in CLAUDE.md (section 7.3).

If `scenarios_create` fails with "Module not found", confirm the module name with `app-modules_list` for that app (google-drive, gemini-ai, http, json, util, builtin). The names in Appendix A are copied from a working build.

**Manual alternative (👤 YOU, if MCP creation fails):** Make → Scenarios → **Create a new scenario** → the **…** menu at the bottom → **Import Blueprint** → choose the `blueprint` part of the file, saved as its own .json. Then **open every Google Drive and Gemini module**, select your connection, and re-pick the folder with the folder picker. Set **Scheduling** (clock icon) to "On demand" (or every 15 min for Song). Add the **Scenario inputs** (scenario settings → Inputs) exactly as listed in the file's `interface`. Click **Save**.

### 6.4 What each scenario does (field reference)

**1. AI Video – Song (OmniaKey → Drive)**: schedule "every 15 min", **kept OFF between songs**.
| # | Module | Key settings |
|---|---|---|
| 1 | Google Drive › Watch Files in a Folder | Folder = Ready; watch = by created time; limit 1 |
| 20 | Tools › Set variable | `omnia_auth` = `Bearer <OmniaKey key>` (👤 human pastes) |
| 2 | Google Drive › Download a File | File ID `{{1.id}}` |
| 3 | JSON › Parse JSON | `{{toString(2.data)}}` |
| 4, 5 | JSON › Transform to JSON | `{{3.input}}`, `{{3.parameters}}` (escapes the lyrics safely) |
| 6 | HTTP › Make a request | POST `https://api.omniakey.com/v1/media/tasks`, headers Authorization / Content-Type / Idempotency-Key, body `{"model":"suno-v4.5","type":"audio","operation":"generate","input":{{4.json}},"parameters":{{5.json}}}` |
| 7 | Sleep | 120 s |
| 8 | HTTP GET task | `…/v1/media/tasks/{{6.data.id}}` |
| 9 | Router | A: status = `succeeded` → 10 download MP3 → 11 upload `Vera<date>-<slug>-Song.mp3` to Claude AI Video Videos → 12 log to Done. B: not succeeded → 13 sleep 180 → 14 GET again → 15 router → success path 16–18, or failure log 19 |

**2. CLAUDE AI Video – Stills from file (Gemini → Drive)**: on demand, ON. Input `request_file_id`.
| # | Module | Key settings |
|---|---|---|
| 6 | Drive › Download | the request JSON (`request_file_id`) |
| 7 | Parse JSON | `{slug, prefix, model?, ref_id?, scenes[{id, setting, prompt}]}` |
| 1 | Drive › Download | reference image = `ifempty(7.ref_id; HERO_IMAGE_ID)` |
| 8 | Iterator | `7.scenes` |
| 3 | Gemini AI › Generate an image | model `ifempty(7.model; "gemini-3-pro-image")`; image = the reference; prompt = `prefix` + blank line + scene `prompt`; JPEG, **2K, 9:16**. Error handler: **Ignore** (one failed image doesn't stop the batch) |
| 4 | Drive › Upload | `Vera<date>-<slug>-<id>-<setting>.jpg` → Claude AI Video Videos |

Optional: duplicate this scenario as "Stills from file **B**" (Make → scenario … → Clone) to run two batches in parallel. One scenario can only run one execution at a time.

**3. CLAUDE AI Video – Clips Omni (Gemini Omni → Drive)**: on demand, ON. Inputs `slug`, `prefix`, `scenes_json` = `[{id, still_id, prompt}]`.
| # | Module | Key settings |
|---|---|---|
| 2 | Parse JSON | `scenes_json` (an array, so one bundle per scene) |
| 3 | Drive › Download | `still_id` (the cutaway still) |
| 7 | Transform to JSON | `prefix` + blank line + `prompt` |
| 8 | Gemini AI › Make an API call | POST `/v1beta/interactions`, body `{"model":"gemini-omni-1.1-flash","input":[{"type":"image",…base64 still…},{"type":"text","text":<7.json>}],"response_format":{"type":"video","aspect_ratio":"9:16"}}`. Error handler: Ignore |
| 9, 10 | Iterators | `8.body.steps` → `9.content` |
| 11 | Drive › Upload | filter `10.type = video`; `toBinary(10.data; base64)` → `Vera<date>-<slug>-<id>-Omni.mp4` |

**4. CLAUDE AI Video – Hedra Submit (no wait)**: on demand, ON. Inputs `slug`, `run_tag`, `prefix`, `scenes_json` = `[{id, still_id, audio_id, prompt}]`.
| # | Module | Key settings |
|---|---|---|
| 1 | Set variable | `hedra_auth` = `Bearer <Hedra key>` (👤 human pastes) |
| 2 | Parse JSON | scenes |
| 3, 4 | Drive download still → HTTP POST `https://api.hedra.com/v3/files` (multipart `file`) | uploads the opening still to Hedra |
| 5, 6 | Drive download audio → POST `/v3/files` | uploads the vocal slice |
| 7 | Transform to JSON | `prefix` + `prompt` |
| 8 | HTTP POST `https://api.hedra.com/v3/models/hedra-character-3` | `{"input":{"prompt":…,"start_image":{"source":"url","url":<4.data.url>},"audio":{"source":"url","url":<6.data.url>},"aspect_ratio":"9:16","resolution":"1080p"},"idempotency_key":"vera-<slug>-<id>-<run_tag>"}` |
| 9 | Drive › Create file from text → **Done** | `Vera<date>-<slug>-<id>-HedraJob` with content `<id>|<job_id>` |

**5. CLAUDE AI Video – Hedra Collect**: on demand, ON. Inputs `slug`, `jobs_json` = `[{id, job_id}]`.
| # | Module | Key settings |
|---|---|---|
| 1 | Set variable | `hedra_auth` (👤 human pastes) |
| 2 | Parse JSON | jobs |
| 10 | HTTP GET `https://api.hedra.com/v3/jobs/{{2.job_id}}` | status |
| 12 | HTTP GET `{{10.data.outputs[1].url}}` | filter: status = `COMPLETED`; parse response **No** |
| 13 | Drive › Upload | `Vera<date>-<slug>-<id>-Hedra.mp4` → Claude AI Video Videos |
| 14 | Drive › Create file from text → Done | `…-HedraLog` with status and **cost** (the Hedra spend record) |

### 6.5 Paste the keys (👤 YOU; Claude must not do this or watch it)
1. Make → Scenarios → **AI Video – Song** → click module **20** (Set variable) → Variable value: replace `Bearer PASTE_OMNIAKEY_KEY_HERE` with `Bearer ` followed by your OmniaKey key (one space after Bearer) → **OK** → **Save** (bottom toolbar, or Ctrl/Cmd+S).
2. **Hedra Submit** → module **1** → `Bearer <your Hedra key>` → OK → **Save**.
3. **Hedra Collect** → module **1** → the same → OK → **Save**.
4. The Gemini key already lives in the Gemini AI connection (6.2).

Forgetting **Save** is the most common failure. It shows up as `Unauthorized` at the first HTTP module.

### 6.6 Turn scenarios ON and OFF (scheduling states)
| Scenario | State | Why |
|---|---|---|
| Stills from file (and B) | **ON** | On-demand scenarios must be active before `scenarios_run` works. Being ON costs nothing; they only run when called |
| Clips Omni | **ON** | same |
| Hedra Submit, Hedra Collect | **ON** | same |
| **Song** | **OFF between songs** | It's a watch scenario. While ON it checks Ready every 15 min, and every check spends a credit even when the folder is empty. Turn it ON only to make a song (section 9, step 5), then OFF |

🤖 CLAUDE: `scenarios_activate` for scenarios 2–5 now. Leave Song inactive.

### 6.7 Verify the build (🤖 CLAUDE)
For each scenario, run `scenarios_get` and confirm:
- no `111111`, `222222`, `VIDEOS_FOLDER_ID`, `READY_FOLDER_ID`, `DONE_FOLDER_ID` or `HERO_IMAGE_ID` text is left anywhere;
- `scenarios_interface` returns the inputs from Appendix A;
- (👤 YOU) in the Make editor, every Drive module shows your folder **name** (not a blank), and Song module 20 and Hedra module 1 hold your key (just check it's there; don't show it to Claude).

---

## 7. Connect Claude Code to Make (👤 YOU once, then 🤖 CLAUDE)

### 7.1 Add the Make MCP server
In Terminal:
```bash
cd ~/VeraEngine && claude mcp add --scope user --transport http make https://mcp.make.com/claude
claude
```
Inside Claude Code, type `/mcp`, choose **make**, and authenticate. In the browser window, **select your organization and team, and allow all scopes** (Claude needs to create, read, activate, deactivate and run scenarios, and to read executions). The status should turn to connected.

If the connection fails, use an API-key URL instead (Make → profile → **API access** → add a token with all scopes, then `claude mcp add --scope user --transport http make "https://<your-zone>/mcp/u/<TOKEN>/v2"`). **That URL contains a secret.** Add it yourself in Terminal. Never paste it into the chat, and never commit it to a file.

### 7.2 Verify (🤖 CLAUDE)
- `scenarios_list` for the team returns your scenarios.
- `connections_list` shows the Drive and Gemini connections.
- Calling a scenario: `scenarios_run` with `scenarioId` and `data` = an object whose keys match the scenario inputs exactly (e.g. `{"slug":"Test1","prefix":"…","scenes_json":"[…]"}`; `scenes_json` and `jobs_json` are **strings** holding JSON arrays). Make may also list each on-demand scenario as its own tool (named like `s<ID>_<scenario name>`); either way works.
- Tool timeouts: a Make MCP call returns after about 25 s (OAuth) or 40 s (API-key URL). Longer runs keep going in Make. The call returns an `executionId`: poll `executions_get` until `displayStatus` is SUCCESS or ERROR. **Never re-run a scenario because a call returned early.** Make also refuses a second run while one is in progress ("Scenario is already being executed").

### 7.3 CLAUDE.md (🤖 CLAUDE writes it to `~/VeraEngine/CLAUDE.md`)
```
# Video engine operator rules
Read ENGINE_GUIDE.md first in every session. Follow section 9 in order and stop at every ⛔ gate.
Never ask for, print, store or paste API keys. Keys live only in Make (human-entered).
Never call OmniaKey, Gemini or Hedra directly. Use the Make scenarios.
No Omni or Hedra spend before Gate 3 approval. Hard stop after one video.
Record every new failure and its fix in ENGINE_GUIDE.md section 11.

## IDs (fill in during setup)
VV (synced output folder) = ~/Library/CloudStorage/GoogleDrive-<you>/My Drive/Claude AI Video Videos
VIDEOS_FOLDER_ID = …   READY_FOLDER_ID = …   DONE_FOLDER_ID = …
HERO_IMAGE_ID = …      STYLE_REF_IDS = …
Make team ID = …       zone = …
GDRIVE_CONN_ID = …     GEMINI_CONN_ID = …
Scenario IDs: SONG = …  STILLS = …  STILLS_B = …  OMNI = …  HEDRA_SUBMIT = …  HEDRA_COLLECT = …
Python = ~/vera-venv/bin/python3 (first on PATH as python3)
```

---

## 8. Smoke tests (🤖 CLAUDE; about $3–5 total). Run all five before a real video.

Use slug `Test1`. Write files to `$VV` with shell commands, then get their IDs with `drive_id.py`.

**About `<date>` in file names:** Make stamps the files it writes with the **New York** date (`formatDate(now; "YYYYMMDD"; "America/New_York")`). Set `DATE=$(TZ=America/New_York date +%Y%m%d)` and use `$DATE` for files you write. **For files Make wrote, never build the name from a date.** List them (`ls "$VV"/*-Test1-*`) and use the real name. A run that spans midnight in New York mixes dates; the scripts' `*-<slug>-…` patterns handle that.

Run `DATE=$(TZ=America/New_York date +%Y%m%d)` in every new shell before these commands. If a Make-written file isn't found under the `$DATE` name, `ls "$VV"/*-Test1-*` and use the real name.

**T1 Song (OmniaKey through Make).**
1. Write `$VV/Ready/Vera<YYYYMMDD>-Test1-SongRequest.json`:
```json
{"slug":"Test1","input":{"prompt":"Upbeat indie pop, female vocal mid-20s, clear diction, 110 BPM","lyrics":"[Verse]\nTesting one two, the engine is on,\nWrite me a song and then it is gone.\n[Chorus]\nThis is a test, this is a test,\nShort little song, then we can rest."},"parameters":{"title":"Engine Test"}}
```
2. Wait until `drive_id.py` prints an ID for it (the file has reached Drive).
3. `scenarios_activate` SONG. A run should start within seconds (check with `executions_list`). If none starts within 60 s, ask the human to open the Song scenario in Make and click **Run once**.
4. Wait about 2–5 min. Pass = `$VV/Vera$DATE-Test1-Song.mp3` exists and plays, and `Done/` has a SongLog.
5. `scenarios_deactivate` SONG. **Always**, pass or fail.

**T2 Still.** Write `$VV/Vera$DATE-Test1-StillsReq.json`:
```json
{"slug":"Test1","prefix":"<section 10.2 opening prefix, filled in for your character>","scenes":[{"id":"S01","setting":"Open-Cafe","prompt":"Outfit: cream knit sweater.\n\nScene: chest-up portrait at a sunny cafe table, relaxed, about to sing."}]}
```
Get its ID, then `scenarios_run` STILLS with `{"request_file_id":"<ID>"}`. Pass = `Vera$DATE-Test1-S01-Open-Cafe.jpg` lands in `$VV`, upright, looking like the hero.

**T3 Omni clip.** `scenarios_run` OMNI with `slug` = `Test1`, `prefix` = the section 10.4 cutaway prefix, and `scenes_json` = `[{"id":"S01","still_id":"<T2 still ID>","prompt":"Within the first 2 seconds she lifts a coffee cup and smiles."}]`. Pass = `…-Test1-S01-Omni.mp4` (about 10 s) lands. **If the run finished in under 3 s, it was a hidden Gemini 503** (the Ignore handler hides it). Wait 20–30 min and retry.

**T4 Hedra lip-sync.**
1. Make the vocal stem and a 6 s slice:
```bash
cd ~/VeraEngine/runs && mkdir -p Test1 && cd Test1
audio-separator "$VV/Vera$DATE-Test1-Song.mp3" --model_filename UVR-MDX-NET-Voc_FT.onnx --output_format WAV --model_file_dir ~/VeraEngine/models
echo '[{"id":"S01","start":0,"end":6}]' > scenes_t.json
python3 ~/VeraEngine/scripts/slices.py *"(Vocals)"*.wav scenes_t.json "$VV" Vera$DATE-Test1
python3 ~/VeraEngine/scripts/chestcrop.py "$VV/Vera$DATE-Test1-S01-Open-Cafe.jpg" "$VV/Vera$DATE-Test1-S01-Close.jpg"
python3 ~/VeraEngine/scripts/drive_id.py "$VV/Vera$DATE-Test1-S01-Vox.mp3" "$VV/Vera$DATE-Test1-S01-Close.jpg"
```
2. `scenarios_run` HEDRA_SUBMIT with `slug` = `Test1`, `run_tag` = `t1`, `prefix` = the section 10.5 Hedra prefix, and `scenes_json` = `[{"id":"S01","still_id":"<Close ID>","audio_id":"<Vox ID>","prompt":"Mood: bright, playful."}]`.
3. Read `$VV/Done/Vera$DATE-Test1-S01-HedraJob` (content `S01|<job_id>`).
4. Wait about 5–10 min, then `scenarios_run` HEDRA_COLLECT with `slug` = `Test1`, `jobs_json` = `[{"id":"S01","job_id":"<job_id>"}]`. If nothing lands, the job isn't finished yet: wait 5 min and collect again (collecting is free to repeat).
5. Pass = `…-Test1-S01-Hedra.mp4` with mouth movement in sync, plus a HedraLog in Done that shows the cost.

**T5 Assembly + text.**
```bash
cd ~/VeraEngine/runs/Test1
echo '[{"id":"S01","start":0,"end":6,"lyric":"Testing one two"}]' > scenes.json
python3 ~/VeraEngine/scripts/make_manifest.py scenes.json "$VV" Test1 manifest.json
ffmpeg -v error -y -i "$VV/Vera$DATE-Test1-Song.mp3" -t 6 song6.mp3
MANIFEST=manifest.json RES=1080 END_CARD_SEC=2 python3 ~/VeraEngine/scripts/assemble.py x "$VV" song6.mp3 "$PWD/base.mp4"
echo '[{"t0":0.5,"t1":4.5,"style":"stamp","big":"ENGINE TEST","small":"it works"}]' > text.json
python3 ~/VeraEngine/scripts/kinetic.py base.mp4 text.json "$PWD/final.mp4" song6.mp3
ffprobe -v error -count_frames -select_streams v -show_entries stream=nb_read_frames -of csv=p=0 final.mp4   # must print 180
```
Pass = 180 frames, the Hedra clip plays with the cutaway intercut, and "ENGINE TEST" slams in with the script line wiping in under it.

**When T1–T5 pass, setup is complete.** Write "Setup verified <date>" at the top of CLAUDE.md.

---

## 9. Runbook: making a video (🤖 CLAUDE follows this every time)

**Recommended first real video:** 60–90 s, about 10–14 scenes, Mode C.

**Dates:** run `DATE=$(TZ=America/New_York date +%Y%m%d)` at the start of each shell session. Find Make-written files by listing `"$VV"/*-<Slug>-*`, not by building names from `$DATE`.

**Files per run** live in `~/VeraEngine/runs/<Slug>/`. Drive outputs go to `$VV`. **Slug** = a short CamelCase name, e.g. `CoffeeRun`. Every retry or re-render uses a **new slug suffix** (`CoffeeRun2b`) or a **new file name** (`…-r2.json`). Drive for desktop and Make can serve a stale copy of an overwritten file.

**Step 0. Goal.** Ask once: the idea, tone, visual feel, must-use lines, length (60–90 s for a first video), mode (recommend C), and which character look (`ref_id`) to use. Record the answers in `runs/<Slug>/brief.md`.

**Step 1. Research (web search).** If the song is about real events, find 5–7 concrete, named, checkable examples with direct personal impact. Separate **confirmed** facts (with links) from **open questions**, and phrase the open ones as questions, not claims.

**Step 2. One Big Idea.** One sentence that everything serves. Arc: problem → turn → hope. The hopeful part gets the last 30%.

**Step 3. ⛔ GATE 1: lyrics.** Present the research summary, the Big Idea, the **Suno style prompt** and the **full lyrics with `[Section]` tags**. Lyric rules that worked:
- The chorus is simple, literal, and repeats the Big Idea.
- Verses are half-time and conversational, so every word is understood. Ask for "very clear crisp diction, dry upfront lead vocal, minimal reverb" in the style prompt (it makes lip-sync and timing easier).
- One light deadpan joke line.
- If you use another language, keep it to short hooks a listener can read on screen.
- A short spoken intro or outro is fine, but it may be too quiet to time (step 6).
- The style prompt sets genre, BPM, voice, instruments and mood. Change the genre every video.

Wait for approval.

**Step 4. Character look.** Pick the `ref_id` (hero or a style-library image). Record it.

**Step 5. Song.**
1. Write `$VV/Ready/Vera$DATE-<Slug>-SongRequest.json` = `{"slug":"<Slug>","input":{"prompt":"<style prompt>","lyrics":"<lyrics with [Section] tags and \n line breaks>"},"parameters":{"title":"<Song Title>"}}`. Write it with Python `json.dump(..., ensure_ascii=False)` so the quotes and accents stay valid.
2. Confirm it has a Drive ID (drive_id.py).
3. `scenarios_activate` SONG and confirm with `executions_list` that a run started. If no run starts within 60 s, ask the human to click **Run once**.
4. Wait for `…-<Slug>-Song.mp3` (2–5 min).
5. `scenarios_deactivate` SONG.
6. Play the first seconds (`ffprobe` the duration) and send the user the file path. If a failure log lands, report the OmniaKey task ID.

**Step 6. Timing, then ⛔ GATE T1 (ear check).**
0. `cd ~/VeraEngine/runs/<Slug>` (create it first). All steps below run from there.
1. `audio-separator <Song.mp3> --model_filename UVR-MDX-NET-Voc_FT.onnx --output_format WAV --model_file_dir ~/VeraEngine/models` gives the `(Vocals)` WAV.
2. `python3 ~/VeraEngine/scripts/vocal_timing.py <vocals.wav>` prints the sung phrases. Find the section starts.
3. Find chorus repeats with `python3 ~/VeraEngine/scripts/vocal_timing.py <vocals.wav> --repeat <first chorus start> 2.0`.
4. For **each section**: `python3 ~/VeraEngine/scripts/align.py <vocals.wav> <start> <end> "line 1" "line 2" …` gives the start and end of every lyric line. **Never spread lines evenly across a section.**
5. Save `timings.json` = `[{"n":1,"section":"Verse 1","text":"…","start":11.6,"end":14.2}, …]`.
6. **Send the user a timing table** (time | section | lyric) and **3 moments to ear-check** ("the chorus hook starts at 0:50.1"). Fix what they flag. Nothing downstream starts before T1 is approved.

**Step 7. Scene map.** Make `scenes.json`, one entry per scene:
```json
{"id":"S01","start":0.0,"end":6.4,"section":"Verse 1","lyric":"<words sung in this window>",
 "setting":"Cafe","outfit":"<outfit>","open_prompt":"<opening still>","cut_prompt":"<cutaway still>",
 "omni_prompt":"<story action>","hedra_prompt":"Mood: …","omni_priority":"A","text":null}
```
- Every boundary sits on a **line boundary** from timings.json.
- Scenes run 4.5–9 s.
- Each scene's visuals match the lyric sung in it.
- Every chorus repeat uses the same setting.
- The last scene ends exactly at the song's end.

**Step 8. ⛔ GATE 2: scene pack.** For each scene, show:
- (a) the **video prompt** (story action first, with timing: "within the first 2 s…");
- (b) the **opening still** prompt (character face-first, chest-up, **at rest**: no pointing, waving, wind-blown hair or mid-motion pose, because the clip starts from this exact frame);
- (c) the **cutaway still** prompt (a clearly different camera position; the character absent, in profile, from behind, small in frame, or only hands, *doing* the action; **never idle face to camera**; for object-only shots write "NO PEOPLE" and pass a non-character `ref_id`, see step 9);
- (d) the **on-screen text** items, each tied to the exact phrase that sings those words;
- (e) the **Omni priority**: A = the action tells the story, B = supports it, C = mood.

Wait for approval.

**Step 9. Stills.**
- Write `$VV/Vera$DATE-<Slug>-OpensReq.json` and `…-CutsReq.json`, each `{"slug","prefix","ref_id","scenes":[{"id","setting","prompt"}]}`:
  - **opening prompt** = `"FRAMING: chest-up medium close-up portrait…\n\nOutfit: …\n\nScene: …"`, with `setting` = `Open-<Place>`;
  - **cutaway prompt** = `"Outfit (<name>): …\n\nScene: …"`, with `setting` = `Cut-<Place>`.
- `prefix` = section 10.2 for opens and section 10.3 for cuts.
- For "NO PEOPLE" cutaways, put them in a separate request whose `ref_id` is an already-made cutaway still (not the hero). Otherwise the hero reference pulls the character into the frame.
- Run STILLS (and STILLS_B in parallel) with each request's ID. At most about 16 scenes per request.
- **After every run, list what landed in `$VV` and re-run only the missing IDs as a NEW request file** (`…-OpensReq-r2.json`). A "success" run doesn't mean every image was made.
- **A regenerated (replacement) still must get a new file name.** Change its `setting` (e.g. `Cut-Cafe` → `Cut-Cafe2`). Otherwise Drive for desktop saves it as `name (1).jpg`, which make_manifest.py ignores, and the rejected still ends up in the video. Move the rejected still to a `_rejected/` subfolder, and set `"cut"` (or the Close still you feed Hedra) to the new name.
- If `gemini-3-pro-image` keeps failing (503 "high demand"), add `"model":"gemini-2.5-flash-image"` to the retry request.
- **Self-check every still before Gate 3:**
  - the content matches the prompt and the lyric;
  - the camera is upright (not sideways);
  - no UI, text or REC icons;
  - the pose and hair are at rest;
  - the face matches the hero;
  - the cutaway shows the right subject.
  
  Regenerate failures first.

**Step 10. ⛔ GATE 3: stills.**
- Crop every opening with `python3 ~/VeraEngine/scripts/chestcrop.py <open.jpg> <Close.jpg>` (the face fills about 22% of the height, which improves lip-sync).
- Build a contact sheet (ffmpeg tile or PIL) **with a caption under every still**: scene, lyric, what it should show.
- Show the openings (crops) and the cutaways, plus the list of fixes you already made.
- **No video spend before approval.**

**Step 11. Clips.**
- **Hedra:**
  1. `python3 ~/VeraEngine/scripts/slices.py <vocals.wav> scenes.json "$VV" Vera$DATE-<Slug>` makes one loudness-normalized vocal-only MP3 per scene.
  2. `python3 ~/VeraEngine/scripts/drive_id.py` on all slices and Close stills.
  3. Run HEDRA_SUBMIT once with every scene: `slug`, `run_tag` (e.g. `r1`), `prefix` (10.5), `scenes_json` `[{id, still_id: Close ID, audio_id: Vox ID, prompt: "Mood: …"}]`. One run submits all of them, about 1 min per 10 scenes.
  4. Read the HedraJob files in Done to build `jobs_json`.
  5. Wait about 10 min, then run HEDRA_COLLECT. Repeat Collect **only for the scenes still missing** every 5 min. Re-collecting a scene that already landed makes a `(1)` duplicate and a second HedraLog, which double-counts the Hedra cost.
  6. **Re-rendering a scene** (e.g. after a new still) uses a slug suffix (`<Slug>b`) so the new clip gets a new name. Then set `"hedra"` in scenes.json to that file name.
- **Omni:**
  - **One scene per call** (multi-scene calls often land only one clip). Go in **priority order A → B → C**.
  - `prefix` = 10.4, `scenes_json` = `[{id, still_id: cutaway still ID, prompt: omni_prompt}]`.
  - After each call, check that `…-<id>-Omni.mp4` landed.
  - **A run that ends in under 3 s = Gemini 503.** Stop and retry in 20–30 min, up to about 4 rounds.
  - Missing C-priority clips are fine: assembly turns them into a "photo drop".
- **Test one full scene first** (Hedra + Omni + a 1-scene assembly) and show the user before you run all of them.

**Step 12. Assembly + text.**
```bash
cd ~/VeraEngine/runs/<Slug>
python3 ../../scripts/make_manifest.py scenes.json "$VV" <Slug> manifest.json
MANIFEST=manifest.json RES=1080 END_CARD_SEC=4.3 python3 ../../scripts/assemble.py x "$VV" "$VV/Vera$DATE-<Slug>-Song.mp3" "$PWD/final_base.mp4" [logo.png]
python3 ../../scripts/kinetic.py final_base.mp4 text.json "$PWD/final.mp4" "$VV/Vera$DATE-<Slug>-Song.mp3"
```
- If a scene was re-rendered under another slug, set `"hedra"` or `"cut"` to that exact file name in scenes.json.
- A cutaway with no Omni clip uses the cutaway still as a photo drop automatically.
- Intercut timing (assemble.py): Hedra for the first ≤3 s (≤40% of the scene), then the Omni piece (≤3 s, `CUT_MAX`), then Hedra again. Scenes under 4.5 s stay Hedra-only.
- `text.json` items (kinetic.py styles):
  - `stamp`: a hook slams in, with `small` wiping in underneath (e.g. a translation);
  - `stat`: a big accent-color number, with a `small` descriptor typed word by word;
  - `check`: a checklist item; set `row` (0–4) and `until` so the items stack;
  - `write`: a sincere line typed in script;
  - `title`: stacked lines split by `|`, plus `y`, `size`, `small`, `small_y`, `small_style`. Use it for the opening title (t0 about 1.2 s) and the end card (last about 4 s).
  - Every item has `t0` and `t1` in seconds. Set `t0` 0.0–0.1 s **before the phrase that sings those words** (kinetic.py snaps to the nearest beat, within 0.18 s).
  - Keep 1 accent color and 2–3 words per stamp.

**Step 13. Final QA (required before Gate 4).**
- Frame count = song length × 30 (ffprobe `nb_read_frames`).
- `python3 ~/VeraEngine/scripts/audit.py final.mp4 manifest.json scenes.json audit.jpg`: every scene's frames match its lyric.
- No frozen frame over 1 s outside the photo drops.
- Text never covers the mouth; hooks never appear before they're sung.
- Every A-priority cutaway has a real clip, or is named in the report.
- The title shows on the opening and end cards.
- Fix everything you can.

**Step 14. ⛔ GATE 4: deliver.**
- Copy `final.mp4` to `$VV/Vera$DATE-<Slug>-Final-9x16.mp4`, so it syncs to Drive.
- Report:
  - the file path and Drive link;
  - the audit sheet;
  - spend: the **Hedra** cost (sum of the HedraLog `cost` lines in Done), the **Gemini** charges (AI Studio billing page), **OmniaKey** (dashboard), and **Make** credits (each scenario's operations);
  - anything that missed the plan;
  - any new lesson (also add it to section 11).
- Hard stop.

---

## 10. Prompt templates (fill in your character; worked example = Vera)

### 10.1 Character lock (the same words in every still and video prompt)
Template: `<Art style, e.g. Photorealistic> <who: age, gender>, <hair: cut, color, one accent detail>, <one accessory>, <skin/face details>, <eye color: MUST match the hero image>, <signature item always visible>, <expression/attitude>.`

AI Video example: *Photorealistic young woman, 24 years old, glossy black jaw-length blunt bob with heavy straight bangs, one clay-orange streak clearly visible in the front bangs, small orange daisy in her hair, light freckles, small cross necklace always visible, cool direct gaze, conventionally pretty face.*

**The hero image wins over the text.** If the text says grey eyes and the image shows blue, every still comes out wrong. Check that the two agree before writing any still prompt.

### 10.2 Opening-still prefix (send as `prefix` for opens)
```
<CHARACTER LOCK>. Match the attached reference image exactly for face and features. Fashionable modern outfit that changes per scene. No microphone. No headset. Natural skin, clean composition, no awkward pose, no extreme angle, no distortion. Only <NAME>'s face is resolved; all other people have their backs turned, are silhouetted, or fall naturally out of focus from shallow depth of field. Never pixelate, smudge or artificially blur faces. The starting image shows the scene before any lyric activity occurs. Wardrobe: fashionable, trendy and youthful with tasteful, modest coverage. OPENING STILL: medium close-up, chest-up framing, <NAME>'s face large in frame (roughly a quarter of the frame height), facing camera, mouth relaxed and slightly open as if about to sing, hands below chin level and never covering the mouth. Vertical 9:16. No text, captions, logos, UI overlays, REC icons or interface elements anywhere. Background signs and screens show only shapes and colors, no readable words. Camera level and upright: horizon horizontal, walls vertical; the image is never rotated, tilted or sideways. Starting pose is neutral and relaxed (standing, walking or seated naturally, hands down or resting); no pointing, waving, reaching toward camera or held gestures, because the clip starts from this exact frame. Hair at rest and neatly in place (no wind, no motion blur, no strands flying); nothing in the frame is caught mid-motion.
```

### 10.3 Cutaway-still prefix (send as `prefix` for cuts)
```
Photorealistic cinematic music-video frame. <NAME> is <short character lock>; match the attached reference for her face and hair. This is a STORY CUTAWAY (B-roll) from a clearly different camera position than her close-up singing shots: the story action is the subject. <NAME> is either not in the frame at all, or seen in profile / from behind / small in frame while actively doing the action described; she is never idle facing camera and her mouth is not the focus. No microphone. Other people have backs turned, are silhouetted, or fall naturally out of focus. Props realistically sized and placed. Vertical 9:16. No text, captions, logos, camera viewfinder overlays, REC indicator or UI chrome; this is a plain cinematic photograph, not a phone or app screen. Background signs and screens show only shapes and colors, no readable words. Camera level and upright; never rotated or sideways. Nothing caught mid-motion; hair at rest.
```

### 10.4 Omni cutaway prefix (send as `prefix` to Clips Omni; the scene prompt follows "Scene action:")
```
Photorealistic cinematic story cutaway for a music video, warm natural light, clean composition. Animate the attached start image: it is the exact first frame; keep its framing, style and colors. The action described below is the point of the clip and must visibly happen within the first 3 seconds. No new people appear; any person already in frame stays as framed (hands, back or silhouette only), never turns toward camera, and no new face is invented. Props stay realistically sized. No jump cuts, no fades, no text overlays. Vertical 9:16. Scene action:
```
Omni prompt style: `Within the first 2 seconds <one clear physical action>.` One action per clip. Omni ignores lighting changes, so build the lighting into the still.

### 10.5 Hedra lip-sync prefix (send as `prefix` to Hedra Submit)
```
Animate the start image as the exact first frame. <NAME> sings the provided vocal with precise lip-sync: mouth shapes follow every syllable and close fully in pauses. Natural head motion, blinks and expressive eyebrows. Keep her face, <hair and accent details>, accessory and outfit exactly as in the image. Hands stay low, away from the mouth. Stays framed chest-up, mostly facing camera. Background stays consistent; background people faceless. No text, no microphone. Vertical 9:16.
```
Per-scene Hedra prompt: `Mood: <2–5 words>. Line: "<lyric>".` For scenes with no vocal: `Mood: quiet, listening; mouth closed while there is no voice.`

### 10.6 Look per video (optional)
Change one look element per video: the hair accent color, the accessory, or the art style (photoreal, anime cel-shaded, watercolor, charcoal). Use the matching style-library image as `ref_id`. For a non-photoreal style, start all three prefixes with the style line instead of "Photorealistic".

---

## 11. Troubleshooting (every row happened in the reference build)

| Symptom | Cause | Fix |
|---|---|---|
| Song request in Ready, nothing happens | The Song scenario is OFF (it's off between songs by design) | Activate it (or click **Run once** in Make), wait, then deactivate. An operator without Make access can't do this; the human flips the switch |
| `Unauthorized` at the first HTTP module | Key placeholder still there, or the key was pasted without clicking **Save** | Human: paste `Bearer <key>` → OK → **Save** (section 6.5) |
| `Scenario is not activated` on `scenarios_run` | On-demand scenarios must be ON | `scenarios_activate` (it costs nothing while idle) |
| `Scenario is already being executed` | The previous run is still going (an MCP call returns after 25–40 s while the run continues) | Poll `executions_get`, then run again |
| Make run "SUCCESS" but no file | An Ignore error handler hid a Gemini failure (usually 503 "high demand") | Runs under 3 s = failed. Retry in 20–30 min; for stills, try `gemini-2.5-flash-image` |
| Only 1 of N Omni clips landed | Gemini Omni capacity | One scene per call; priority A first; retry rounds every 25 min |
| Drive module shows a blank folder after import | The folder path points at the wrong place | Re-pick the folder with the picker and Save, or fix the `/ID/ID` path from the top of My Drive |
| `MISSING` from drive_id.py | The file hasn't uploaded yet, or Stream mode left it cloud-only | Wait (the script polls for 120 s). Check the Drive for desktop menu-bar icon; mark the folder Available offline |
| "Operation not permitted" reading the CloudStorage folder | macOS privacy | Give your terminal app Full Disk Access (section 5.2) |
| A retry used old content | Overwritten file served stale by sync or Make | Always use a new file name (`-r2`) or a new slug suffix |
| Timing is wrong in the second half / lines land early | Lines were spread evenly, or the quiet spoken intro was missed | align.py per section; ear-check 3 moments (Gate T1) |
| Hook text appears seconds early | Text was timed to the start of the chorus block | Tie `t0` to the phrase that sings the hook (`vocal_timing.py --repeat`) |
| Lip-sync weak or drifting | Full-mix audio, small face, or cumulative rounding | Vocal-only slices (slices.py), chest-up crops (chestcrop.py), assemble.py's frame-exact cuts. Never cut scenes with float seconds |
| Frozen hair or pose looks broken | The still was mid-motion (hair blowing, pointing) | Regenerate the still at rest; gestures go in the video prompt |
| Cutaway shows the character instead of the object | The hero reference pulls her in | "NO PEOPLE" in the prompt plus a non-character `ref_id` |
| Sideways or tilted still | The model rotated the frame | The upright-camera line in the prefix; reject at self-check |
| Static still in the final looks like a bug | No Omni clip, plain still | assemble.py's photo-drop effect is automatic; get A-priority clips |
| A clip from an older video shows up | The glob matched another run | Always pass the run's slug (make_manifest.py does) |
| chestcrop prints `noface` (no crop made) | The face detector missed a stylized or angled face | Look at the image, then rerun with `--box=x,y,w,h` (the face's pixel box) or regenerate the still more front-facing |
| `CascadeClassifier` missing in chestcrop | opencv 5.x | `pip install "opencv-python-headless<5"` |
| kinetic.py text in the wrong font | Fonts missing from `scripts/fonts/` | Section 4.4 |
| Org paused / "data transfer" errors in Make | Free plan limits | Core plan or higher |
| Hedra job never completes | Bad input, or out of credits | Check the job on hedra.com; buy credits; resubmit with a new `run_tag` **and a slug suffix** (`<Slug>b`), so the new clip gets a new name; set `"hedra"` in scenes.json |
| A redone still or clip is ignored; the old one shows in the video | Same output name, so Drive saved `name (1).ext`, which make_manifest.py skips | Always give regenerations a new name (new `setting` or slug suffix); set `"cut"`/`"hedra"` in scenes.json |
| No Drive ID on Windows | drive_id.py reads a macOS attribute | Copy the ID from the file's Drive link (`/file/d/<ID>/`), or run on a Mac |

---

## 12. Time and cost reference (actuals, Oct 2026)

| Stage | Time | Cost |
|---|---|---|
| Research + lyrics | 15–30 min | Claude plan |
| Song (OmniaKey Suno v4.5) | 2–5 min | under $2 |
| Vocal stem + timing + ear check | 15–30 min | free |
| Stills (about 2 per scene, 2K) | 20–60 min, Gemini capacity permitting | about $0.15–0.25 each |
| Hedra 1080p lip-sync | about 10–20 min for all scenes in parallel | about $0.05–0.07 per second of clip |
| Omni cutaways | about 40 s each when capacity is available, hours of retries when it isn't | about $1 per clip |
| Assembly + text + QA | 15–30 min | free |
| Make credits | | about 1,500–2,500 per full 3-min video (Core includes 10,000/mo) |

---

## Appendix A: Make blueprints (5 files)

Save each block as `~/VeraEngine/blueprints/<file name>`. Each file holds `blueprint` (pass to `scenarios_create` as `blueprint`), `scheduling` (pass as `scheduling`) and, where present, `interface` (pass to `scenarios_set-interface` as `{"input": <interface>, "output": []}`). Replace the placeholders first (section 6.3). Key placeholders stay until the human pastes the keys in Make.

### A.1 `1_Song.json`

```json
{
 "blueprint": {
  "name": "AI Video – Song (OmniaKey → Drive)",
  "flow": [
   {
    "id": 1,
    "module": "google-drive:watchFilesInAFolder",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111,
     "select": "create",
     "destination": "drive",
     "folderId": "/VIDEOS_FOLDER_ID/READY_FOLDER_ID",
     "mimeType": "all",
     "limit": 1
    },
    "mapper": {}
   },
   {
    "id": 20,
    "module": "util:SetVariable2",
    "version": 1,
    "parameters": {},
    "mapper": {
     "name": "omnia_auth",
     "value": "Bearer PASTE_OMNIAKEY_KEY_HERE"
    }
   },
   {
    "id": 2,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "select": "map",
     "file": "{{1.id}}",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf",
     "formatDrawings": "image/png"
    }
   },
   {
    "id": 3,
    "module": "json:ParseJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "json": "{{toString(2.data)}}"
    }
   },
   {
    "id": 4,
    "module": "json:TransformToJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "object": "{{3.input}}"
    }
   },
   {
    "id": 5,
    "module": "json:TransformToJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "object": "{{3.parameters}}"
    }
   },
   {
    "id": 6,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "url": "https://api.omniakey.com/v1/media/tasks",
     "method": "post",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{20.omnia_auth}}"
      },
      {
       "name": "Content-Type",
       "value": "application/json"
      },
      {
       "name": "Idempotency-Key",
       "value": "vera-{{1.id}}"
      }
     ],
     "timeout": "40",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "contentType": "json",
     "inputMethod": "jsonString",
     "jsonStringBodyContent": "{\"model\":\"suno-v4.5\",\"type\":\"audio\",\"operation\":\"generate\",\"input\":{{4.json}},\"parameters\":{{5.json}}}"
    }
   },
   {
    "id": 7,
    "module": "util:FunctionSleep",
    "version": 1,
    "parameters": {},
    "mapper": {
     "duration": "120"
    }
   },
   {
    "id": 8,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "url": "https://api.omniakey.com/v1/media/tasks/{{6.data.id}}",
     "method": "get",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{20.omnia_auth}}"
      }
     ],
     "timeout": "40",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true
    }
   },
   {
    "id": 9,
    "module": "builtin:BasicRouter",
    "version": 1,
    "routes": [
     {
      "flow": [
       {
        "id": 10,
        "module": "http:MakeRequest",
        "version": 4,
        "parameters": {
         "tlsType": "",
         "authenticationType": "noAuth"
        },
        "mapper": {
         "url": "{{8.data.assets[1].url}}",
         "method": "get",
         "headers": [],
         "timeout": "40",
         "shareCookies": false,
         "parseResponse": false,
         "allowRedirects": true,
         "stopOnHttpError": true,
         "requestCompressedContent": true
        },
        "filter": {
         "name": "succeeded",
         "conditions": [
          [
           {
            "a": "{{8.data.status}}",
            "o": "text:equal",
            "b": "succeeded"
           }
          ]
         ]
        }
       },
       {
        "id": 11,
        "module": "google-drive:uploadAFile",
        "version": 4,
        "parameters": {
         "__IMTCONN__": 111111
        },
        "mapper": {
         "select": "value",
         "destination": "drive",
         "folderId": "/VIDEOS_FOLDER_ID",
         "filename": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{3.slug}}-Song.mp3",
         "data": "{{10.data}}",
         "convert": false
        }
       },
       {
        "id": 12,
        "module": "google-drive:createAFileFromText",
        "version": 4,
        "parameters": {
         "__IMTCONN__": 111111
        },
        "mapper": {
         "destination": "drive",
         "folderId": "/VIDEOS_FOLDER_ID/DONE_FOLDER_ID",
         "name": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{3.slug}}-SongLog.txt",
         "content": "AI Video Song run log\nrequest_file_id: {{1.id}}\nrequest_file_name: {{1.name}}\nomniakey_task_id: {{6.data.id}}\nomniakey_status: {{8.data.status}}\nmp3_drive_file_id: {{11.id}}\nmp3_name: {{11.name}}\nlogged_at: {{now}}",
         "convert": false
        }
       }
      ]
     },
     {
      "flow": [
       {
        "id": 13,
        "module": "util:FunctionSleep",
        "version": 1,
        "parameters": {},
        "mapper": {
         "duration": "180"
        },
        "filter": {
         "name": "not succeeded",
         "conditions": [
          [
           {
            "a": "{{8.data.status}}",
            "o": "text:notequal",
            "b": "succeeded"
           }
          ]
         ]
        }
       },
       {
        "id": 14,
        "module": "http:MakeRequest",
        "version": 4,
        "parameters": {
         "tlsType": "",
         "authenticationType": "noAuth"
        },
        "mapper": {
         "url": "https://api.omniakey.com/v1/media/tasks/{{6.data.id}}",
         "method": "get",
         "headers": [
          {
           "name": "Authorization",
           "value": "{{20.omnia_auth}}"
          }
         ],
         "timeout": "40",
         "shareCookies": false,
         "parseResponse": true,
         "allowRedirects": true,
         "stopOnHttpError": true,
         "requestCompressedContent": true
        }
       },
       {
        "id": 15,
        "module": "builtin:BasicRouter",
        "version": 1,
        "routes": [
         {
          "flow": [
           {
            "id": 16,
            "module": "http:MakeRequest",
            "version": 4,
            "parameters": {
             "tlsType": "",
             "authenticationType": "noAuth"
            },
            "mapper": {
             "url": "{{14.data.assets[1].url}}",
             "method": "get",
             "headers": [],
             "timeout": "40",
             "shareCookies": false,
             "parseResponse": false,
             "allowRedirects": true,
             "stopOnHttpError": true,
             "requestCompressedContent": true
            },
            "filter": {
             "name": "succeeded",
             "conditions": [
              [
               {
                "a": "{{14.data.status}}",
                "o": "text:equal",
                "b": "succeeded"
               }
              ]
             ]
            }
           },
           {
            "id": 17,
            "module": "google-drive:uploadAFile",
            "version": 4,
            "parameters": {
             "__IMTCONN__": 111111
            },
            "mapper": {
             "select": "value",
             "destination": "drive",
             "folderId": "/VIDEOS_FOLDER_ID",
             "filename": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{3.slug}}-Song.mp3",
             "data": "{{16.data}}",
             "convert": false
            }
           },
           {
            "id": 18,
            "module": "google-drive:createAFileFromText",
            "version": 4,
            "parameters": {
             "__IMTCONN__": 111111
            },
            "mapper": {
             "destination": "drive",
             "folderId": "/VIDEOS_FOLDER_ID/DONE_FOLDER_ID",
             "name": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{3.slug}}-SongLog.txt",
             "content": "AI Video Song run log\nrequest_file_id: {{1.id}}\nrequest_file_name: {{1.name}}\nomniakey_task_id: {{6.data.id}}\nomniakey_status: {{14.data.status}}\nmp3_drive_file_id: {{17.id}}\nmp3_name: {{17.name}}\nlogged_at: {{now}}",
             "convert": false
            }
           }
          ]
         },
         {
          "flow": [
           {
            "id": 19,
            "module": "google-drive:createAFileFromText",
            "version": 4,
            "parameters": {
             "__IMTCONN__": 111111
            },
            "mapper": {
             "destination": "drive",
             "folderId": "/VIDEOS_FOLDER_ID/DONE_FOLDER_ID",
             "name": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{3.slug}}-SongLog.txt",
             "content": "AI Video Song run log\nrequest_file_id: {{1.id}}\nrequest_file_name: {{1.name}}\nomniakey_task_id: {{6.data.id}}\nomniakey_status: {{14.data.status}}\nmp3_drive_file_id: NONE (song not ready after ~5 min or failed; check task in OmniaKey)\nlogged_at: {{now}}",
             "convert": false
            },
            "filter": {
             "name": "not succeeded",
             "conditions": [
              [
               {
                "a": "{{14.data.status}}",
                "o": "text:notequal",
                "b": "succeeded"
               }
              ]
             ]
            }
           }
          ]
         }
        ]
       }
      ]
     }
    ]
   }
  ],
  "metadata": {
   "version": 1,
   "scenario": {
    "roundtrips": 1,
    "maxErrors": 3,
    "autoCommit": true,
    "autoCommitTriggerLast": true,
    "sequential": true,
    "confidential": false,
    "dataloss": false,
    "dlq": false,
    "freshVariables": false
   }
  }
 },
 "scheduling": {
  "type": "indefinitely",
  "interval": 900
 }
}
```

### A.2 `2_Stills_from_file.json`

```json
{
 "blueprint": {
  "name": "CLAUDE AI Video – Stills from file (Gemini → Drive)",
  "flow": [
   {
    "id": 6,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "file": "{{var.input.request_file_id}}",
     "select": "map",
     "formatDrawings": "image/png",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf"
    }
   },
   {
    "id": 7,
    "module": "json:ParseJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "json": "{{toString(6.data)}}"
    }
   },
   {
    "id": 1,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "file": "{{ifempty(7.ref_id; \"HERO_IMAGE_ID\")}}",
     "select": "map",
     "formatDrawings": "image/png",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf"
    }
   },
   {
    "id": 8,
    "module": "builtin:BasicFeeder",
    "version": 1,
    "parameters": {},
    "mapper": {
     "array": "{{7.scenes}}"
    }
   },
   {
    "id": 3,
    "module": "gemini-ai:generateAnImageV2",
    "version": 1,
    "parameters": {
     "__IMTCONN__": 222222
    },
    "mapper": {
     "model": "{{ifempty(7.model; \"gemini-3-pro-image\")}}",
     "images": [
      {
       "data": "{{1.data}}",
       "fileName": "{{1.name}}",
       "mimeType": "image/jpeg",
       "upload_format": "base64"
      }
     ],
     "prompt": "{{7.prefix}}\n\n{{8.prompt}}",
     "response_format": {
      "mimeType": "image/jpeg",
      "imageSize": "2K",
      "aspectRatio": "9:16"
     }
    },
    "onerror": [
     {
      "id": 5,
      "module": "builtin:Ignore",
      "version": 1,
      "parameters": {},
      "mapper": {}
     }
    ]
   },
   {
    "id": 4,
    "module": "google-drive:uploadAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "data": "{{3.data}}",
     "select": "value",
     "convert": false,
     "filename": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{7.slug}}-{{8.id}}-{{8.setting}}.jpg",
     "folderId": "/VIDEOS_FOLDER_ID",
     "destination": "drive"
    }
   }
  ],
  "metadata": {
   "instant": false,
   "version": 1,
   "scenario": {
    "dlq": false,
    "dataloss": false,
    "maxErrors": 3,
    "autoCommit": true,
    "roundtrips": 1,
    "sequential": true,
    "confidential": false,
    "freshVariables": false,
    "autoCommitTriggerLast": true
   }
  }
 },
 "scheduling": {
  "type": "on-demand"
 },
 "interface": [
  {
   "name": "request_file_id",
   "type": "text",
   "label": "Drive file ID of the stills request JSON",
   "required": true
  }
 ]
}
```

### A.3 `3_Clips_Omni.json`

```json
{
 "blueprint": {
  "name": "CLAUDE AI Video – Clips Omni (Gemini Omni → Drive)",
  "flow": [
   {
    "id": 2,
    "module": "json:ParseJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "json": "{{var.input.scenes_json}}"
    }
   },
   {
    "id": 3,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "file": "{{2.still_id}}",
     "select": "map",
     "formatDrawings": "image/png",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf"
    }
   },
   {
    "id": 7,
    "module": "json:TransformToJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "object": "{{var.input.prefix}}\n\n{{2.prompt}}"
    }
   },
   {
    "id": 8,
    "module": "gemini-ai:makeApiCall",
    "version": 1,
    "parameters": {
     "__IMTCONN__": 222222
    },
    "mapper": {
     "url": "/v1beta/interactions",
     "method": "POST",
     "headers": [
      {
       "key": "Content-Type",
       "value": "application/json"
      }
     ],
     "body": "{\"model\":\"gemini-omni-1.1-flash\",\"input\":[{\"type\":\"image\",\"data\":\"{{base64(3.data)}}\",\"mime_type\":\"image/jpeg\"},{\"type\":\"text\",\"text\":{{7.json}}}],\"response_format\":{\"type\":\"video\",\"aspect_ratio\":\"9:16\"}}"
    },
    "onerror": [
     {
      "id": 12,
      "module": "builtin:Ignore",
      "version": 1,
      "parameters": {},
      "mapper": {}
     }
    ]
   },
   {
    "id": 9,
    "module": "builtin:BasicFeeder",
    "version": 1,
    "parameters": {},
    "mapper": {
     "array": "{{8.body.steps}}"
    }
   },
   {
    "id": 10,
    "module": "builtin:BasicFeeder",
    "version": 1,
    "parameters": {},
    "mapper": {
     "array": "{{9.content}}"
    }
   },
   {
    "id": 11,
    "module": "google-drive:uploadAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "filter": {
     "name": "video part",
     "conditions": [
      [
       {
        "a": "{{10.type}}",
        "b": "video",
        "o": "text:equal"
       }
      ]
     ]
    },
    "mapper": {
     "data": "{{toBinary(10.data; \"base64\")}}",
     "select": "value",
     "convert": false,
     "filename": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{var.input.slug}}-{{2.id}}-Omni.mp4",
     "folderId": "/VIDEOS_FOLDER_ID",
     "destination": "drive"
    }
   }
  ],
  "metadata": {
   "instant": false,
   "version": 1,
   "scenario": {
    "dlq": false,
    "dataloss": false,
    "maxErrors": 3,
    "autoCommit": true,
    "roundtrips": 1,
    "sequential": true,
    "confidential": false,
    "freshVariables": false,
    "autoCommitTriggerLast": true
   }
  }
 },
 "scheduling": {
  "type": "on-demand"
 },
 "interface": [
  {
   "name": "slug",
   "type": "text",
   "required": true
  },
  {
   "name": "prefix",
   "type": "text",
   "required": false
  },
  {
   "name": "scenes_json",
   "type": "text",
   "required": true
  }
 ]
}
```

### A.4 `4_Hedra_Submit.json`

```json
{
 "blueprint": {
  "name": "CLAUDE AI Video – Hedra Submit (no wait)",
  "flow": [
   {
    "id": 1,
    "module": "util:SetVariable2",
    "version": 1,
    "parameters": {},
    "mapper": {
     "name": "hedra_auth",
     "value": "Bearer PASTE_HEDRA_KEY_HERE"
    }
   },
   {
    "id": 2,
    "module": "json:ParseJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "json": "{{var.input.scenes_json}}"
    }
   },
   {
    "id": 3,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "file": "{{2.still_id}}",
     "select": "map",
     "formatDrawings": "image/png",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf"
    }
   },
   {
    "id": 4,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "timeout": "120",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "url": "https://api.hedra.com/v3/files",
     "method": "post",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{1.hedra_auth}}"
      }
     ],
     "contentType": "multipart",
     "multipartBodyContent": [
      {
       "data": "{{3.data}}",
       "name": "file",
       "fileName": "{{3.name}}",
       "multipartFieldType": "file"
      }
     ]
    }
   },
   {
    "id": 5,
    "module": "google-drive:getAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "file": "{{2.audio_id}}",
     "select": "map",
     "formatDrawings": "image/png",
     "formatDocuments": "text/plain",
     "formatSpreadsheets": "text/csv",
     "formatPresentations": "application/pdf"
    }
   },
   {
    "id": 6,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "timeout": "120",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "url": "https://api.hedra.com/v3/files",
     "method": "post",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{1.hedra_auth}}"
      }
     ],
     "contentType": "multipart",
     "multipartBodyContent": [
      {
       "data": "{{5.data}}",
       "name": "file",
       "fileName": "audio.mp3",
       "multipartFieldType": "file"
      }
     ]
    }
   },
   {
    "id": 7,
    "module": "json:TransformToJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "object": "{{var.input.prefix}}\n\n{{2.prompt}}"
    }
   },
   {
    "id": 8,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "timeout": "120",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "url": "https://api.hedra.com/v3/models/hedra-character-3",
     "method": "post",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{1.hedra_auth}}"
      },
      {
       "name": "Content-Type",
       "value": "application/json"
      }
     ],
     "contentType": "json",
     "inputMethod": "jsonString",
     "jsonStringBodyContent": "{\"input\":{\"prompt\":{{7.json}},\"start_image\":{\"source\":\"url\",\"url\":\"{{4.data.url}}\"},\"audio\":{\"source\":\"url\",\"url\":\"{{6.data.url}}\"},\"aspect_ratio\":\"9:16\",\"resolution\":\"1080p\"},\"idempotency_key\":\"vera-{{var.input.slug}}-{{2.id}}-{{var.input.run_tag}}\"}"
    }
   },
   {
    "id": 9,
    "module": "google-drive:createAFileFromText",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "name": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{var.input.slug}}-{{2.id}}-HedraJob",
     "content": "{{2.id}}|{{8.data.job_id}}",
     "convert": false,
     "folderId": "/VIDEOS_FOLDER_ID/DONE_FOLDER_ID",
     "destination": "drive"
    }
   }
  ],
  "metadata": {
   "instant": false,
   "version": 1,
   "scenario": {
    "dlq": false,
    "dataloss": false,
    "maxErrors": 3,
    "autoCommit": true,
    "roundtrips": 1,
    "sequential": true,
    "confidential": false,
    "freshVariables": false,
    "autoCommitTriggerLast": true
   }
  }
 },
 "scheduling": {
  "type": "on-demand"
 },
 "interface": [
  {
   "name": "slug",
   "type": "text",
   "required": true
  },
  {
   "name": "run_tag",
   "type": "text",
   "required": true
  },
  {
   "name": "prefix",
   "type": "text",
   "required": true
  },
  {
   "name": "scenes_json",
   "type": "text",
   "required": true
  }
 ]
}
```

### A.5 `5_Hedra_Collect.json`

```json
{
 "blueprint": {
  "name": "CLAUDE AI Video – Hedra Collect",
  "flow": [
   {
    "id": 1,
    "module": "util:SetVariable2",
    "version": 1,
    "parameters": {},
    "mapper": {
     "name": "hedra_auth",
     "value": "Bearer PASTE_HEDRA_KEY_HERE"
    }
   },
   {
    "id": 2,
    "module": "json:ParseJSON",
    "version": 1,
    "parameters": {},
    "mapper": {
     "json": "{{var.input.jobs_json}}"
    }
   },
   {
    "id": 10,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "timeout": "120",
     "shareCookies": false,
     "parseResponse": true,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "url": "https://api.hedra.com/v3/jobs/{{2.job_id}}",
     "method": "get",
     "headers": [
      {
       "name": "Authorization",
       "value": "{{1.hedra_auth}}"
      }
     ]
    }
   },
   {
    "id": 12,
    "module": "http:MakeRequest",
    "version": 4,
    "parameters": {
     "tlsType": "",
     "authenticationType": "noAuth"
    },
    "mapper": {
     "timeout": "120",
     "shareCookies": false,
     "parseResponse": false,
     "allowRedirects": true,
     "stopOnHttpError": true,
     "requestCompressedContent": true,
     "url": "{{10.data.outputs[1].url}}",
     "method": "get",
     "headers": []
    },
    "filter": {
     "name": "completed",
     "conditions": [
      [
       {
        "a": "{{10.data.status}}",
        "b": "COMPLETED",
        "o": "text:equal"
       }
      ]
     ]
    }
   },
   {
    "id": 13,
    "module": "google-drive:uploadAFile",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "data": "{{12.data}}",
     "select": "value",
     "convert": false,
     "filename": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{var.input.slug}}-{{2.id}}-Hedra.mp4",
     "folderId": "/VIDEOS_FOLDER_ID",
     "destination": "drive"
    }
   },
   {
    "id": 14,
    "module": "google-drive:createAFileFromText",
    "version": 4,
    "parameters": {
     "__IMTCONN__": 111111
    },
    "mapper": {
     "name": "Vera{{formatDate(now; \"YYYYMMDD\"; \"America/New_York\")}}-{{var.input.slug}}-{{2.id}}-HedraLog",
     "content": "AI Video Hedra clip log\nscene: {{2.id}}\nhedra_job_id: {{2.job_id}}\nstatus: {{10.data.status}}\ncost: {{10.data.cost}} {{10.data.currency}}\nclip_drive_file_id: {{13.id}}\nlogged_at: {{now}}",
     "convert": false,
     "folderId": "/VIDEOS_FOLDER_ID/DONE_FOLDER_ID",
     "destination": "drive"
    }
   }
  ],
  "metadata": {
   "instant": false,
   "version": 1,
   "scenario": {
    "dlq": false,
    "dataloss": false,
    "maxErrors": 3,
    "autoCommit": true,
    "roundtrips": 1,
    "sequential": true,
    "confidential": false,
    "freshVariables": false,
    "autoCommitTriggerLast": true
   }
  }
 },
 "scheduling": {
  "type": "on-demand"
 },
 "interface": [
  {
   "name": "slug",
   "type": "text",
   "required": true
  },
  {
   "name": "jobs_json",
   "type": "text",
   "required": true
  }
 ]
}
```

---

## Appendix B: Scripts (9 files)

Save each block as `~/VeraEngine/scripts/<file name>`, exactly as printed. All of them run with `python3 <script> …`; each file's top comment gives its usage. The `fonts/` folder (section 4.4) sits next to them.

### B.1 `drive_id.py`

```python
#!/usr/bin/env python3
"""Print the Google Drive file ID of files inside the Google Drive for desktop folder (macOS).
Drive for desktop stores the ID as an extended attribute once the file has finished uploading.
Usage: python3 drive_id.py <file> [<file> ...] [--wait 120]   -> prints "<id>  <file>" per file
Waits (default 120 s) for new files that are still uploading. Exit code 1 if any ID is missing."""
import sys, subprocess, time, os
args = sys.argv[1:]; wait = 120
if "--wait" in args:
    i = args.index("--wait"); wait = int(args[i + 1]); del args[i:i + 2]
NAMES = ["com.google.drivefs.item-id#S", "com.google.drivefs.item-id"]
def get(f):
    for n in NAMES:
        r = subprocess.run(["xattr", "-p", n, f], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.strip(): return r.stdout.strip()
    return None
bad = 0
for f in args:
    t0 = time.time(); fid = get(f)
    while not fid and time.time() - t0 < wait:
        time.sleep(5); fid = get(f)
    if fid: print(f"{fid}  {os.path.basename(f)}")
    else: print(f"MISSING  {os.path.basename(f)}  (not synced yet? check the Drive for desktop menu-bar icon)"); bad = 1
sys.exit(bad)
```

### B.2 `slices.py`

```python
#!/usr/bin/env python3
"""Cut one loudness-normalized, vocal-only MP3 per scene for Hedra lip-sync (lesson: vocal stem = better lip-sync).
Usage: python3 slices.py <vocals.wav> <scenes.json> <out_dir> <file_prefix>
scenes.json: [{"id":"S01","start":0.0,"end":6.2, ...}, ...]  -> <out_dir>/<file_prefix>-S01-Vox.mp3 ..."""
import json, subprocess, sys, os
voc, scenes, out, pre = sys.argv[1:5]
os.makedirs(out, exist_ok=True)
for s in json.load(open(scenes)):
    a, b = float(s["start"]), float(s["end"])
    f = os.path.join(out, f"{pre}-{s['id']}-Vox.mp3")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-t", f"{b - a:.3f}", "-i", voc,
                    "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", "44100", "-ac", "2", "-b:a", "192k", f], check=True)
    print(f"{s['id']}  {a:.2f}-{b:.2f}  {f}")
```

### B.3 `vocal_timing.py`

```python
#!/usr/bin/env python3
"""AI Video vocal-stem timing (lesson 44). Free, runs inside Claude's workspace.
Usage: python3 vocal_timing.py <vocals.wav> [--repeat START LEN]...
1) prints sung phrases (50 ms RMS, gaps < 0.35 s merged, phrases >= 0.25 s)
2) for each --repeat START LEN, prints the top matches of that vocal passage elsewhere
   (chroma + MFCC of the vocal stem), which pins down repeated choruses / pre-choruses.
Make the stem first: audio-separator song.wav --model_filename UVR-MDX-NET-Voc_FT.onnx --output_format WAV
"""
import sys, subprocess, numpy as np

def phrases(path, gap=0.35, minlen=0.25):
    a = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                                     capture_output=True).stdout, np.int16).astype(float) / 32768
    hop = 400
    e = np.array([np.sqrt(np.mean(a[i*hop:(i+1)*hop]**2)) for i in range(len(a)//hop)])
    th = max(0.02, np.percentile(e, 40) * 1.2)
    segs, s = [], None
    for i, v in enumerate(e > th):
        if v and s is None: s = i
        if not v and s is not None: segs.append([s, i]); s = None
    if s is not None: segs.append([s, len(e)])
    m = []
    for sg in segs:
        if m and (sg[0] - m[-1][1]) * 0.05 < gap: m[-1][1] = sg[1]
        else: m.append(sg)
    return [(round(x[0]*0.05, 2), round(x[1]*0.05, 2)) for x in m if (x[1]-x[0])*0.05 >= minlen], len(a)/8000

def repeats(path, t0, L, top=5):
    import librosa
    y, sr = librosa.load(path, sr=22050, mono=True); hop = 512; fps = sr/hop
    F = np.vstack([librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=hop),
                   librosa.feature.mfcc(y=y, sr=sr, hop_length=hop, n_mfcc=13)[1:] / 50])
    ref = F[:, int(t0*fps):int((t0+L)*fps)]; n = ref.shape[1]; r = ref.flatten(); r = (r-r.mean())/r.std()
    out = []
    for s in np.arange(0, len(y)/sr - L, 0.1):
        w = F[:, int(s*fps):int(s*fps)+n]
        if w.shape[1] < n: break
        v = w.flatten(); v = (v-v.mean())/(v.std()+1e-9); out.append((s, float(np.dot(r, v)/len(r))))
    out = np.array(out); best = []
    for i in np.argsort(-out[:, 1]):
        if all(abs(out[i, 0]-t) > 4 for t, _ in best): best.append((round(out[i, 0], 1), round(out[i, 1], 3)))
        if len(best) == top: break
    return best

if __name__ == "__main__":
    p = sys.argv[1]; ph, dur = phrases(p)
    print(f"duration {dur:.2f} s, {len(ph)} phrases")
    for a, b in ph: print(f"{a}-{b}")
    args = sys.argv[2:]
    while args and args[0] == "--repeat":
        t0, L = float(args[1]), float(args[2]); args = args[3:]
        print(f"repeats of {t0}+{L}s:", repeats(p, t0, L))
```

### B.4 `align.py`

```python
#!/usr/bin/env python3
"""Line-level lyric alignment on the vocal stem (lesson 52). For one section: give its time window and its lines;
splits the sung phrases into len(lines) groups (monotonic DP) so each line's sung time matches its syllable count.
Usage: python3 align.py vocals.wav START END "line 1" "line 2" ...   -> prints start-end per line
Cross-check with Gemini on a 20-40 s window of the vocal stem, and always ear-check 3 moments with JD (gate T1)."""
import sys, re
exec(open(__file__.replace("align.py", "vocal_timing.py")).read().split("if __name__")[0])

def syl(s):
    w = re.findall(r"[a-zA-Zéèàù']+", s.lower()); n = 0
    for x in w:
        n += max(1, len(re.findall(r"[aeiouyéèàù]+", x)) - (1 if x.endswith("e") and len(x) > 3 else 0))
    return max(1, n)

def align(wav, t0, t1, lines, gap=0.2):
    ph, _ = phrases(wav, gap=gap, minlen=0.15)
    ph = [p for p in ph if p[1] > t0 and p[0] < t1]
    S = [syl(l) for l in lines]; L, P = len(lines), len(ph)
    tot = sum(b - a for a, b in ph); rate = tot / sum(S)
    INF = 1e18; best = [[INF] * (P + 1) for _ in range(L + 1)]; arg = [[0] * (P + 1) for _ in range(L + 1)]
    best[0][0] = 0
    for i in range(1, L + 1):
        for j in range(i, P + 1):
            for k in range(i - 1, j):
                if best[i - 1][k] == INF: continue
                d = sum(b - a for a, b in ph[k:j]); c = best[i - 1][k] + (d - rate * S[i - 1]) ** 2
                if c < best[i][j]: best[i][j] = c; arg[i][j] = k
    out, j = [], P
    for i in range(L, 0, -1):
        k = arg[i][j]; out.append((ph[k][0], ph[j - 1][1], lines[i - 1])); j = k
    return out[::-1]

if __name__ == "__main__":
    w, a, b = sys.argv[1], float(sys.argv[2]), float(sys.argv[3])
    for s, e, l in align(w, a, b, sys.argv[4:]): print(f"{s:6.2f}-{e:6.2f}  {l}")
```

### B.5 `chestcrop.py`

```python
#!/usr/bin/env python3
"""AI Video chest-up crop for Hedra (lesson 35). Finds the largest face and crops a 9:16 frame where the face
is ~22% of frame height and sits ~36% from the top, then resizes to 1080x1920.
Usage: python3 chestcrop.py in.jpg out.jpg [--force] [--box=x,y,w,h] [--face=0.22]   (skips if the face is already >= 18% of height)
"""
import sys, cv2

src, out = sys.argv[1], sys.argv[2]
force = "--force" in sys.argv
box = next((a.split("=")[1] for a in sys.argv if a.startswith("--box=")), None)
target = float(next((a.split("=")[1] for a in sys.argv if a.startswith("--face=")), 0.22))
im = cv2.imread(src); H, W = im.shape[:2]
g = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
cc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
fs = [tuple(map(int, box.split(",")))] if box else cc.detectMultiScale(g, 1.1, 6, minSize=(int(W * 0.06), int(W * 0.06)))
if len(fs) == 0 and not box:
    cc = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")
    fs = cc.detectMultiScale(g, 1.1, 5, minSize=(int(W * 0.06), int(W * 0.06)))
if len(fs) == 0:
    print("noface", src); cv2.imwrite(out, cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)); sys.exit(0)
x, y, w, h = max(fs, key=lambda f: f[2] * f[3])
ratio = h / H
if ratio >= 0.18 and not force:
    print(f"keep {ratio:.2f}", src); cv2.imwrite(out, cv2.resize(im, (1080, 1920), interpolation=cv2.INTER_LANCZOS4)); sys.exit(0)
ch = min(H, int(h / target)); cw = int(ch * 9 / 16)
if cw > W: cw = W; ch = int(cw * 16 / 9)
cx = x + w / 2; cy = y + h / 2
x0 = int(min(max(cx - cw / 2, 0), W - cw)); y0 = int(min(max(cy - ch * 0.36, 0), H - ch))
crop = im[y0:y0 + ch, x0:x0 + cw]
cv2.imwrite(out, cv2.resize(crop, (1080, 1920), interpolation=cv2.INTER_LANCZOS4), [cv2.IMWRITE_JPEG_QUALITY, 94])
print(f"crop {ratio:.2f} -> {cw}x{ch}", src)
```

### B.6 `make_manifest.py`

```python
#!/usr/bin/env python3
"""Build the assembly manifest: one row per scene with its window, its Hedra clip and its cutaway (Omni clip, else cutaway still).
Usage: python3 make_manifest.py <scenes.json> <clips_dir> <slug> <out_manifest.json>
Looks for  *-<slug>-SNN-Hedra.mp4,  *-<slug>-SNN-Omni.mp4,  *-<slug>-SNN-Cut-*.jpg  in clips_dir (newest file wins).
A scene may override with "hedra": "<file name>" / "cut": "<file name>" in scenes.json."""
import json, glob, os, sys
scenes, d, slug, out = sys.argv[1:5]
def pick(pat):
    g = [x for x in glob.glob(os.path.join(d, pat)) if "(1)" not in x]
    return max(g, key=os.path.getmtime) if g else None
man = []
for s in json.load(open(scenes)):
    sid = s["id"]
    hed = os.path.join(d, s["hedra"]) if s.get("hedra") else pick(f"*-{slug}-{sid}-Hedra.mp4")
    cut = os.path.join(d, s["cut"]) if s.get("cut") else (pick(f"*-{slug}-{sid}-Omni.mp4") or pick(f"*-{slug}-{sid}-Cut-*.jpg"))
    man.append({"id": sid, "start": float(s["start"]), "end": float(s["end"]), "hedra": hed, "cut": cut})
    print(f"{sid} {s['start']:>7}-{s['end']:<7} hedra={os.path.basename(hed or 'NONE')}  cut={os.path.basename(cut or 'NONE')}")
json.dump(man, open(out, "w"), indent=1)
```

### B.7 `assemble.py`

```python
#!/usr/bin/env python3
"""AI Video assembly (v2, intercut): trims each scene clip to its timed window, normalizes to 720x1280@30fps,
concatenates in order over the continuous full song, and overlays the end frame.

Usage: python3 assemble.py <scene_pack.md> <clips_dir> <song.mp3> <out.mp4> [logo.png]
Clip lookup per scene SNN: first match of *-SNN-Hedra.mp4, then *-SNN-Omni.mp4 in clips_dir
(override per scene with env PREFER_OMNI="S14,S15,...").
"""
import os, re, subprocess, sys, glob, json

pack, clips_dir, song, out = sys.argv[1:5]
logo = sys.argv[5] if len(sys.argv) > 5 else None
prefer_omni = set(filter(None, os.environ.get("PREFER_OMNI", "").split(",")))
def _map(name):
    return {k: float(v) for k, v in (x.split(":") for x in filter(None, os.environ.get(name, "").split(",")))}
OFFSETS = _map("OFFSETS")   # per-scene Omni start offset, e.g. "S11:0,S31:0"
SPLIT2 = _map("SPLIT2")     # short scenes: Hedra for first N s, then Omni, e.g. "S11:1.7"
def dur_of(f):
    if isinstance(f, Still): return 99.0
    return float(subprocess.run(["ffprobe","-v","error","-show_entries","format=duration","-of","csv=p=0",f],capture_output=True,text=True).stdout.strip() or 0)
MAN = {}
if os.environ.get("MANIFEST"):
    # manifest overrides scene windows and sources: [{"id","start","end","hedra":path,"cut":path(.mp4 Omni or .jpg still)}]
    _m = json.load(open(os.environ["MANIFEST"]))
    rows = [(m["id"], str(m["start"]), str(m["end"])) for m in _m]; MAN = {m["id"]: m for m in _m}
else:
    rows = re.findall(r'^\| (S\d\d) \| ([\d.]+)–([\d.]+) \|', open(pack).read(), re.M)
work = os.path.join(os.path.dirname(out) or ".", "_assembly")
os.makedirs(work, exist_ok=True)

def run(cmd):
    subprocess.run(cmd, check=True)

parts, report = [], []
INTERCUT = os.environ.get("INTERCUT", "1") == "1"
RW, RH = (1080, 1920) if os.environ.get("RES", "720") == "1080" else (720, 1280)
VF = f"scale={RW}:{RH}:force_original_aspect_ratio=increase,crop={RW}:{RH},fps=30,setsar=1"
STILLS = os.environ.get("STILL_DIR")  # fallback: Ken Burns cutaway from the cutaway still when no Omni clip

def find(sid, kind):
    pat = f"*{os.environ.get('SLUG', '')}*-{sid}-{kind}.mp4"  # SLUG keeps other runs' clips out (lesson 51)
    g = sorted(x for x in glob.glob(os.path.join(clips_dir, pat)) if sid.startswith("Cut-") or "-Cut-" not in os.path.basename(x))
    return g[0] if g else None

FPS = 30
def F(t):
    return int(round(t * FPS))

def kb(still, length, out):
    # "photo drop" (lesson 54): the cutaway still lands as a framed print over a blurred copy of itself,
    # spins in with a small overshoot, then drifts, so it reads as a deliberate photo, not a frozen video.
    from PIL import Image, ImageFilter, ImageOps
    import math
    n = F(length)
    src = Image.open(still).convert("RGB")
    bg = ImageOps.fit(src, (RW, RH)).filter(ImageFilter.GaussianBlur(RW // 40))
    bg = Image.blend(bg, Image.new("RGB", (RW, RH), (15, 15, 20)), 0.45)
    cw = int(RW * 0.78); ph = ImageOps.fit(src, (cw, int(cw * 16 / 9 * 0.82)))
    b = int(RW * 0.025)
    card = Image.new("RGBA", (ph.width + 2 * b, ph.height + int(b * 3.2)), (246, 238, 220, 255))
    card.paste(ph, (b, b))
    sh = Image.new("RGBA", card.size, (0, 0, 0, 150)).filter(ImageFilter.GaussianBlur(8))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{RW}x{RH}", "-r", "30",
                          "-i", "-", "-frames:v", str(n), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    def back(t):  # ease-out-back
        c1 = 1.70158; c3 = c1 + 1; t -= 1
        return 1 + c3 * t ** 3 + c1 * t ** 2
    for i in range(n):
        t = i / 30.0
        if t < 0.33:
            k = back(min(1, t / 0.33)); ang = -16 + 13 * k; sc = 1.25 - 0.25 * k; yo = -RH * 0.08 * (1 - k)
        else:
            d = t - 0.33; ang = -3 + 1.2 * d; sc = 1.0 + 0.012 * d; yo = 0
        c = card.resize((int(card.width * sc), int(card.height * sc)))
        s_ = sh.resize(c.size)
        c = c.rotate(ang, expand=True, resample=Image.BICUBIC); s_ = s_.rotate(ang, expand=True)
        fr = bg.copy()
        x = (RW - c.width) // 2; y = int((RH - c.height) // 2 + yo)
        fr.paste(s_, (x + 12, y + 18), s_); fr.paste(c, (x, y), c)
        p.stdin.write(fr.tobytes())
    p.stdin.close(); p.wait()

class Still(str):
    pass

def cut(src, start, length, out):
    if isinstance(src, Still):
        return kb(src, length, out)
    # piece of src from `start` for exactly F(length) frames (frame-exact: no cumulative A/V drift),
    # normalized, last frame held if src is short
    n = F(length)
    run(["ffmpeg", "-v", "error", "-y", "-ss", f"{start:.3f}", "-i", src,
         "-vf", VF + f",tpad=stop_mode=clone:stop_duration={length + 1:.3f}", "-frames:v", str(n), "-an",
         "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", out])

for sid, a, b in rows:
    dur = round((F(float(b)) - F(float(a))) / FPS, 4)  # frame-exact scene length on the absolute song clock
    hed = find(sid, "Hedra")
    omni = find(f"Cut-{sid}", "Omni") or find(sid, "Omni")  # cutaway clip preferred
    if sid in MAN:
        hed = MAN[sid].get("hedra"); c = MAN[sid].get("cut")
        omni = (Still(c) if c and c.endswith(".jpg") else c) if c else None
    if not omni and STILLS:
        g = sorted(x for x in glob.glob(os.path.join(STILLS, f"*{os.environ.get('SLUG', '')}*-{sid}-Cut-*.jpg")) if "(1)" not in x)
        if g: omni = Still(g[0])
    seg = os.path.join(work, f"{sid}.mp4")
    if sid in prefer_omni and omni: hed = None
    off = OFFSETS.get(sid, float(os.environ.get("OMNI_OFFSET", "1.0")))
    if INTERCUT and hed and omni and sid in SPLIT2:
        h1 = F(SPLIT2[sid]) / FPS; om = round(dur - h1, 4); off = max(0, min(off, dur_of(omni) - om))
        p = [os.path.join(work, f"{sid}_{i}.mp4") for i in range(2)]
        cut(hed, 0, h1, p[0]); cut(omni, off, om, p[1])
        l = os.path.join(work, f"{sid}_list.txt"); open(l, "w").write("".join(f"file '{x}'\n" for x in p))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", l, "-c", "copy", seg])
        report.append({"scene": sid, "source": f"Hedra 0-{h1}s | Omni {om}s from {off}s", "dur": dur})
    elif INTERCUT and hed and omni and dur >= 4.5:
        # Hedra (singing, in sync) -> Omni story beat -> Hedra (back in sync)
        # Hedra keeps the majority so lip-sync dominates; cutaway is a short story beat
        h1 = F(min(3.0, dur * 0.4)) / FPS; om = F(min(float(os.environ.get("CUT_MAX", "3.0")), dur * 0.35)) / FPS; h2 = round(dur - h1 - om, 4)
        p = [os.path.join(work, f"{sid}_{i}.mp4") for i in range(3)]
        cut(hed, 0, h1, p[0])
        off = max(0, min(off, dur_of(omni) - om))
        cut(omni, off, om, p[1])
        cut(hed, h1 + om, h2, p[2])
        l = os.path.join(work, f"{sid}_list.txt"); open(l, "w").write("".join(f"file '{x}'\n" for x in p))
        run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", l, "-c", "copy", seg])
        report.append({"scene": sid, "source": f"Hedra 0-{h1}s | Omni {om}s | Hedra last {h2}s", "dur": dur})
    elif hed or omni:
        src = hed or omni
        cut(src, 0, dur, seg)
        report.append({"scene": sid, "source": os.path.basename(src), "dur": dur})
    else:
        run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", f"color=c=black:s={RW}x{RH}:r=30:d={dur}",
             "-frames:v", str(F(dur)), "-c:v", "libx264", "-preset", "veryfast", "-pix_fmt", "yuv420p", seg])
        report.append({"scene": sid, "source": "MISSING (black)", "dur": dur})
    parts.append(seg)

lst = os.path.join(work, "list.txt")
open(lst, "w").write("".join(f"file '{p}'\n" for p in parts))
silent = os.path.join(work, "video_silent.mp4")
run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", silent])

total = sum(r["dur"] for r in report)
END = float(os.environ.get("END_CARD_SEC", "3.0"))
end_start = max(0, total - END)
en = f"enable='gte(t,{end_start})'"
txt = "Created by Tableland Partners"
# end card: darken the last END seconds, centered logo, credit line underneath
scrim = f"drawbox=x=0:y=0:w=iw:h=ih:color=black@0.72:t=fill:{en}"
draw = "null"  # title + credit are kinetic.py text (lesson 56); the end card here is scrim + logo only
inputs = ["-i", silent, "-i", song]
if logo:
    inputs += ["-loop", "1", "-i", logo]
    fc = (f"[0:v]{scrim}[d];[2:v]scale={int(RW*0.5)}:-1,format=rgba[lg];"
          f"[d][lg]overlay=(W-w)/2:H*0.70:shortest=1:{en}[v1];[v1]{draw}[v]")
else:
    fc = f"[0:v]{scrim},{draw}[v]"
run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[v]", "-map", "1:a",
     "-t", str(total), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p",
     "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", out])
json.dump({"total_sec": total, "scenes": report}, open(out + ".report.json", "w"), indent=1)
print(json.dumps({"total_sec": total, "missing": [r["scene"] for r in report if r["source"].startswith("MISSING")]}))
```

### B.8 `kinetic.py`

```python
#!/usr/bin/env python3
"""AI Video kinetic typography (lessons 55-56, Grok research 10-28). Builds an ASS file of animated text and burns it in.
Usage: python3 kinetic.py <in.mp4> <text.json> <out.mp4> [song.mp3 for beat snap]
text.json items: {"t0": s, "t1": s, "style": STYLE, "big": "...", "small": "..."}
STYLE: stamp   - hook/stat: Anton, slams in from 170% with -5deg, overshoot, settles (8 frames)
       sub     - translation under a stamp: Pacifico in accent, mask-wipe reveal left to right (12 frames)
       stat    - number in accent (stamp) + descriptor in Oswald typed on word by word
       check   - checklist item: accent tick pops (6 frames) then text slides in; items stack and stay until "until"
       write   - sincere line: Pacifico typed letter by letter (2 frames/letter), soft settle
       title   - end-card title: stacked Anton lines stamping in one by one + small credit
Design rules: one accent colour, cream type with black outline + soft shadow, safe zone y 1150-1480 of 1920
(clear of the mouth, top UI and bottom captions), hold >= 0.5 s after landing, exits in 6 frames.
"""
import json, sys, os, subprocess

FONTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")
CREAM, INK, ACCENT = "&H00DCEEF6", "&H00141414", "&H0030C4F4"   # ASS is &HAABBGGRR: cream F6EEDC, accent mustard F4C430
W, H = 1080, 1920

def ts(t):
    t = max(0, t); h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

def beats(song):
    try:
        import librosa
        y, sr = librosa.load(song, sr=22050, mono=True)
        _, b = librosa.beat.beat_track(y=y, sr=sr)
        return list(librosa.frames_to_time(b, sr=sr))
    except Exception:
        return []

def snap(t, bt, win=0.18):
    if not bt: return t
    b = min(bt, key=lambda x: abs(x - t))
    return b if abs(b - t) <= win else t

HEAD = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {W}
PlayResY: {H}
WrapStyle: 2
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Hook,Anton,200,{CREAM},{CREAM},{INK},&H96000000,0,0,0,0,100,100,2,0,1,6,5,5,60,60,0,1
Style: Stat,Anton,260,{ACCENT},{ACCENT},{INK},&H96000000,0,0,0,0,100,100,1,0,1,6,5,5,60,60,0,1
Style: Desc,Oswald,96,{CREAM},{CREAM},{INK},&H96000000,1,0,0,0,100,100,1,0,1,4,3,5,60,60,0,1
Style: Script,Pacifico,120,{ACCENT},{ACCENT},{INK},&H96000000,0,0,0,0,100,100,0,0,1,4,3,5,60,60,0,1
Style: Check,Oswald,92,{CREAM},{CREAM},{INK},&H96000000,1,0,0,0,100,100,1,0,1,4,3,4,60,60,0,1
Style: Tick,Anton,104,{ACCENT},{ACCENT},{INK},&H96000000,0,0,0,0,100,100,0,0,1,4,3,5,60,60,0,1
Style: Title,Anton,150,{CREAM},{CREAM},{INK},&H96000000,0,0,0,0,100,100,3,0,1,6,6,5,60,60,0,1
Style: Credit,Oswald,46,{CREAM},{CREAM},{INK},&H96000000,0,0,0,0,100,100,2,0,1,3,2,5,60,60,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""

def ev(t0, t1, style, text, layer=0):
    return f"Dialogue: {layer},{ts(t0)},{ts(t1)},{style},,0,0,0,,{text}\n"

def fit(text, base, per_char):
    # shrink long lines so they stay inside ~900 px
    return min(base, int(900 / max(1, len(text) * per_char)))

def stamp(t0, t1, text, y, style="Hook", base=200):
    fs = fit(text, base, 0.36)
    d = int((t1 - t0) * 1000)
    tag = (f"{{\\an5\\pos({W//2},{y})\\fs{fs}\\fscx175\\fscy175\\frz-5\\alpha&HFF&"
           f"\\t(0,60,\\alpha&H00&)\\t(0,200,0.6,\\fscx106\\fscy94\\frz0)\\t(200,300,\\fscx100\\fscy100)"
           f"\\t({d-200},{d},\\fscx70\\fscy70\\alpha&HFF&)}}")
    return ev(t0, t1, style, tag + text, 2)

def wipe(t0, t1, text, y, style="Script", base=120, delay=0.25):
    fs = fit(text, base, 0.42); d = int((t1 - t0) * 1000); s = int(delay * 1000)
    tag = (f"{{\\an5\\pos({W//2},{y})\\fs{fs}\\clip(0,0,0,{H})\\t({s},{s+420},0.5,\\clip(0,0,{W},{H}))"
           f"\\t({d-200},{d},\\alpha&HFF&)}}")
    return ev(t0, t1, style, tag + text, 1)

def typed(t0, t1, text, y, style="Desc", base=96, per=0.07, words=True, delay=0.2):
    fs = fit(text, base, 0.42); d = int((t1 - t0) * 1000)
    parts = text.split(" ") if words else list(text)
    out = f"{{\\an5\\pos({W//2},{y})\\fs{fs}\\t({d-200},{d},\\alpha&HFF&)}}"
    for i, p in enumerate(parts):
        a = int((delay + i * per) * 1000)
        sep = " " if words and i < len(parts) - 1 else ""
        out += f"{{\\alpha&HFF&\\t({a},{a+70},\\alpha&H00&)}}{p}{sep}"
    return ev(t0, t1, style, out, 1)

def build(items, bt):
    out = HEAD
    for o in items:
        st = o.get("style", "stamp"); t0 = snap(float(o["t0"]), bt) if st != "check" else float(o["t0"]); t1 = float(o["t1"])
        if st == "stamp":
            out += stamp(t0, t1, o["big"], 1280)
            if o.get("small"): out += wipe(t0, t1, o["small"], 1440)
        elif st == "stat":
            out += stamp(t0, t1, o["big"], 1250, "Stat", 260)
            if o.get("small"): out += typed(t0, t1, o["small"], 1440, delay=0.3)
        elif st == "check":
            y = 1020 + 112 * int(o.get("row", 0)); until = float(o.get("until", t1))
            out += ev(t0, until, "Tick", f"{{\\an5\\pos(150,{y})\\fscx0\\fscy0\\t(0,120,0.6,\\fscx125\\fscy125)\\t(120,200,\\fscx100\\fscy100)\\t({int((until-t0)*1000)-200},{int((until-t0)*1000)},\\alpha&HFF&)}}✓", 2)
            out += ev(t0, until, "Check", f"{{\\an4\\move(250,{y},200,{y},80,320)\\alpha&HFF&\\t(80,260,\\alpha&H00&)\\t({int((until-t0)*1000)-200},{int((until-t0)*1000)},\\alpha&HFF&)}}{o['big']}", 1)
        elif st == "write":
            out += typed(t0, t1, o["big"], int(o.get("y", 1320)), "Script", 100, per=0.045, words=False, delay=0.05)
        elif st == "title":
            lines = o["big"].split("|"); y0 = int(o.get("y", 560)); fs = int(o.get("size", 220)); gap = int(fs * 0.95)
            for i, l in enumerate(lines):
                out += stamp(t0 + 0.25 * i, t1, l, y0 + gap * i, "Title", fs)
            if o.get("small"): out += wipe(t0, t1, o["small"], int(o.get("small_y", 1560)), o.get("small_style", "Credit"), 54 if o.get("small_style", "Credit") == "Credit" else 96, delay=0.25 * len(lines) + 0.2)
    return out

if __name__ == "__main__":
    src, spec, out = sys.argv[1:4]
    song = sys.argv[4] if len(sys.argv) > 4 else None
    items = json.load(open(spec))
    ass = os.path.splitext(out)[0] + ".ass"
    open(ass, "w").write(build(items, beats(song) if song else []))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-vf", f"ass={ass}:fontsdir={FONTS}", "-c:v", "libx264",
                    "-preset", "veryfast", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "copy", "-movflags", "+faststart", out], check=True)
    print("ok", len(items), "text items ->", out)
```

### B.9 `audit.py`

```python
#!/usr/bin/env python3
"""Lyric <-> visual audit sheet: two frames per scene (25% and 55% into its window) captioned with scene, window and lyric.
Usage: python3 audit.py <final.mp4> <manifest.json> <scenes.json> <out.jpg>"""
import json, subprocess, sys, io
from PIL import Image, ImageDraw, ImageFont
vid, manf, scf, out = sys.argv[1:5]
man = json.load(open(manf)); lyr = {s["id"]: s.get("lyric", "") for s in json.load(open(scf))}
try: font = ImageFont.truetype(__file__.rsplit("/", 1)[0] + "/fonts/Oswald_700Bold.ttf", 15)
except Exception: font = ImageFont.load_default()
W, H, COLS = 216, 384, 8; rows = (len(man) + COLS - 1) // COLS
im = Image.new("RGB", (COLS * W, rows * (H + 44)), "white"); d = ImageDraw.Draw(im)
for k, m in enumerate(man):
    a, b = float(m["start"]), float(m["end"]); x = (k % COLS) * W; y = (k // COLS) * (H + 44)
    for j, t in enumerate((a + 0.25 * (b - a), a + 0.55 * (b - a))):
        p = subprocess.run(["ffmpeg", "-v", "error", "-ss", f"{t:.2f}", "-i", vid, "-frames:v", "1", "-vf", f"scale={W//2}:{H//2}",
                            "-f", "image2pipe", "-vcodec", "png", "-"], capture_output=True).stdout
        im.paste(Image.open(io.BytesIO(p)), (x + j * W // 2, y + 44))
    d.text((x + 3, y + 2), f"{m['id']} {a:.1f}-{b:.1f}", fill="black", font=font)
    d.text((x + 3, y + 21), lyr.get(m["id"], "")[:30], fill="#D9692F", font=font)
im.save(out, quality=85); print("ok", out)
```

---

*End of guide. Operator: keep this file updated. Add every new failure and fix to section 11, and note the date at the top.*
