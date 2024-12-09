from pyee import AsyncIOEventEmitter
import asyncio

async def main():
    emitter = AsyncIOEventEmitter()

    @emitter.on('event')
    async def handler(arg):
        print(f'Event triggered with argument: {arg}')

    await emitter.emit('event', 'Hello, World!')

asyncio.run(main())
