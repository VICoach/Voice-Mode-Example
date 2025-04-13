import os
from config.clients import get_elevenlabs_client, get_groq_client


groq_client = get_groq_client()
async def groq_transcribe(file_path):
    try:
        with open(file_path, "rb") as f:
            file_bytes = f.read()

        transcription = groq_client.audio.transcriptions.create(
            file=(os.path.basename(file_path), file_bytes),
            model="whisper-large-v3-turbo",
            response_format="verbose_json",
        )
        return transcription.text
    except Exception as e:
        print(f"Error: {e}")
        return "Error: Failed to transcribe audio."


async def text_to_speech(text: str):
    """
    Generates an audio file from the given text using ElevenLabs API and returns the audio data.
    Returns:
        bytes: The generated audio data in MP3 format
    """
    voice_client = get_elevenlabs_client()
    audio_generator = voice_client.text_to_speech.convert(
        voice_id="21m00Tcm4TlvDq8ikWAM",
        output_format="mp3_22050_32",
        text=text,
        model_id="eleven_v2_5_flash",
    )

    # Convert generator to bytes
    audio_data = b"".join(chunk for chunk in audio_generator)
    return audio_data
