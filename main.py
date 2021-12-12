import asyncio
import time

from scrapers.scraper import scrape_all

if __name__ == "__main__":
    start_time = time.time()
    results = asyncio.run(scrape_all())
    print(*results, sep="\n")

    print("--- %s seconds ---" % (time.time() - start_time))
