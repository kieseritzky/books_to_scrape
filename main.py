import config, storage, parsers, scraper
from playwright.async_api import async_playwright
import asyncio
from logger_config import logging

logger = logging.getLogger(__name__)

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless = config.HEADLESS)
        context = await browser.new_context()

        basic_data = []
        advanced_data = []

        try:

            await scraper.basic_scraper(context, basic_data)

        except KeyboardInterrupt:
            logger.exception("Scraping interrupted by user. Saving progress...")
            # print(f"\nScraping interrupted by user. Saving progress...")

        except Exception as e:
            logger.exception("An error occured during scraping: %s", e)
            # print(f"\nAn error occured during scraping: {e}")

        finally:
            storage.save_to_csv(config.BASIC_CSV, basic_data, config.BASIC_FIELDS)
            storage.save_to_json(config.BASIC_JSON, basic_data)

        try:

            await scraper.advanced_scraper(context, advanced_data)

        except KeyboardInterrupt:
            logger.info("Scraping interrupted by user. Saving progress...")
            # print("\nScraping interrupted by user. Saving progress...")

        except Exception as e:
            logger.exception("An error occured during scraping: %s", e)
            # print(f"\nAn error occured during scraping: {e}")

        finally:

            storage.save_to_csv(config.ADVANCED_CSV, advanced_data, config.ADVANCED_FIELDS)
            storage.save_to_json(config.ADVANCED_JSON, advanced_data)

            await browser.close()   

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Program interrupted by user.")
    except Exception as e:
        logger.warning("Scraper stopped: %s", e)