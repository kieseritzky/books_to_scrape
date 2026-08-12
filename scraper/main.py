from database.connection import engine, Base
from database import models
from api.routers import basic
from database.connection import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends
import config
from playwright.async_api import async_playwright
import asyncio
from logger_config import logging
from scraper.listing import basic_listing
from storage.csv_writer import save_to_csv
from storage.json_writer import save_to_json
from scraper.listing import collect_urls
from scraper.worker import worker
from utils.progress import ProgressTracker
from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    TaskProgressColumn,
    TimeElapsedColumn,
)

logger = logging.getLogger(__name__)

Base.metadata.create_all(bind=engine)


async def display_worker(progress_events, rich_progress, task):

    while True:

        event = await progress_events.queue.get()

        if event["type"] == "book":

            rich_progress.update(
                task,
                advance=1
            )

        elif event["type"] == "shutdown":
            break

        progress_events.queue.task_done()


async def main():

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = config.HEADLESS)
        context = await browser.new_context()
        queue = asyncio.Queue()

        basic_data = []
        advanced_data = []

        progress_events = ProgressTracker()

        logger.info("Starting scraper")
        
        # try:

        #     await basic_listing(context, basic_data)

        # except KeyboardInterrupt:
        #     logger.exception("Scraping interrupted by user. Saving progress...")
        #     # print(f"\nScraping interrupted by user. Saving progress...")

        # except Exception as e:
        #     logger.exception("An error occured during scraping: %s", e)
        #     # print(f"\nAn error occured during scraping: {e}")

        # finally:
        #     save_to_csv(config.BASIC_CSV, basic_data, config.BASIC_FIELDS)
        #     save_to_json(config.BASIC_JSON, basic_data)
        #     await browser.close()

        try:
            with Progress(
                TextColumn("{task.description}"),
                BarColumn(),
                TaskProgressColumn(),
                TimeElapsedColumn(),
            ) as rich_progress:
                       
                books_task = rich_progress.add_task(
                    "Books scraped",
                    total = 1000
                )
                display = asyncio.create_task(
                                display_worker(
                                    progress_events,
                                    rich_progress,
                                    books_task
                                )
                            )
                producer = asyncio.create_task(
                    collect_urls(context, queue, progress_events)

                )
                workers = [
                            asyncio.create_task(worker(context, queue, advanced_data, progress_events))
                            for _ in range(3)
                ]

                logger.info(
                    "Started %d workers",
                    len(workers)
                )

                await producer
                await queue.join()

                for _ in workers:
                    await queue.put(None)

                await asyncio.gather(*workers)

                logger.info(
                    "Scraping completed. Total books: %d",
                    len(advanced_data)
                )

                await progress_events.shutdown()
                await display

        except KeyboardInterrupt:
            logger.info("Scraping interrupted by user. Saving progress...")
            # print("\nScraping interrupted by user. Saving progress...")

        except Exception as e:
            logger.exception("An error occured during scraping: %s", e)
            # print(f"\nAn error occured during scraping: {e}")

        finally:
            logger.info("Saving scraped data.")
            save_to_csv(config.ADVANCED_CSV, advanced_data, config.ADVANCED_FIELDS)
            save_to_json(config.ADVANCED_JSON, advanced_data)
            await browser.close()   


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Program interrupted by user.")
    except Exception as e:
        logger.warning("Scraper stopped: %s", e)