from abc import ABC, abstractmethod
from dataclasses import dataclass
import pandas as pd
import numpy as np

from ts_tariffs.tariffs import TariffRegime

class Validator:
    @staticmethod
    def electricity_data_cols(df):
        mandatory_cols = np.array([
            'demand_energy',
            'demand_power',
            'generation_energy',
            'generation_power',
            'power_factor'
        ])
        is_present = [col in mandatory_cols for col in df.columns]
        if not all(is_present):
            raise ValueError(f'{mandatory_cols[~is_present]}')


@dataclass
class MeterData(ABC):
    name: str
    meter_ts: pd.DataFrame

    def set_sample_rate(self, sample_rate):
        pass


@dataclass
class ElectricityMeterData(MeterData):

    def __post_init__(self):
        Validator.electricity_data_cols(self.meter_ts)

    # @classmethod
    # def from_dataframe(cls, ):
    #
    #     return


    def set_sample_rate(self, sample_rate):
        pass


my_df = pd.DataFrame(columns=[
            'demand_power',
            'generation_energy',
            'power_factor'
        ])
meter = ElectricityMeterData('test', my_df)


@dataclass
class Site:
    name: str
    tariffs: TariffRegime
    meter_data: MeterData
    bill_ledgers: dict[pd.DataFrame] = None
    bill: dict[float] = None

    # def __post_init__(self):
    #
    #     self.meter_data.set_sample_rate(self.tariffs.metering_sample_rate)

    def calculate_bill(self, detailed_bill=True):
        self.bill_ledgers = {}
        self.bill = {}
        for charge in self.tariffs.charges:
            self.bill_ledgers[charge.name] = charge.calculate_charge(
                self.meter_data.meter_ts,
                detailed_bill=detailed_bill
            )
            self.bill[charge.name] = float(self.bill_ledgers[charge.name].sum())
