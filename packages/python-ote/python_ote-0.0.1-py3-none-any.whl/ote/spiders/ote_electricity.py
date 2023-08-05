from datetime import date
from urllib.parse import urlencode

import scrapy
from dateutil import rrule
from scrapy.loader import ItemLoader

from ..items import DayMarketPricesItem


class DayMarketPricesSpider(scrapy.Spider):
    name = "day_market_prices_spider"

    def __init__(self, date_from, date_to=None, cb_item_scraped=None, *args, **kwargs):
        """ Get the electricity prices from OTE. It will scrape the OTE website
            and get daily electricity price for the given interval specified by
            `date_from` and `date_to` (which are datetime.date-compatible
            objects). If `date_to` is not provided it will scrape data starting
            from `date_from` till today.

            The `cb_item_scraped` is a callback accepting one argument "item"
            that will be called for each item (consumption data for the given
            month) scraped.
        """
        super().__init__(*args, **kwargs)

        # Year/month to scrape
        self._date_from = date_from
        self._date_to = date_to if date_to is not None else date.today()

        # Output callback - will be called for each item scraped
        self._cb_item_scraped = cb_item_scraped

    def start_requests(self):
        # Iterate over years/months between `date_from` and `date_to` and get
        # the hourly prices for the respective days.
        #
        # We need to set the day in `dtstart` to the first day of month because
        # otherwise if the day is greater than the day in `until` the last
        # month would not be included. For example for dtstart 2020-03-09 and
        # until 2020-08-01 would skip 2020-08 because 2020-08-09 comes after
        # 2020-08-01.
        for dt in rrule.rrule(rrule.DAILY, dtstart=self._date_from.replace(day=1), until=self._date_to):
            qs = urlencode(
                {
                    "date": dt.isoformat(),
                }
            )
            url = f"https://www.ote-cr.cz/cs/kratkodobe-trhy/elektrina/denni-trh?{qs}"
            yield scrapy.Request(url=url, callback=self.handle_day_market_prices, cb_kwargs={"dt": dt, "not_before": self._date_from, "not_after": self._date_to})

    def handle_day_market_prices(self, response, dt, not_before, not_after):
        table_rows = response.css("table.report_table tbody tr")
        for row in table_rows:
            loader = ItemLoader(item=DayMarketPricesItem(), selector=row)
            loader.add_css("date", "th::text")
            loader.add_css("consumption", "td::text")
            item = loader.load_item()

            # Check if the date in consumption data is within our time frame;
            # if it is, yield the consumption data, otherwise continue with the
            # next item
            if not_before <= item["date"] <= not_after:
                self._cb_item_scraped(item)
                yield item
