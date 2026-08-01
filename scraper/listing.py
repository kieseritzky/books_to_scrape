from urllib.parse import urljoin
import logging
from utils.retry import retry
from config import BASE_URL
from scraper.parsers import parse_book
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)


logger = logging.getLogger(__name__)

async def basic_listing(context, data):
    total_books = 1000

    progress = Progress(
        TextColumn("{task.description}"),
        BarColumn(),
        TaskProgressColumn(),
        TimeElapsedColumn()
    )


    with progress:
        books_task = progress.add_task(
            "Books scraped",
            total=total_books
        )

        page = await context.new_page()
        await retry(lambda: page.goto(BASE_URL))
        await page.wait_for_load_state()

        page_number = 1

        while True:
            logger.info("Scraping page number %d", page_number)

            # print(f"Scraping page number {page_number}")
            book_el = await page.locator(".product_pod").all()

            for el in book_el:
                result = await parse_book(el)
                data.append(result)

                progress.update(
                    books_task,
                    advance=1
                )
            next_button = page.locator(".next a")
            if await next_button.count() == 0:
                break

            await retry(lambda: next_button.click())
            page_number += 1

        logger.info("Extracted data for %d books from %d page_number", len(data), page_number)


async def collect_urls(context, queue, progress):
    page_number=1
    page = await context.new_page()
    await retry(lambda: page.goto(BASE_URL, wait_until="domcontentloaded"))

    while True:


        #Grab all URLs 
        logger.info("Extracting links from listing page %d", page_number)


        link_elements = await page.locator(".product_pod h3 a").all()
        relative_urls = [await el.get_attribute("href") for el in link_elements]

        logger.info(
            "Found %d books on listing page %d",
            len(relative_urls),
            page_number
        )

        for rel_url in relative_urls:
            full_url = urljoin(page.url, rel_url)
            await queue.put(full_url)

        logger.debug(
            "Queued %d URLs",
            len(relative_urls)
        )
        
        next_button = page.locator(".next a")
        if await next_button.count() == 0:
            logger.info("Finished extracting all URLs.")
            break

        await retry(lambda: next_button.click())
        await page.wait_for_load_state("domcontentloaded")

        page_number += 1

        await progress.page_finished(page_number)


    