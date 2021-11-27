### Installation:

`pip install site-scrapers`

### Usage:

```python
import asyncio

from scrapers.scraper import scrape_all

if __name__ == '__main__':
    results = asyncio.run(scrape_all())
    print(*results, sep="\n")
```

### Supported Dealerships
https://lietotiauto.mollerauto.lv  
https://lv.brcauto.eu  
https://certified.inchcape.lv/auto
