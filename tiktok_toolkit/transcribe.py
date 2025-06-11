from faster_whisper import WhisperModel
from pathlib import Path
import subprocess


def format_timestamp(seconds: float) -> str:
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds - int(seconds)) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


def transcribe_folder(
    input_dir: str,
    output_dir: str = "transcripts/",
    model_size: str = "medium",
    device: str = "cpu",  # "cuda" für GPU
    delete_temp: bool = True,
):
    """Transkribiert alle MP4-Dateien in einem Verzeichnis."""
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)

    video_files = sorted(input_path.glob("*.mp4"))
    if not video_files:
        print("❌ Keine MP4-Dateien gefunden.")
        return

    model = WhisperModel(model_size, compute_type="int8", device=device)

    for video_file in video_files:
        txt_file = output_path / f"{video_file.stem}_transcript.txt"
        srt_file = output_path / f"{video_file.stem}_transcript.srt"

        print(f"\n🎬 Transkribiere: {video_file.name}")
        if txt_file.exists() and srt_file.exists():
            print(f"⏭️  Überspringe {video_file.name}, Transkript existiert bereits.")
            continue

        wav_file = video_file.with_suffix(".wav")
        result = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(video_file),
                "-ar",
                "16000",
                "-ac",
                "1",
                str(wav_file),
            ],
            capture_output=True,
            text=True,
        )

        if result.returncode != 0:
            print(f"❌ ffmpeg-Fehler bei {video_file.name}:\n{result.stderr}")
            continue

        segments, _ = model.transcribe(str(wav_file), language="de")

        # TXT speichern
        with open(txt_file, "w", encoding="utf-8") as f_txt:
            for segment in segments:
                f_txt.write(segment.text.strip() + "\n")

        print(f"📝 Transkript gespeichert in: {txt_file}")

        # SRT speichern
        with open(srt_file, "w", encoding="utf-8") as f_srt:
            for i, segment in enumerate(segments, start=1):
                start = format_timestamp(segment.start)
                end = format_timestamp(segment.end)
                text = segment.text.strip()
                f_srt.write(f"{i}\n{start} --> {end}\n{text}\n\n")

        print(f"⏱️  SRT-Datei gespeichert in: {srt_file}")

        if delete_temp:
            wav_file.unlink()

    print("\n✅ Alle Videos verarbeitet.")
