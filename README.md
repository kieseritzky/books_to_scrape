# Books to Scrape - Async Playwright Web Scraper

## Overview

This project is a web scraper built with Python and Playwright that extracts book information from Books to Scrape.

The project started as a basic scraper that collected information from listing pages and was later upgraded into an asynchronous scraper using a queue-based worker architecture.

The upgraded version demonstrates how asynchronous programming can improve scraping performance by allowing multiple book detail pages to be processed concurrently.

The project demonstrates asynchronous programming, task queues, and the producer-consumer pattern to efficiently scrape book detail pages concurrently.

---

## Features

### Basic Scraper

* Scrapes book information available directly from listing pages
* Navigates through pagination
* Saves extracted data to CSV and JSON formats

### Advanced Async Scraper

* Extracts individual book URLs from listing pages
* Uses `asyncio.Queue` to manage scraping tasks
* Implements a producer-consumer architecture
* Uses multiple asynchronous workers
* Each worker maintains its own Playwright page to avoid resource contention
* Scrapes detailed information from individual book pages
* Continues scraping even if individual pages fail
* Uses structured logging for console output and error reporting
* Gracefully handles interruption (Ctrl+C) by saving scraped data before exiting.

---

## Technologies Used

* Python
* Playwright
* asyncio
* JSON
* CSV
* logging

---

## Project Architecture

The advanced scraper follows a producer-consumer pattern:

```
Listing Page
     |
     |  Collect book URLs
     |
     v
 asyncio.Queue
     |
     |
 -----------------
 |       |       |
 v       v       v
Worker  Worker  Worker

Detail pages scraped concurrently
```

The listing page acts as the producer by collecting URLs and adding them to the queue.

Workers act as consumers by taking URLs from the queue, visiting book pages, extracting details, and storing results.

---

## Data Extracted

The scraper collects information such as:

* Book title
* Product information
* Price
* Availability
* Rating
* UPC
* Description
* Other available metadata

---

## Installation

Clone the repository:

```bash
git clone https://github.com/kieseritzky/books_to_scrape
```

Navigate into the project:

```bash
cd books-to-scrape
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the environment:

Windows:

```bash
venv\Scripts\activate
```

Linux/macOS:

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Install Playwright browsers:

```bash
playwright install
```

---

## Running the Project

Run the scraper:

```bash
python main.py
```

The scraped data will be saved in CSV and JSON formats.

---

## Learning Outcomes

This project helped me practice:

* Asynchronous programming in Python
* Creating and managing asyncio tasks
* Queue-based architectures
* Producer-consumer design patterns
* Browser automation using Playwright
* Error handling in async applications
* Improving scraper scalability
* Using Python's logging module for structured application logging

---

## Future Improvements

Possible improvements:

- [ ] Add retry handling for failed requests
- [X] Add logging instead of print statements
- [ ] Store data in a database
- [ ] Add duplicate detection
- [ ] Add configurable worker counts
- [ ] Add scraping statistics and progress tracking

---

## Disclaimer

This project was created for educational purposes using Books to Scrape, a website designed for practicing web scraping.
