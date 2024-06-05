from aiogram import F, types, Router
from aiogram.filters import CommandStart

from sqlalchemy.ext.asyncio import AsyncSession
from database.orm_query import (
    orm_add_to_cart,
    orm_add_user,
)

from filters.chat_types import ChatTypeFilter
from handlers.menu_processing import get_menu_content
from kbds.inline import MenuCallBack, get_callback_btns, get_user_cart
from handlers.menu_processing import carts
from database.orm_query import (
    orm_change_banner_image,
    orm_get_categories,
    orm_add_product,
    orm_delete_product,
    orm_get_info_pages,
    orm_get_product,
    orm_get_products,
    orm_update_product,
)

user_private_router = Router()
user_private_router.message.filter(ChatTypeFilter(["private"]))

# Проверка ID админа
# @user_private_router.message(F.text == "start")
# async def start_cmd(message: types.Message):
#     print(message.from_user.id)

@user_private_router.message(CommandStart())
async def start_cmd(message: types.Message, session: AsyncSession):
    print(message.from_user.id)
    media, reply_markup = await get_menu_content(session, level=0, menu_name="main")

    await message.answer_photo(media.media, caption=media.caption, reply_markup=reply_markup)


async def add_to_cart(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    print(callback_data)
    print('корзина')
    user = callback.from_user
    await orm_add_user(
        session,
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        phone=None,
    )
    await orm_add_to_cart(session, user_id=user.id, product_id=callback_data.product_id)
    await callback.answer("Товар добавлен в корзину.")
    await callback.message.edit_reply_markup()


@user_private_router.callback_query(MenuCallBack.filter())
async def user_menu(callback: types.CallbackQuery, callback_data: MenuCallBack, session: AsyncSession):
    print(callback_data)
    print('тут')

    if callback_data.menu_name == "add_to_cart":
        await add_to_cart(callback, callback_data, session)
        return

    media, reply_markup = await get_menu_content(
        session,
        level=callback_data.level,
        menu_name=callback_data.menu_name,
        category=callback_data.category,
        page=callback_data.page,
        product_id=callback_data.product_id,
        user_id=callback.from_user.id,
    )
    print(media, reply_markup)

    if callback_data.category != None:
        for product in await orm_get_products(session, int(callback_data.category)):
            print(f'проверка {product.id}')
            media, reply_markup = await get_menu_content(
                session,
                level=callback_data.level,
                menu_name=callback_data.menu_name,
                category=callback_data.category,
                page=callback_data.page,
                product_id=product.id,
                user_id=callback.from_user.id,
            )
            print(media, reply_markup)
            await callback.message.answer_video(
                video=product.image,
                caption=f"<strong>{product.name}\
                                </strong>\n{product.description}\nСтоимость: {round(product.price, 2)}\n\
                                 номер {product.id}"
                , reply_markup=reply_markup)
            await callback.answer('fdfd')

    else:
        await callback.message.edit_media(media=media, reply_markup=reply_markup)
        await callback.answer()


