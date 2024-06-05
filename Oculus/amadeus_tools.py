from pydantic.v1 import BaseModel, BaseSettings, Field
from typing import Optional,Type
from langchain.tools import BaseTool
from langchain.callbacks.manager import (AsyncCallbackManagerForToolRun, CallbackManagerForToolRun)
import requests
import aiohttp

# Flight Search offers tool
class AmadeusFlightOffersSearchToolSchema(BaseModel):
    originLocationCode: str = Field(description="The origin city code Format")
    destinationLocationCode: str = Field(description="The destination city code Format")
    departureDate: str = Field(description="The departure date, Must be in Date format")
    returnDate: Optional[str] = Field(description="The return date, Must be in Date format")
    adults: int = Field(description="The number of traveling adults")
    max: Optional[int]  = Field(default=5, description="maximum number of flight offers to return")
    nonStop: Optional[bool] = Field(default=False, description="Whether to only search for non-stop flights")
    maxPrice: Optional[int] = Field(default=None, description="The maximum price for the flight offers")
    currencyCode: Optional[str] = Field(default=None, description="The currency code for the flight offers")
    travelClass: Optional[str] = Field(default=None, description="The travel class for the flight offers, Available values : ECONOMY, PREMIUM_ECONOMY, BUSINESS, FIRST")


class AmadeusFlightOffersSearchTool(BaseTool, BaseSettings):
    name: str = "Amadeus_flight_offers_search"
    description: str = """Tool that searches for flight offers using the Amadeus API."""
    args_schema: Type[AmadeusFlightOffersSearchToolSchema] = AmadeusFlightOffersSearchToolSchema
    base_url: str = "https://test.api.amadeus.com/v2/shopping/flight-offers"
    client_id: str = Field(..., env="AMADEUS_CLIENT_ID")
    client_secret: str = Field(..., env="AMADEUS_CLIENT_SECRET")

    @property
    def _headers(self) -> dict:
        # Authenticate with the Amadeus API and obtain an access token
        data = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        response = requests.post("https://test.api.amadeus.com/v1/security/oauth2/token", headers={"Content-Type": "application/x-www-form-urlencoded"}, data=data)
        if response.status_code == 200:
            access_token = response.json()["access_token"]
        else:
            raise Exception(f"An error occurred while authenticating with the Amadeus API: {response.text}")

        return {"accept": "application/vnd.amadeus+json", "Authorization": f"Bearer {access_token}"}

    def _run(
        self,
        originLocationCode: str,
        destinationLocationCode: str,
        departureDate: str,
        adults: int,
        nonStop: bool = False,
        max: Optional[int] = 5,
        returnDate: Optional[str] = None,
        maxPrice: Optional[int] = None,
        currencyCode: Optional[str] = None,
        travelClass: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:

        """Run the tool"""

        # Set up the query parameters for the GET request
        params = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate,
            "returnDate": returnDate,
            "adults": adults,
            "nonStop": str(nonStop).lower(),
            "maxPrice": maxPrice,
            "currencyCode": currencyCode,
            "travelClass": travelClass,
            "max": max
        }

        # Make a GET request to the Amadeus Flight Offers API
        response = requests.get(self.base_url, params=params, headers=self._headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f"An error occurred while making a GET request to the Amadeus Flight Offers API: {response.text}")

    async def _arun(
        self,
        originLocationCode: str,
        destinationLocationCode: str,
        departureDate: str,
        adults: int,
        nonStop: bool = False,
        max: Optional[int] = 5,
        returnDate: Optional[str] = None,
        maxPrice: Optional[int] = None,
        currencyCode: Optional[str] = None,
        travelClass: Optional[str] = None,
        run_manager: Optional[CallbackManagerForToolRun] = None,
    ) -> dict:

        """Run the tool asynchronously."""

        # Set up the query parameters for the GET request
        params = {
            "originLocationCode": originLocationCode,
            "destinationLocationCode": destinationLocationCode,
            "departureDate": departureDate,
            "returnDate": returnDate,
            "adults": adults,
            "nonStop": str(nonStop).lower(),
            "maxPrice": maxPrice,
            "currencyCode": currencyCode,
            "travelClass": travelClass,
            "max": max
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(self.base_url, params=params, headers=self._headers) as response:
                return await response.json()