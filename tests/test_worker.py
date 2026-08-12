import pytest, asyncio, pytest_asyncio, logging
from unittest.mock import AsyncMock, patch
from scraper.worker import worker

@pytest.mark.asyncio
async def test_worker(expected_book, mock_context, mock_page, mock_progress, mock_parser):

    mock_context.new_page.return_value = mock_page

    queue = asyncio.Queue()

    await queue.put("https://books.com/book1")
    await queue.put(None)

    data = []



    # Fake retry
    async def fake_retry(operation):
        return await operation()

    # Act
    with patch(
        "scraper.worker.parse_book_page",
        new=mock_parser,
    ), patch(
        "scraper.worker.retry",
        new=fake_retry,
    ):
        await worker(mock_context, queue, data, mock_progress)

    # Assert

    # 1. Did worker open the correct URL?
    mock_page.goto.assert_awaited_once_with(
        "https://books.com/book1",
        wait_until="domcontentloaded",
    )

    # 2. Did worker call the parser?
    mock_parser.assert_awaited_once_with(mock_page)

    # 3. Did worker save the book?
    assert data == [expected_book]

    # 4. Did worker update progress?
    mock_progress.book_finished.assert_awaited_once()

@pytest.mark.asyncio
async def test_worker_goto_failure(expected_book, mock_context, mock_page, mock_progress, mock_parser, caplog):
    mock_context.new_page.return_value = mock_page
    mock_page.goto.side_effect = Exception("network error")
    queue = asyncio.Queue()
    await queue.put("https://hello.com")
    await queue.put(None)
    data = []

    async def fake_retry(operation):
        return await operation()

    caplog.set_level(logging.ERROR)

    
    with patch(
        "scraper.worker.retry", new=fake_retry
    ), patch(
        "scraper.worker.parse_book_page", new=mock_parser
    ):
        await worker(mock_context, queue, data, mock_progress)

    assert  mock_parser.await_count == 0
    assert data == []
    mock_progress.finished_book.assert_not_awaited()    
    assert "Failed scraping https://hello.com." in caplog.text