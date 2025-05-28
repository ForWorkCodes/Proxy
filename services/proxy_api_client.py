from aiohttp import ClientSession, ClientError
from typing import List
from typing import Optional
from config import API_BASE_URL
from aiogram.fsm.context import FSMContext
from data.locales import get_text
import logging
import re
from dtos.user_dto import UserUpsertDTO
from dtos.proxy_dto import ProxyAvailabilityDTO, ProxyAvailabilityResponse, ProxyGetPriceDTO,\
    ProxyGetPriceResponse, ProxyProcessBuyingDTO, ProxyProcessBuyingResponse, ProxyUsersListResponse, ProxyItem

logger = logging.getLogger(__name__)
ADDRESS_REGEX = re.compile(r"^\d{1,3}(\.\d{1,3}){3}:\d{1,5}$")


class ProxyAPIClient:
    def __init__(self):
        self.base_url = API_BASE_URL

    async def get_countries(self, proxy_version: str) -> List[str]:
        """
        Fetch country codes from API for a given proxy type
        """
        params = {"version": proxy_version}

        try:
            async with ClientSession() as session:
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

    async def get_country_dict(self, state: FSMContext) -> dict:
        """
        Returns a dictionary of the form: {'US': 'United States', 'DE': 'Germany', ...}
        with the user's locale.
        """
        data = await state.get_data()
        proxy_version = data.get("proxy_version")
        if not proxy_version:
            raise ValueError(await get_text(state, "proxy_type_not_selected_error"))

        country_codes = await self.get_countries(proxy_version)
        return {
            code: await self.get_country_name(state, code)
            for code in country_codes
        }

    async def check_availability(self, dto: ProxyAvailabilityDTO) -> ProxyAvailabilityResponse:
        """
        Checks the availability of the required number of proxies.
        Returns: (True/False, available quantity)
        """

        try:
            async with ClientSession() as session:
                async with session.get(f"{self.base_url}/availability", params=dto.dict()) as response:
                    if response.status == 200:
                        data = await response.json()
                        return ProxyAvailabilityResponse(
                            success=True,
                            available=data.get("available", False),
                            available_quantity=data.get("available_quantity", 0)
                        )
        except ClientError as e:
            logger.error(f"API request failed: {e}")

        return ProxyAvailabilityResponse(
            success=False,
            available=False,
            available_quantity=0
        )

    async def check_price(self, dto: ProxyGetPriceDTO) -> ProxyGetPriceResponse:
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.base_url}/get_price", params=dto.dict()) as response:
                    if response.status == 200:
                        data = await response.json()
                        return ProxyGetPriceResponse(
                            success=True,
                            available=True if data.get("total_price") else False,
                            total_price=data.get("total_price", 0)
                        )
        except ClientError as e:
            logger.error(f"API request failed: {e}")

        return ProxyGetPriceResponse(
            success=False,
            available=False,
            total_price=0
        )

    async def process_buying_proxy(self, dto: ProxyProcessBuyingDTO) -> ProxyProcessBuyingResponse:
        status_code = 404
        error = ""
        try:
            async with ClientSession() as session:
                async with session.post(f"{self.base_url}/buy_proxy", json=dto.dict()) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            raw_list = data.get("proxies", [])
                            proxy_items = [ProxyItem(**item) for item in raw_list]
                            return ProxyProcessBuyingResponse(
                                success=True,
                                status_code=0,
                                error="",
                                quantity=data.get("quantity"),
                                price=data.get("price"),
                                days=data.get("days"),
                                country=data.get("country"),
                                list=proxy_items
                            )
                        else:
                            status_code = data.get("status_code")
                            error = data.get("error")
        except ClientError as e:
            error = f"API request failed: {e}"
            logger.error(f"API request failed: {e}")

        return ProxyProcessBuyingResponse(
            success=False,
            status_code=status_code,
            error=error,
            quantity=0,
            price=0,
            days=0,
            country="",
            list=[]
        )

    async def get_my_list_proxy(self, telegram_id: int) -> ProxyUsersListResponse:
        status_code = 404
        try:
            async with ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/get-proxy-telegram-id",
                        json={"telegram_id": str(telegram_id)}
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if data.get("success"):
                            raw_list = data.get("proxies", [])
                            proxy_items = [ProxyItem(**item) for item in raw_list]
                            return ProxyUsersListResponse(
                                success=True,
                                status_code=0,
                                error="",
                                list=proxy_items
                            )
                        else:
                            status_code = data.get("status_code")
                            error = data.get("error")
        except ClientError as e:
            error = f"API request failed: {e}"
            logger.error(f"API request failed: {e}")

        return ProxyUsersListResponse(
            success=False,
            status_code=status_code,
            error=error,
            list=[]
        )

    async def check_my_proxy(self, telegram_id: int, address: str):
        if not ADDRESS_REGEX.match(address):
            return {
                "success": False,
                "status_code": 400,
                "error": "Invalid address format. Expected IP:PORT"
            }

        try:
            async with ClientSession() as session:
                async with session.post(
                        f"{self.base_url}/checker-proxy",
                        json={"telegram_id": str(telegram_id), "address": address}
                ) as response:
                    if response.status == 200:
                        return await response.json()
                    else:
                        return {
                            "success": False,
                            "status_code": response.status,
                            "error": "Server returned error"
                        }
        except ClientError as e:
            return {
                "success": False,
                "status_code": 500,
                "error": f"Request failed: {e}"
            }

    async def get_user(self, telegram_id: int) -> Optional[dict]:
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.base_url}/user/by-telegram-id/{str(telegram_id)}") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except ClientError as e:
            logger.error(f"API error in get_user: {e}")
            return None

    async def get_balance(self, telegram_id: int) -> Optional[dict]:
        try:
            async with ClientSession() as session:
                async with session.get(f"{self.base_url}/user/get_balance/{str(telegram_id)}") as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except ClientError as e:
            logger.error(f"API error in get_user: {e}")
            return None

    async def upsert_user(self, dto: UserUpsertDTO) -> Optional[dict]:
        try:
            async with ClientSession() as session:
                async with session.post(f"{self.base_url}/user/upsert", json=dto.dict()) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return None
        except ClientError as e:
            logger.error(f"API error in upsert_user: {e}")
            return None

    async def update_language(self, telegram_id: int, lang: str):
        try:
            async with ClientSession() as session:
                await session.patch(
                    f"{self.base_url}/user/{telegram_id}/language",
                    json={"language": lang}
                )
        except ClientError as e:
            logger.error(f"API error in update_language: {e}")

    async def update_notification(self, telegram_id: int, notification: bool):
        try:
            async with ClientSession() as session:
                await session.patch(
                    f"{self.base_url}/user/{telegram_id}/notification",
                    json={"notification": notification}
                )
        except ClientError as e:
            logger.error(f"API error in update_notification: {e}")
