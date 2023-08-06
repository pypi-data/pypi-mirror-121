from typing import Optional
import pandas as pd
from OctopusAgile import Agile
import warnings

from .abstract import Collector
from .misc import iso8601z


class Octopus(Collector):
    timezone = 'Europe/London'

    def get_data(
            self,
            region_code: str,
            interval: Optional[pd.Interval]
            = None,
    ) -> pd.DataFrame:
        agile = Agile(region_code)
        if not interval:
            rates = agile.get_new_rates()
        else:
            date_from = iso8601z(interval.left)
            date_to = iso8601z(interval.right)
            if interval.length.days > 2:
                warnings.warn(
                    'You requested an interval larger than 2 days, '
                    'be advised that the response may not be complete')
            rates = agile.get_rates(date_from, date_to)

        rates = pd.DataFrame.from_dict(rates['date_rates'], orient='index')
        # noinspection PyTypeChecker
        rates.index = pd.to_datetime(rates.index)
        rates.rename(columns={0: 'value_inc_vat'}, inplace=True)
        rates = rates.tz_convert(self.timezone)
        rates.sort_index(inplace=True)
        return rates
