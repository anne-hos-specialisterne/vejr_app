
from src.vejrdata.api_clients.base import BaseAPIClient


class DMI_API(BaseAPIClient):

    def __init__(self):
        super().__init__(
            base_url="https://opendataapi.dmi.dk/v2"
        )

