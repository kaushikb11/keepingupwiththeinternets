import datetime
import os
import re
from dataclasses import dataclass
from typing import List, Optional, Tuple

import azure.cognitiveservices.speech as speechsdk
from pydub import AudioSegment


@dataclass
class SpeakerConfig:
    voice_name: str
    style: str = "chat"
    style_degree: float = 1.0


SPEAKER_CONFIGS = {
    "Host": SpeakerConfig(voice_name="en-US-JasonNeural", style="chat"),
    "Learner": SpeakerConfig(voice_name="en-US-JennyNeural", style="friendly"),
    "Expert": SpeakerConfig(voice_name="en-US-GuyNeural", style="professional"),
}


class PodcastGenerator:
    def __init__(self, base_dir: Optional[str] = "./podcasts"):
        self.base_dir = base_dir
        os.makedirs(base_dir, exist_ok=True)

    def _generate_audio(self, text: str, speaker: str, output_path: str) -> str:
        """Generate audio for a single piece of dialogue."""
        wav_path = output_path.replace(".mp3", ".wav")

        speech_config = speechsdk.SpeechConfig(
            subscription=os.getenv("AZURE_SPEECH_KEY"),
            region=os.getenv("AZURE_SPEECH_REGION"),
        )

        config = SPEAKER_CONFIGS[speaker]
        speech_config.speech_synthesis_voice_name = config.voice_name

        # Create audio config with WAV format
        audio_config = speechsdk.AudioConfig(filename=wav_path)

        synthesizer = speechsdk.SpeechSynthesizer(
            speech_config=speech_config, audio_config=audio_config
        )

        # Generate audio
        result = synthesizer.speak_text(text)

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            # Convert WAV to MP3 using pydub
            if os.path.exists(wav_path):
                audio = AudioSegment.from_wav(wav_path)
                audio.export(output_path, format="mp3", bitrate="192k")
                # Clean up WAV file
                os.remove(wav_path)
                return output_path
        else:
            print(f"Failed with reason: {result.reason}")
            raise Exception(f"Speech synthesis failed with reason: {result.reason}")

    def _generate_audio_batch(self, segments: List[Tuple[str, str, int]]) -> List[str]:
        """Generate audio files sequentially."""
        audio_files = []

        for idx, (speaker, text, timestamp) in enumerate(segments):
            # Clean the text
            text = text.strip()
            if not text:
                print(f"Skipping empty text for {speaker}")
                continue

            # Use the unique timestamp in the filename
            output_path = f"{self.output_dir}/{speaker.lower()}_{timestamp:013d}.mp3"
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            try:
                print(f"\nGenerating audio {idx + 1}/{len(segments)} for {speaker}:")
                print(f"Text: {text[:100]}...")
                result = self._generate_audio(text, speaker, output_path)
                audio_files.append(result)
                print(f"✓ Generated: {os.path.basename(output_path)}")
            except Exception as e:
                print(f"Failed to generate audio for {speaker}: {e}")
                raise

        return audio_files

    def _merge_audio_files(self, audio_files: List[str], output_file: str) -> str:
        """Merge audio files with crossfade."""
        print(f"\nStarting merge of {len(audio_files)} files...")

        if not audio_files:
            raise Exception("No audio files to merge")

        merged = AudioSegment.empty()
        sorted_files = sorted(
            audio_files, key=lambda x: int(re.search(r"_(\d{13})", x).group(1))
        )

        print("\nProcessing files in order:")
        for idx, file in enumerate(sorted_files):
            print(f"Processing {idx + 1}/{len(sorted_files)}: {os.path.basename(file)}")
            if not os.path.exists(file):
                print(f"Warning: File does not exist: {file}")
                continue

            try:
                audio = AudioSegment.from_mp3(file)
                print(f"Loaded audio segment, duration: {len(audio)}ms")

                if len(merged) > 0:
                    # Add small pause between segments
                    silence = AudioSegment.silent(duration=500)  # 500ms pause
                    merged = merged + silence + audio
                else:
                    merged = audio
            except Exception as e:
                print(f"Error processing {file}: {e}")
                raise

        print(f"\nExporting final audio to: {output_file}")
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

        merged.export(
            output_file,
            format="mp3",
            bitrate="192k",
            parameters=["-acodec", "libmp3lame", "-q:a", "2"],
        )

        if os.path.exists(output_file):
            size_mb = os.path.getsize(output_file) / (1024 * 1024)
            duration_sec = len(merged) / 1000
            print(f"Successfully created merged file:")
            print(f"- Path: {output_file}")
            print(f"- Size: {size_mb:.2f}MB")
            print(f"- Duration: {duration_sec:.1f} seconds")
        else:
            raise Exception(f"Failed to create merged file: {output_file}")

        return output_file

    def generate_podcast(self, script: str) -> str:
        """Main method to generate podcast from script."""
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        self.output_dir = f"{self.base_dir}/podcast_{timestamp}"
        os.makedirs(self.output_dir, exist_ok=True)

        segments = []
        matches = re.findall(
            r"(Host|Learner|Expert):\s*(.*?)(?=(Host|Learner|Expert|$))",
            script,
            re.DOTALL,
        )

        # Create segments with unique timestamps for each dialogue
        for idx, (speaker, text, _) in enumerate(matches):
            # Use combination of base timestamp and index for unique ordering
            segment_timestamp = int(datetime.datetime.now().timestamp() * 1000) + idx
            segments.append((speaker, text.strip(), segment_timestamp))
            print(f"Added segment {idx + 1}: {speaker} - {text[:50]}...")

        print(f"\nFound {len(segments)} dialogue segments")

        audio_files = self._generate_audio_batch(segments)

        output_file = (
            f"{self.output_dir}/podcast_{int(datetime.datetime.now().timestamp())}.mp3"
        )
        return self._merge_audio_files(audio_files, output_file)
