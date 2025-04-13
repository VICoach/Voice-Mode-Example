from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from controllers.voice_controller import speech_to_text_controller, text_to_speech_controller
import base64

router = APIRouter()

@router.websocket("/ws/audio-stream")
async def audio_stream(websocket: WebSocket):
    await websocket.accept()

    try:
        while True:
            message = await websocket.receive_json()

            if "filestring" in message:
                base64_audio = message["filestring"]

                try:
                    # Decode the audio
                    audio_bytes = base64.b64decode(base64_audio)
                    print(f"Received audio bytes: {len(audio_bytes)} bytes")

                    # Transcribe
                    transcript = await speech_to_text_controller(audio_bytes)
                    print(f"Transcription: {transcript}")

                    # Convert transcript to TTS audio
                    audio_data = await text_to_speech_controller(transcript)

                    # Encode TTS audio as base64 to send over WebSocket
                    encoded_audio = base64.b64encode(audio_data).decode("utf-8")

                    # Send the transcript and audio
                    await websocket.send_json({
                        "transcript": transcript,
                        "audio_base64": encoded_audio
                    })

                except Exception as e:
                    await websocket.send_json({"error": str(e)})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_json({"error": str(e)})
