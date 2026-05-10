#!/usr/bin/env python3
"""
ElevenLabs Batch Voice Changer

Purpose:
- Accepts audio/video input such as WAV, MP3, MP4.
- Extracts audio when needed.
- Splits audio into safe chunks under ElevenLabs' 5-minute web workflow limit.
- Sends each chunk to ElevenLabs Voice Changer / Speech-to-Speech API.
- Merges converted chunks.
- Applies final mastering using FFmpeg loudness normalization and peak limiting.

Requires:
- Python 3.9+
- FFmpeg installed and available on PATH
- ELEVENLABS_API_KEY environment variable

PowerShell example:
  $env:ELEVENLABS_API_KEY="your_api_key_here"
  python elevenlabs_batch_voice_changer.py --input "tutorial.mp4" --voice-id "YOUR_VOICE_ID" --output "tutorial_final.mp3"
"""

import argparse
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


ELEVENLABS_STS_URL = "https://api.elevenlabs.io/v1/speech-to-speech/{voice_id}"
DEFAULT_MODEL_ID = "eleven_multilingual_sts_v2"
DEFAULT_CHUNK_SECONDS = 270
DEFAULT_OUTPUT_FORMAT = "mp3_44100_128"


class WorkflowError(Exception):
    """Raised for user-facing workflow errors."""


def run_command(command, description):
    """Run a command and raise a clean error if it fails."""
    try:
        result = subprocess.run(
            command,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True,
        )
        return result
    except FileNotFoundError:
        raise WorkflowError(
            "FFmpeg/FFprobe was not found. Install FFmpeg and make sure ffmpeg.exe and ffprobe.exe are available on PATH."
        )
    except subprocess.CalledProcessError as exc:
        message = exc.stderr.strip() or exc.stdout.strip() or "Unknown FFmpeg error"
        raise WorkflowError(f"Failed during: {description}\n{message}")


def ensure_tool_exists(tool_name):
    if shutil.which(tool_name) is None:
        raise WorkflowError(
            f"{tool_name} was not found on PATH. Install FFmpeg and restart your terminal/VS Code."
        )


def ensure_prerequisites(input_path):
    ensure_tool_exists("ffmpeg")
    ensure_tool_exists("ffprobe")

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise WorkflowError(
            "ELEVENLABS_API_KEY environment variable is missing. In PowerShell, run:\n"
            "$env:ELEVENLABS_API_KEY=\"your_api_key_here\""
        )

    if not input_path.exists():
        raise WorkflowError(f"Input file does not exist: {input_path}")

    return api_key


def get_duration_seconds(media_path):
    command = [
        "ffprobe",
        "-v",
        "error",
        "-show_entries",
        "format=duration",
        "-of",
        "default=noprint_wrappers=1:nokey=1",
        str(media_path),
    ]
    result = run_command(command, "reading media duration")
    try:
        return float(result.stdout.strip())
    except ValueError:
        raise WorkflowError(f"Could not read duration for file: {media_path}")


def extract_audio_to_wav(input_path, extracted_wav_path):
    """Extract/convert input audio to clean mono 44.1kHz WAV for consistent chunking."""
    print(f"[1/5] Extracting/converting audio: {input_path.name}")
    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(input_path),
        "-vn",
        "-ac",
        "1",
        "-ar",
        "44100",
        "-c:a",
        "pcm_s16le",
        str(extracted_wav_path),
    ]
    run_command(command, "extracting audio")


def split_audio(extracted_wav_path, chunks_dir, chunk_seconds):
    duration = get_duration_seconds(extracted_wav_path)
    chunk_count = max(1, math.ceil(duration / chunk_seconds))

    print(f"[2/5] Splitting audio into {chunk_count} chunk(s), max {chunk_seconds}s each")
    chunk_paths = []

    for index in range(chunk_count):
        start = index * chunk_seconds
        out_path = chunks_dir / f"chunk_{index + 1:03d}.wav"
        command = [
            "ffmpeg",
            "-y",
            "-ss",
            str(start),
            "-t",
            str(chunk_seconds),
            "-i",
            str(extracted_wav_path),
            "-ac",
            "1",
            "-ar",
            "44100",
            "-c:a",
            "pcm_s16le",
            str(out_path),
        ]
        run_command(command, f"splitting chunk {index + 1}")
        chunk_paths.append(out_path)

    return chunk_paths


