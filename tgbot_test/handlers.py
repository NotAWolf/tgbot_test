from telegram import Update, Chat
from typing import cast
from telegram.ext import ContextTypes
import bot_messeges
from test_parser import get_all_dicounts


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, response=bot_messeges.GREETINGS)


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, response=bot_messeges.HELP)


async def allshops(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_response(update, context, response=bot_messeges.SHOPS)


async def alldiscounts(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    discounts = get_all_dicounts()
    for shop in discounts:
        response = shop.name

        for product in shop.products:
            if user_message.lower() in product.name.lower():
                response +='\n' + product.name + ' ' + str(product.price)
        
        if response == shop.name:
            response += bot_messeges.NOT_FOUND
        await send_response(update, context, response=response)


async def send_response(update: Update,
                  context: ContextTypes.DEFAULT_TYPE,
                  response: str) -> None:
    args = {"chat_id": _get_chat_id(update), "text": response}
    await context.bot.send_message(**args)


def _get_chat_id(update: Update) -> int:
    return cast(Chat, update.effective_chat).id
