import logging
from utils.retry import retry
from scraper.parsers import clean_key, clean_text, parse_book_page

logger = logging.getLogger(__name__)

async def worker(context, queue, data, progress):
        detail_page = await context.new_page()
        while True:
            url = await queue.get()

            if url is None:
                queue.task_done()
                break
            try:
                await retry(lambda: detail_page.goto(url, wait_until="domcontentloaded"))

                result = await parse_book_page(detail_page)
                data.append(result)
                await progress.book_finished()

            except Exception as e:
                logger.exception("Failed scraping %s.", url)
                # print(f"Failed {url}: {e}")

            finally:
                queue.task_done()