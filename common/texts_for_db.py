from aiogram.utils.formatting import Bold, as_list, as_marked_section


categories = ['100-300', '301-500', "501-1000"]

description_for_info_pages = {
    "main": "Добро пожаловать!",
    "about": "Игрушки на 3Д принтере",
    "payment": as_marked_section(
        Bold("Варианты оплаты:"),
        'перевод по ссылке На тинькофф банк',
        'наличкой',
        marker="✅ ",
    ).as_html(),
    "shipping": as_list(
        as_marked_section(
            Bold("Варианты доставки/заказа:"),
            "Курьер",
            "Самовынос (заберу на работе)",
            marker="✅ ",
        ),
        as_marked_section(Bold("Нельзя:"), "Почта", "Голуби", marker="❌ "),
        sep="\n----------------------\n",
    ).as_html(),
    'catalog': 'Категории:',
    'cart': 'В корзине ничего нет!'
}
