import asyncio
from cgitb import text
from turtle import delay
from aiogram import Bot, Dispatcher, executor, types
from config import token, user_id
import json
from aiogram.utils.markdown import hbold, hlink
from main import check_news


bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)


@dp.message_handler(commands='start')
async def start(message: types.Message):
    await message.reply("Чо каво?")

@dp.message_handler(commands="all_news")
async def get_all_news(message:types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        
    for k, v in sorted(news_dict.items()):
        # news = f"<b>{v['article_title']}</b>\n" \
        #        f"{v['article_desc']}\n" \
        #        f"{v['article_url']}\n" 
        # news = f"{hbold(v['article_title'])}\n" \
        #        f"{v['article_desc']}\n" \
        #        f"{hlink(v['article_desc'], v['article_url'])}" 
        
        news = f"<b>{hlink(v['article_title'], v['article_url'])}</b>\n" \
                        
        await message.answer(news)
        
        
@dp.message_handler(commands="last_five")
async def get_last_five_news(message:types.Message):
    with open("news_dict.json") as file:
        news_dict = json.load(file)
        
    for k, v in sorted(news_dict.items())[-5:]:    
        news = f"<b>{hlink(v['article_title'], v['article_url'])}</b>\n"                        
        await message.answer(news)
        
        
        
@dp.message_handler(commands="fresh_news")
async def get_last_five_news(message:types.Message):
    fresh_news = check_news()
    
    if len(fresh_news) >= 1:
        for k, v in sorted(fresh_news.items()):    
            news = f"<b>{hlink(v['article_title'], v['article_url'])}</b>\n"                        
            await message.answer(news) 
    else:
        await message.answer('No fresh news')  
        
async def news_every_minute():
    while True:
        fresh_news = check_news()
        
        if len(fresh_news) >= 1:
            for k, v in sorted(fresh_news.items()):    
                news = f"<b>{hlink(v['article_title'], v['article_url'])}</b>\n"                        
                await bot.send_message(user_id, news)
        else:
            await bot.send_message(user_id, "No news")
        
        await asyncio.sleep(120)     
                

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(news_every_minute())
    executor.start_polling(dp)

