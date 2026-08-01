import asyncio, random, logging
from playwright.async_api import async_playwright


logger = logging.getLogger(__name__)

async def retry(operation, retries=3):
    last_exception = None
    for i in range(retries):
        delay = 2**i + random.uniform(0, 1)
        try:
            return await operation()
            break
        except Exception as e:
            last_exception = e
            logger.info("Attempt%d failed", i+1)
            # print(f"Attempt{i+1} failed: {e}")
            if i == retries -1:
                logger.info("All attempts failed.")
                # print("All attempts failed.")
                raise 
        await asyncio.sleep(delay)
           
