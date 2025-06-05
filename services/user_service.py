from utils.i18n import resolve_language
from aiogram.fsm.context import FSMContext
from services.proxy_api_client import ProxyAPIClient
from dtos.user_dto import UserUpsertDTO

proxy_api_client = ProxyAPIClient()


class UserService:

    def __init__(self):
        self.proxy_api_client = ProxyAPIClient()

    async def create_user(self, user_id: int, message, state: FSMContext) -> dict:
        data = await state.get_data()
        if "user" in data:
            print("Пользователь получен из кэша", data["user"])
            return data["user"]

        resolved_lang = resolve_language(message.from_user.language_code)
        user_db = await self.proxy_api_client.get_user(user_id)

        if user_db:
            print("Пользователь найден в базе данных")
            user = {
                "user_id": user_db['telegram_id'],
                "username": user_db['username'],
                "firstname": user_db['firstname'],
                "language": user_db['language'],
                "notification": user_db['notification'],
                "active": user_db['active'],
                "banned": user_db['banned']
            }
        else:
            print("Пользователь не найден в базе данных")
            dto = UserUpsertDTO(
                telegram_id=str(user_id),
                chat_id=str(message.chat.id),
                username=message.from_user.username,
                firstname=message.from_user.first_name,
                language=resolved_lang,
                active=True,
                banned=False,
                notification=False
            )
            user = await self.proxy_api_client.upsert_user(dto)

            if user is None:
                await message.answer("⚠️ Error creating user. Please try again later.")
                print("❌ Критическая ошибка: не удалось создать пользователя")
                return

        print("-----------------------------")
        print(user)
        print("-----------------------------")

        await state.update_data(user=user)
        return user

    async def update_user_language(self, user_id: int, lang: str, state: FSMContext) -> None:
        await self.proxy_api_client.update_language(user_id, lang)
        data = await state.get_data()

        if "user" in data:
            user = data["user"]
            user["language"] = lang
            print("language updated: ", lang)
            await state.update_data(user=user)

    async def update_user_notification(self, user_id: int, notification: bool, state: FSMContext) -> None:
        await self.proxy_api_client.update_notification(user_id, notification)
        data = await state.get_data()

        if "user" in data:
            user = data["user"]
            user["notification"] = notification
            print("notification updated: ", notification)
            await state.update_data(user=user)

    async def get_balance(self, user_id: int) -> dict:
        user = await proxy_api_client.get_balance(user_id)

        if not user or "amount" not in user:
            return {
                "success": False
            }

        amount = round(float(user["amount"]), 1)
        return {
            "success": True,
            "balance": amount,
            "currency": "RUB"
        }