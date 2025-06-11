# 🎬 TikTok Toolkit

Ein CLI-Tool zum **Scrapen, Transkribieren und Kommentaranalysieren** von TikTok-Videos. Entwickelt für Forschungs- und Analysezwecke (z. B. Medien- oder Diskursanalysen).

---

## 🔧 Installation

### 1. Projekt klonen

```bash
git clone <dein-repo-url> tiktok_toolkit
cd tiktok_toolkit
```

2. Virtuelle Umgebung einrichten

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Abhängigkeiten installieren

```bash
pip install -e .
```

4. Externe Module klonen

🔹 TikTokComment-Scraper

```bash
git clone https://github.com/romysaputrasihananda/tiktok-comment-scrapper.git extern/tiktokcomment
```

🔹 TikTok Video Scraper

```bash
git clone https://github.com/Q-Bukold/TikTok-Content-Scraper.git extern/TT_Scraper
```

Beide Module werden automatisch über sys.path eingebunden – keine Installation via pip notwendig.

⸻

🚀 CLI-Befehle

Nach der Installation steht dir der CLI-Befehl tiktok zur Verfügung:

```bash
tiktok --help
```

🎥 Scrape einzelne Videos aus CSV

```bash
tiktok scrape-videos test_links.csv --output-dir downloads/
```

	•	CSV-Format: Jede Zeile enthält eine TikTok-Video-URL.

⸻

👤 Scrape gesamtes Profil

```bash
tiktok scrape-user maximilianpuetzofficial --output-dir downloads/
```

⸻

💬 Kommentare scrapen

```bash
tiktok scrape-comments test_links.csv --output-dir comments/
```

⸻

📝 Transkription aller MP4s im Ordner

```bash
tiktok transcribe downloads/ --output-dir transcripts/
```

Optionen:
	•	--device cuda für GPU
	•	--model-size large für größeres Whisper-Modell

⸻

📁 Projektstruktur

```bash
tiktok_toolkit/
├── tiktok_toolkit/
│   ├── cli.py
│   ├── scrape.py
│   ├── scrape_comments.py
│   ├── transcribe.py
│   └── __init__.py
├── extern/
│   ├── tiktokcomment/
│   └── TT_Scraper/
├── pyproject.toml
├── README.md
```

⸻

🧩 Abhängigkeiten
	•	typer
	•	pandas
	•	faster-whisper
	•	beautifulsoup4
	•	loguru
