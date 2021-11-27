### Installation:

`pip install site-scrapers`

### What this does?
Will fetch car details from dealership (concurrently)

### Usage:

```python
import asyncio

from scrapers.scraper import scrape_all

if __name__ == '__main__':
    results = asyncio.run(scrape_all())
    print(*results, sep="\n") # will output fetched car details
```

### Supported Dealerships
https://lietotiauto.mollerauto.lv  
https://lv.brcauto.eu  
https://certified.inchcape.lv/auto
