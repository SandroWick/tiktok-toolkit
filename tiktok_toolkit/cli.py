import typer
from tiktok_toolkit import scrape, scrape_comments, transcribe

app = typer.Typer(help="📦 TikTok Toolkit: Scrape, Transcribe, Analyze")


@app.command("scrape-videos")
def scrape_videos(
    input_csv: str = typer.Argument(..., help="CSV-Datei mit TikTok-Links"),
    output_dir: str = typer.Option("downloads/", help="Zielordner für Downloads"),
    start_index: int = typer.Option(
        0, help="Startindex (z. B. um Scraping fortzusetzen)"
    ),
):
    """🎥 Scraped Videos aus einer CSV-Liste."""
    video_ids = scrape.extract_video_ids_from_csv(input_csv)
    typer.echo(f"📄 {len(video_ids)} Video-IDs in der CSV-Datei gefunden.")

    existing_ids = scrape.get_downloaded_ids(output_dir)
    remaining_ids = [vid for vid in video_ids[start_index:] if vid not in existing_ids]

    typer.echo(
        f"🧹 {len(existing_ids)} bereits vorhanden, {len(remaining_ids)} werden neu gescraped."
    )

    if not remaining_ids:
        typer.echo("✅ Keine neuen Videos zum Scrapen.")
        raise typer.Exit()

    scrape.scrape_video_list(remaining_ids, output_dir, start_index=0)


@app.command("scrape-user")
def scrape_user(
    username: str = typer.Argument(..., help="TikTok-Benutzername"),
    output_dir: str = typer.Option("downloads/", help="Zielordner für Downloads"),
):
    """👤 Scraped das komplette TikTok-Profil eines Users."""
    scrape.scrape_user_profile(username, output_dir)


@app.command("scrape-comments")
def scrape_comments_cmd(
    input_csv: str = typer.Option(None, help="CSV-Datei mit TikTok-Links"),
    from_output_dir: str = typer.Option(
        None, help="Ordner mit heruntergeladenen Videos zur ID-Extraktion"
    ),
    output_dir: str = typer.Option("comments/", help="Zielordner für Kommentare"),
    start_index: int = typer.Option(0, help="Startindex für Kommentar-Scraping"),
):
    """💬 Scraped Kommentare zu einer Liste von Videos."""
    if input_csv:
        video_ids = scrape_comments.extract_video_ids_from_csv(input_csv)
        typer.echo(f"✅ {len(video_ids)} Video-IDs aus CSV extrahiert.")
    elif from_output_dir:
        video_ids = sorted(scrape_comments.get_downloaded_ids(from_output_dir))
        typer.echo(f"📁 {len(video_ids)} Video-IDs aus Ordner extrahiert.")
    else:
        typer.echo("❌ Bitte entweder --input-csv oder --from-output-dir angeben.")
        raise typer.Exit(code=1)

    scrape_comments.scrape_comments_batch(video_ids, output_dir, start_index)


@app.command("transcribe")
def transcribe_cmd(
    input_dir: str = typer.Argument(..., help="Verzeichnis mit MP4-Dateien"),
    output_dir: str = typer.Option(
        "transcripts/", help="Zielverzeichnis für Transkripte"
    ),
    model_size: str = typer.Option("medium", help="Whisper-Modellgröße"),
    device: str = typer.Option("cpu", help="Gerätetyp: cpu oder cuda"),
    keep_temp: bool = typer.Option(False, help="Temporäre WAV-Dateien behalten"),
):
    """📝 Transkribiert alle MP4-Dateien in einem Verzeichnis."""
    transcribe.transcribe_folder(
        input_dir=input_dir,
        output_dir=output_dir,
        model_size=model_size,
        device=device,
        delete_temp=not keep_temp,
    )


if __name__ == "__main__":
    app()
