from typing import List
import aiohttp
from config import API_BASE_URL
from aiogram.fsm.context import FSMContext
from data.locales import get_text
from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiohttp import ClientError
import logging

logger = logging.getLogger(__name__)

class CountryService:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def get_countries(self, proxy_type: str) -> List[str]:
        """
        Fetch country codes from API for a given proxy type
        """
        params = {"type": proxy_type}

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/countries", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data
                    else:
                        logger.warning(f"Bad response from /countries: {response.status}")
        except ClientError as e:
            logger.error(f"API error in get_countries: {e}")
        except Exception as e:
            logger.exception(f"Unexpected error in get_countries: {e}")

        return []

    @staticmethod
    async def get_country_name(state: FSMContext, code: str) -> str:
        """
        Get localized country name from the localization system.
        Falls back to the code itself if translation not found.
        """
        try:
            return await get_text(state, f"country_{code.lower()}")
        except KeyError:
            return code.upper()


    async def get_countries_list_keyboard(self, state: FSMContext):
        data = await state.get_data()
        proxy_type = data.get("proxy_type")
        country_codes = await self.get_countries(proxy_type)
        
        keyboard = []
        for code in country_codes:
            country_name = await self.get_country_name(state, code)
            keyboard.append([KeyboardButton(text=country_name)])
        
        return ReplyKeyboardMarkup(
            keyboard=keyboard,
            resize_keyboard=True,
            one_time_keyboard=True
        )
    
    async def get_country_dict(self, state: FSMContext) -> dict:
        """
        Returns a dictionary of the form: {'US': 'United States', 'DE': 'Germany', ...}
        with the user's locale.
        """
        data = await state.get_data()
        proxy_type = data.get("proxy_type")
        if not proxy_type:
            raise ValueError(await get_text(state, "proxy_type_not_selected_error"))

        country_codes = await self.get_countries(proxy_type)
        return {
            code: await self.get_country_name(state, code)
            for code in country_codes
        }
    
    async def check_availability(self, proxy_type: str, country_code: str, quantity: int) -> tuple[bool, int]:
        """
        Checks the availability of the required number of proxies.
        Returns: (True/False, available quantity)
        """
        params = {
            "type": proxy_type,
            "country": country_code,
            "quantity": quantity
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"{self.base_url}/availability", params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return data.get("available", False), data.get("available_quantity", 0), True
                    return False, 0
        except ClientError as e:
            logger.error(f"API request failed: {e}")

        return False, 0, False

