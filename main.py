from dotenv import load_dotenv

from src.agents.podcast_agent import PodcastAgent


def main():
    # Load environment variables
    load_dotenv()

    # Create and run agent
    agent = PodcastAgent()

    # Generate podcast for OutOfTheLoop subreddit
    result = agent.workflow.invoke({"subreddit": "OutOfTheLoop"})

    print(f"✨ Podcast generated successfully!")
    print(f"📝 Script: {result['final_script'][:500]}...")
    print(f"🎧 Audio saved to: {result['audio_path']}")


if __name__ == "__main__":
    main()
