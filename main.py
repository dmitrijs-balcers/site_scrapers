import asyncio
import time
from scrapers.scraper import scrape_all


if __name__ == "__main__":
    start_time = time.time()
    results = asyncio.run(scrape_all())

    # r2 = [flow(
    #     result,
    #     lambda _: _.bind(lambda _: _),
    #     lambda _: print(*_, sep="\n")
    # ) for result in results]

    print(*results, sep="\n")

    print("--- %s seconds ---" % (time.time() - start_time))
