import datetime
from .core.gql_type import GQLType
from dataclasses import dataclass
from enum import StrEnum

class DrivingStatus(StrEnum):
    WAIT = "WAIT"
    DRIVE = "DRIVE"
    REST = "REST"

@dataclass
class TaxiHistoryType(GQLType):
    from_latitude: float
    from_longitude: float
    to_longitude: float
    to_latitude: float
    price: float
    created_at: datetime
    taxi_fio: str
    def __post_init__(self):
        if isinstance(self.created_at, str):
            self.created_at = datetime.datetime.fromisoformat(self.created_at)
        if isinstance(self.price, str):
            self.price = float(self.price)