from deepgram import Deepgram
import asyncio, json,os
from dotenv import load_dotenv
load_dotenv()

DEEPGRAM_API_KEY = os.getenv('DEEPGRAM_API_KEY')

PATH_TO_FILE = './Bueller-Life-moves-pretty-fast.wav'

async def main():
    dg_client = Deepgram(DEEPGRAM_API_KEY)

    socket = await dg_client.transcription.live({'punctuate': True})

    print('Socket opened')

    async def process_audio(connection):
        with open(PATH_TO_FILE,'rb') as audio:
            CHUNK_SIZE_BYTES = 8192
            CHUNK_RATE_SEC = 0.001
            chunk = audio.read(CHUNK_SIZE_BYTES)
            while chunk:
                connection.send(chunk)
                await asyncio.sleep(CHUNK_RATE_SEC)
                chunk = audio.read(CHUNK_SIZE_BYTES)

            await connection.finish()
    
    socket.register_handler(socket.event.CLOSE, lambda _: print('Socket closed'))

    socket.register_handler(socket.event.TRANSCRIPT_RECEIVED, print)

    await process_audio(socket)

asyncio.run(main())
