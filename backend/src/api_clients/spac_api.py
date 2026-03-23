
from src.api_clients.base import BaseAPIClient



class SpacAPI(BaseAPIClient):

    def __init__(self, api_key):
        super().__init__(
            base_url='https://climate.spac.dk/api',
            headers={"Authorization": f"Bearer {api_key}"}
        )



