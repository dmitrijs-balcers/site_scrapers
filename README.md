### Installation:

`pip install site-scrapers`

### Usage:

```python
from returns.methods import unwrap_or_failure
from scrapers.list.mollerAuto import fetch_moller_auto_list

if __name__ == '__main__':
    print(*unwrap_or_failure(fetch_moller_auto_list()), sep="\n")
```

### Supported Dealerships
https://lietotiauto.mollerauto.lv  
https://lv.brcauto.eu  
https://certified.inchcape.lv/auto
