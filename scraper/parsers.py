def clean_key(raw_key):
    return raw_key.lower().replace(" ", "_").replace("(", "").replace(")", "").replace(".", "").replace("#", "")

def clean_text(raw_text):
    if raw_text:
        return raw_text.strip()
    return ""

async def parse_book(el):
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


    return result

async def parse_book_page(detail_page):
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
    return result