from returns.methods import unwrap_or_failure
from returns.pipeline import flow

from scrapers.brcAuto import parse_brc_auto
from scrapers.mollerAuto import parse_moller_auto
from scrapers.inchcape import parse_inchcape

if __name__ == "__main__":
    print(*flow(
        parse_moller_auto(),
        unwrap_or_failure,
    ), sep="\n")

    print(*flow(
        parse_inchcape(),
        unwrap_or_failure
    ), sep="\n")

    print(*flow(
        parse_brc_auto(),
        unwrap_or_failure
    ), sep="\n")