def build_session():
    session = requests.Session()
    retry = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=2,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["POST"],
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("https://", adapter)
    return session


def convert_chunk_with_elevenlabs(
    session,
    api_key,
    chunk_path,
    converted_path,
    voice_id,
    model_id,
    stability,
    similarity_boost,
    style,
    speaker_boost,
    remove_background_noise,
    output_format,
):
    url = ELEVENLABS_STS_URL.format(voice_id=voice_id)

    params = {"output_format": output_format}
    headers = {"xi-api-key": api_key}

    voice_settings = {
        "stability": stability,
        "similarity_boost": similarity_boost,
        "style": style,
        "use_speaker_boost": speaker_boost,
    }

    data = {
        "model_id": model_id,
        "voice_settings": json.dumps(voice_settings),
        "remove_background_noise": str(remove_background_noise).lower(),
    }

    with open(chunk_path, "rb") as audio_file:
        files = {
            "audio": (chunk_path.name, audio_file, "audio/wav"),
        }
        response = session.post(
            url,
            headers=headers,
            params=params,
            data=data,
            files=files,
            timeout=600,
        )

    if not response.ok:
        try:
            error_detail = response.json()
        except Exception:
            error_detail = response.text
        raise WorkflowError(
            f"ElevenLabs API failed for {chunk_path.name}. "
            f"HTTP {response.status_code}: {error_detail}"
        )

    converted_path.write_bytes(response.content)


def convert_all_chunks(
    api_key,
    chunk_paths,
    converted_dir,
    args,
):
    print("[3/5] Sending chunks to ElevenLabs Voice Changer")
    session = build_session()
    converted_paths = []

    for index, chunk_path in enumerate(chunk_paths, start=1):
        converted_path = converted_dir / f"converted_{index:03d}.mp3"
        print(f"  - Converting chunk {index}/{len(chunk_paths)}: {chunk_path.name}")
        started = time.time()

        convert_chunk_with_elevenlabs(
            session=session,
            api_key=api_key,
            chunk_path=chunk_path,
            converted_path=converted_path,
            voice_id=args.voice_id,
            model_id=args.model_id,
            stability=args.stability,
            similarity_boost=args.similarity_boost,
            style=args.style,
            speaker_boost=args.speaker_boost,
            remove_background_noise=args.remove_background_noise,
            output_format=args.elevenlabs_output_format,
        )

        elapsed = time.time() - started
        print(f"    Done in {elapsed:.1f}s -> {converted_path.name}")
        converted_paths.append(converted_path)

    return converted_paths


def merge_converted_chunks(converted_paths, merged_path, list_file_path):
    print("[4/5] Merging converted chunks")

    with open(list_file_path, "w", encoding="utf-8") as list_file:
        for path in converted_paths:
            safe_path = path.as_posix().replace("'", "'\\''")
            list_file.write(f"file '{safe_path}'\n")

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file_path),
        "-c:a",
        "libmp3lame",
        "-b:a",
        "192k",
        str(merged_path),
    ]
    run_command(command, "merging converted chunks")


def master_audio(merged_path, output_path, lufs):
    print(f"[5/5] Mastering final audio around {lufs} LUFS with peak control")

    suffix = output_path.suffix.lower()
    if suffix == ".wav":
        codec_args = ["-c:a", "pcm_s16le"]
    elif suffix == ".mp3":
        codec_args = ["-c:a", "libmp3lame", "-b:a", "192k"]
    else:
        raise WorkflowError("Output file must end with .mp3 or .wav")

    audio_filter = (
        f"loudnorm=I={lufs}:TP=-1.5:LRA=11,"
        "alimiter=limit=0.95:level=true"
    )

    command = [
        "ffmpeg",
        "-y",
        "-i",
        str(merged_path),
        "-af",
        audio_filter,
        *codec_args,
        str(output_path),
    ]
    run_command(command, "final mastering")


