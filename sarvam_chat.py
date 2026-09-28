import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from sarvamai import SarvamAI

# Load API key
for line in Path(".env").read_text().splitlines():
    name, sep, value = line.partition("=")
    if sep and name.strip() == "SARVAM_API_KEY":
        os.environ["SARVAM_API_KEY"] = value.strip().strip("\"'")

api_key = os.getenv("SARVAM_API_KEY")
if not api_key:
    raise RuntimeError("SARVAM_API_KEY not found in .env")

client = SarvamAI(api_subscription_key=api_key)

extensions = {
    ".aac", ".aiff", ".amr", ".flac", ".m4a",
    ".mp3", ".ogg", ".opus", ".wav", ".webm", ".wma"
}

output_dir = Path("output text")
output_dir.mkdir(exist_ok=True)

files = [
    p for p in Path(".").iterdir()
    if p.is_file() and p.suffix.lower() in extensions
]

def transcribe(path):
    try:
        with path.open("rb") as f:
            result = client.speech_to_text.transcribe(
                file=f,
                model="saaras:v3",
                mode="transcribe"
            )

        out = output_dir / f"{path.stem}.txt"
        out.write_text(result.transcript, encoding="utf-8")
        return f"✓ {path.name}"

    except Exception as e:
        return f"✗ {path.name}: {e}"

with ThreadPoolExecutor(max_workers=5) as pool:
    jobs = [pool.submit(transcribe, f) for f in files]

    for job in as_completed(jobs):
        print(job.result())

print("Done.")







 