

from pydantic import BaseModel
from datetime import datetime


class DMIprops(BaseModel):
    parameterId: str
    observed: datetime
    value: float
    stationId: str

class DMIobservation(BaseModel):
    id: str
    properties: DMIprops

class DMIdata(BaseModel):
    features: list[DMIobservation]