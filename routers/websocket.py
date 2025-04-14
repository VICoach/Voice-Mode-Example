from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from controllers.voice_controller import speech_to_text_controller, text_to_speech_controller

router = APIRouter()

@router.websocket("/ws/audio-stream")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            # Wait for raw audio bytes
            audio_bytes = await websocket.receive_bytes()
            print(f"Received audio bytes: {len(audio_bytes)} bytes")

            # Transcribe
            transcript = await speech_to_text_controller(audio_bytes)
            print(f"Transcription: {transcript}")

            # Convert transcript to TTS audio
            tts_audio_bytes = await text_to_speech_controller(transcript)

            # Send result: first JSON metadata
            await websocket.send_json({"transcript": transcript})

            # Then send the audio separately as binary
            await websocket.send_bytes(tts_audio_bytes)

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
