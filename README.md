### Installation:

`pip install site-scrapers`

### Usage:

```python
from returns.methods import unwrap_or_failure
from scrapers.mollerAuto import parse_moller_auto

if __name__ == '__main__':
    print(*unwrap_or_failure(parse_moller_auto()), sep="\n")
```

### Supported Dealerships
https://lietotiauto.mollerauto.lv  
https://lv.brcauto.eu
