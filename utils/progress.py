import asyncio

class ProgressTracker:

    def __init__(self):
        self.queue = asyncio.Queue()

    async def book_finished(self):
        await self.queue.put({
            "type": "book"
        })

    async def page_finished(self, page_number):
        await self.queue.put({
            "type": "page",
            "page_number": page_number,
        })

    async def shutdown(self):
        await self.queue.put({
            "type": "shutdown"
        })

    