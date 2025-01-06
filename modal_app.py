from datetime import datetime

import modal

app = modal.App("keepingupwithinternets")
volume = modal.Volume.from_name("podcast-storage", create_if_missing=True)


def get_keepingupwithinternets_mount():
    return [modal.Mount.from_local_dir("src", remote_path="/root/src")]


image = (
    modal.Image.debian_slim()
    .pip_install(
        "praw",
        "openai",
        "python-dotenv",
        "firecrawl-py",
        "elevenlabs",
        "azure-cognitiveservices-speech",
        "pydub",
        "langchain-openai",
        "langgraph",
    )
    .apt_install(["ffmpeg"])
)


@app.function(
    image=image,
    volumes={"/podcasts": volume},
    secrets=[modal.Secret.from_name("keepingupwiththeinternets-secrets")],
    mounts=get_keepingupwithinternets_mount(),
)
def generate_podcast():
    import sys

    sys.path.append("/root")

    from src.agents.podcast_agent import PodcastAgent

    print(f"Starting podcast generation at {datetime.now()}")

    agent = PodcastAgent(tts_service="azure", base_dir="/podcasts")

    result = agent.run("OutOfTheLoop")

    print("✨ Podcast generated successfully!")
    print(f"📝 Script: {result['final_script'][:500]}...")
    print(f"🎧 Audio saved to: {result['audio_path']}")


@app.function(schedule=modal.Period(days=7))
def scheduled_podcast():
    return generate_podcast.remote()
