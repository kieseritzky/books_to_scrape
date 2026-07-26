from urllib.parse import urljoin
import asyncio
from config import BASE_URL
from parsers import clean_key, clean_text

async def basic_scraper(context, data):
    page = await context.new_page()
    await page.goto(BASE_URL)
    await page.wait_for_load_state()

    page_number = 1
    books = 1

    while True:
        print(f"Scraping page number {page_number}")
        book_el = await page.locator(".product_pod").all()
        for el in book_el:
            result = {}

            title_el = el.locator("h3 a")
            result["title"] = clean_key(await title_el.get_attribute("title"))

            price_el = el.locator(".price_color")
            result["price"] = clean_text(await price_el.inner_text())

            avail_el = el.locator("p.instock.availability")
            result["availability"] = clean_text(await avail_el.inner_text())

            rating_el = el.locator(".star-rating")
            full_class = await rating_el.get_attribute("class")
            rating_word = full_class.split()[1]
            result["rating"] = rating_word
        
            data.append(result)
            books += 1

        next_button = page.locator(".next a")
        if await next_button.count() == 0:
            break

        await next_button.click()
        page_number += 1

    print(f"Extracted data for {books} books from {page_number} pages")

async def advanced_scraper(context, data):

    queue = asyncio.Queue()
    async def worker():
        detail_page = await context.new_page()
        while True:
            url = await queue.get()

            if url is None:
                queue.task_done()
                break
            try:
                await detail_page.goto(url, wait_until="domcontentloaded")

                result = {}
                para_el = detail_page.locator("article.product_page > p")
                if await para_el.count() > 0:
                    description = await para_el.inner_text()
                else:
                    description = "No description available."
                result["description"] = description
                rows = await detail_page.locator("table.table.table-striped tr").all()
                for row in rows:
                    key = clean_key(await row.locator("th").inner_text())
                    value = clean_text(await row.locator("td").inner_text())
                    result[key.lower().replace(" ", "_")] = value
                data.append(result)

            except Exception as e:
                print(f"Failed {url}: {e}")

            finally:
                queue.task_done()

        await detail_page.close()

    workers = [
        asyncio.create_task(worker())
        for _ in range(2)
        ]
    
    page = await context.new_page()
    await page.goto(BASE_URL, wait_until="domcontentloaded")

    book = 0
    page_number = 1

    while True:
        print(f"Extracting links from listing page {page_number}...")

        #Grab all URLs 
        link_elements = await page.locator(".product_pod h3 a").all()
        relative_urls = [await el.get_attribute("href") for el in link_elements]

        for rel_url in relative_urls:
            full_url = urljoin(page.url, rel_url)
            await queue.put(full_url)

            # Scrape and store
            
            book += 1

        next_button = page.locator(".next a")
        if await next_button.count() == 0:
            print("No more pages left to scrape.")
            break

        await next_button.click()
        await page.wait_for_load_state("domcontentloaded")

        page_number += 1

    await queue.join()

    for _ in workers:
        await queue.put(None)

    await asyncio.gather(*workers)
    print(f"Successfully scraped {book} books from {page_number} pages.")    