def positive_float(value):
    try:
        number = float(value)
    except ValueError:
        raise argparse.ArgumentTypeError(f"Expected a number, got: {value}")
    return number


def restricted_0_to_1(value):
    number = positive_float(value)
    if number < 0 or number > 1:
        raise argparse.ArgumentTypeError("Value must be between 0 and 1")
    return number


def parse_args():
    parser = argparse.ArgumentParser(
        description="Batch process long tutorial audio/video through ElevenLabs Voice Changer and master the final output.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument("--input", required=True, help="Input audio/video file: WAV, MP3, MP4, etc.")
    parser.add_argument("--voice-id", required=True, help="ElevenLabs target voice ID")
    parser.add_argument("--output", required=True, help="Final output path ending with .mp3 or .wav")
    parser.add_argument("--chunk-seconds", type=int, default=DEFAULT_CHUNK_SECONDS, help="Chunk size in seconds. Keep below 300.")
    parser.add_argument("--model-id", default=DEFAULT_MODEL_ID, help="ElevenLabs speech-to-speech model ID")
    parser.add_argument("--stability", type=restricted_0_to_1, default=0.62, help="Voice stability from 0 to 1")
    parser.add_argument("--similarity-boost", type=restricted_0_to_1, default=0.82, help="Similarity boost from 0 to 1")
    parser.add_argument("--style", type=restricted_0_to_1, default=0.18, help="Style exaggeration from 0 to 1")
    parser.add_argument("--speaker-boost", action=argparse.BooleanOptionalAction, default=True, help="Enable/disable speaker boost")
    parser.add_argument("--remove-background-noise", action=argparse.BooleanOptionalAction, default=True, help="Ask ElevenLabs to remove background noise before conversion")
    parser.add_argument("--lufs", type=positive_float, default=-16.0, help="Integrated loudness target, e.g. -16 for tutorials/podcasts")
    parser.add_argument("--elevenlabs-output-format", default=DEFAULT_OUTPUT_FORMAT, help="ElevenLabs output format, e.g. mp3_44100_128")

    args = parser.parse_args()

    if args.chunk_seconds <= 0:
        parser.error("--chunk-seconds must be greater than 0")
    if args.chunk_seconds >= 300:
        parser.error("--chunk-seconds must be less than 300. Use 270 for safe uploads.")

    return args


def main():
    args = parse_args()
    input_path = Path(args.input).expanduser().resolve()
    output_path = Path(args.output).expanduser().resolve()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        api_key = ensure_prerequisites(input_path)

        print("ElevenLabs Batch Voice Changer")
        print(f"Input : {input_path}")
        print(f"Output: {output_path}")
        print(f"Voice : {args.voice_id}")
        print(f"Model : {args.model_id}")
        print("")

        with tempfile.TemporaryDirectory(prefix="elevenlabs_batch_") as temp_root:
            temp_root_path = Path(temp_root)
            chunks_dir = temp_root_path / "chunks"
            converted_dir = temp_root_path / "converted"
            chunks_dir.mkdir(parents=True, exist_ok=True)
            converted_dir.mkdir(parents=True, exist_ok=True)

            extracted_wav_path = temp_root_path / "source_extracted.wav"
            merged_path = temp_root_path / "merged_converted.mp3"
            list_file_path = temp_root_path / "concat_list.txt"

            extract_audio_to_wav(input_path, extracted_wav_path)
            chunk_paths = split_audio(extracted_wav_path, chunks_dir, args.chunk_seconds)
            converted_paths = convert_all_chunks(api_key, chunk_paths, converted_dir, args)
            merge_converted_chunks(converted_paths, merged_path, list_file_path)
            master_audio(merged_path, output_path, args.lufs)

        print("")
        print("SUCCESS")
        print(f"Final mastered file created: {output_path}")

    except WorkflowError as exc:
        print("")
        print("ERROR")
        print(str(exc))
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nCancelled by user.")
        sys.exit(130)


if __name__ == "__main__":
    main()
