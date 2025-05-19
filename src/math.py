import asyncio
import logging
import os
import json
import aiohttp
import random
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, BaseFilter, Command
from aiogram.enums import ContentType
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import re
import base64

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
load_dotenv(override=True)
TELEGRAM_BOT_TOKEN = "7227343484:AAFf72XqB8VRAs1JAH-kTcSZtvsvQZpi8XI"
OPENROUTER_API_KEY = "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"

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher()

# Regex for detecting mathematical expressions
MATH_REGEX = re.compile(r'[\d+\-*/=^()\[\]{}√π∞∑∫∮∝≠≤≥≈]', re.UNICODE)

# Custom filter for photo content type
class PhotoFilter(BaseFilter):
    async def __call__(self, message: types.Message) -> bool:
        return message.content_type == ContentType.PHOTO

# Learning topics
TOPICS = {
    "linear": "Решение линейных уравнений",
    "quadratic": "Решение квадратных уравнений",
    "cubic": "Решение уравнений 3-й степени",
    "integrals": "Решение интегралов",
    "fractions": "Операции с дробями",
    "exponential": "Решение экспоненциальных уравнений",
    "logarithms": "Решение логарифмических уравнений"
}

# Store user states for learning mode
USER_STATES = {}

def clean_latex(text: str) -> str:
    """Remove LaTeX symbols and simplify mathematical expressions."""
    text = re.sub(r'\\[\(\[]|\\[\)\]]', '', text)
    text = re.sub(r'\^{([^}]+)}', r'^\1', text)
    text = re.sub(r'\\frac{([^}]+)}{([^}]+)}', r'\1/\2', text)
    text = re.sub(r'\\sqrt{([^}]+)}', r'sqrt(\1)', text)
    text = text.replace(r'\cdot', '*').replace(r'\times', '*')
    text = text.replace('\\', '')
    return text.strip()

async def invoke_llm_api(user_content, image_data=None) -> str:
    """Calls the OpenRouter API with text or image and returns the response."""
    if not OPENROUTER_API_KEY:
        return "Ошибка: Токен OPENROUTER_API_KEY не найден в .env"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("REFERER_URL", "http://localhost"),
        "X-Title": os.getenv("TITLE_NAME", "Math Telegram Bot")
    }

    # Updated system prompt for answer-first format
    system_prompt = """Ты решаешь только математические задачи.
    Формат ответа: 
    Ответ: [число или числа, например, 2 или 1.1]
    Решение: [пошаговое объяснение]
    Общий ответ (Ответ + Решение) должен быть короче 100 символов.
    Не используй LaTeX (например, \(, \), x^{2}). 
    Пиши в текстовом формате (x^2, sqrt(x), a/b)."""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_content}
    ]

    if image_data:
        messages[1]["content"] = [
            {"type": "text", "text": user_content},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_data}"}
        ]

    body = {
        "model": "qwen/qwen-2-vl-7b-instruct",
        "messages": messages,
        "stream": False,
        "max_tokens": 512,
        "temperature": 0.7
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=body) as response:
                if response.status != 200:
                    error_text = await response.text()
                    logging.error(f"API request failed: {response.status}, {error_text}")
                    return f"Ошибка API: {response.status}"
                response_data = await response.json()
                if response_data.get("choices") and response_data["choices"][0].get("message"):
                    response_text = response_data["choices"][0]["message"]["content"]
                    return clean_latex(response_text)
                return "Не удалось получить ответ."
    except Exception as e:
        logging.error(f"API error: {e}")
        return "Ошибка при обращении к API."

async def download_image(file_id: str) -> str:
    """Downloads an image and returns its base64 encoding."""
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file.file_path}"
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                image_data = await response.read()
                return base64.b64encode(image_data).decode("utf-8")
            logging.error(f"Failed to download image: {response.status}")
            return None

def generate_examples(topic: str) -> list:
    """Generates 3 unique examples for the given topic with increasing difficulty."""
    examples = []
    answers = []
    
    if topic == "linear":
        for i in range(1, 4):
            a = random.randint(i, i * 2)  
            b = random.randint(-i * 5, i * 5)
            c = random.randint(-i * 5, i * 5)
            x = random.randint(-10, 10)  
            d = a * x + b - c  
            example = f"{a}x + {b} = {c} + {d}"
            examples.append(example)
            answers.append(str(x))
    
    elif topic == "quadratic":
        for i in range(1, 4):
            a = random.randint(1, i)
            x = random.randint(-5, 5)
            c = random.randint(-i * 5, i * 5)
            b = -2 * a * x 
            example = f"{a}x^2 + {b}x + {c} = 0"
            examples.append(example)
            answers.append(str(x))
    
    elif topic == "cubic":
        for i in range(1, 4):
            a = random.randint(1, i)
            x = random.randint(-3, 3)
            b = random.randint(-i * 3, i * 3)
            c = random.randint(-i * 5, i * 5)
            d = -a * x**3 - b * x**2 - c * x  
            example = f"{a}x^3 + {b}x^2 + {c}x + {d} = 0"
            examples.append(example)
            answers.append(str(x))
    
    elif topic == "integrals":
        for i in range(1, 4):
            a = random.randint(1, i)
            n = random.randint(1, i)  
            c = random.randint(-i, i)
            example = f"∫ ({a}x^{n} + {c}) dx"
            answers.append(f"{a/(n+1)}x^{n+1} + {c}x + C")
    
    elif topic == "fractions":
        for i in range(1, 4):
            a = random.randint(1, i * 2)
            b = random.randint(1, i * 2)
            c = random.randint(1, i * 2)
            d = random.randint(1, i * 2)
            ans = (a * d + b * c) / (b * d)  
            if ans.is_integer() or abs(ans - round(ans, 1)) < 0.01:
                example = f"({a}/{b}) + ({c}/{d})"
                examples.append(example)
                answers.append(str(round(ans, 1)))
    
    elif topic == "exponential":
        for i in range(1, 4):
            base = random.choice([2, 3, 4])
            x = random.randint(1, i)
            example = f"{base}^x = {base**x}"
            examples.append(example)
            answers.append(str(x))
    
    elif topic == "logarithms":
        for i in range(1, 4):
            base = random.choice([2, 3, 10])
            x = random.randint(1, i)
            example = f"log_{base}({base**x}) = ?"
            examples.append(example)
            answers.append(str(x))
    
    return [{"example": ex, "answer": ans} for ex, ans in zip(examples, answers)]

def create_topics_keyboard() -> InlineKeyboardMarkup:
    """Creates an inline keyboard with learning topics."""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for topic_id, topic_name in TOPICS.items():
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=topic_name, callback_data=f"topic_{topic_id}")]
        )
    return keyboard

def create_main_keyboard() -> ReplyKeyboardMarkup:
    """Creates a reply keyboard with 'Обучение' and 'Решение примеров' buttons."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Обучение"), KeyboardButton(text="Решение примеров")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

@dp.message(CommandStart())
async def send_welcome(message: types.Message):
    """Handles the /start command."""
    keyboard = create_main_keyboard()
    await message.reply(
        "Добро пожаловать в MathBot - ваш помощник в решении примеров! "
        "Этот бот поможет вам освоить математику, решить уравнения и проверить свои знания. "
        "Отправьте выражение, фото или выберите действие ниже:",
        reply_markup=keyboard
    )

@dp.message(lambda message: message.text == "Обучение")
async def learn_command(message: types.Message):
    """Handles the 'Обучение' button to show topics."""
    keyboard = create_topics_keyboard()
    await message.reply("Выбери тему для обучения:", reply_markup=keyboard)

@dp.message(lambda message: message.text == "Решение примеров")
async def solve_examples(message: types.Message):
    """Handles the 'Решение примеров' button."""
    keyboard = create_main_keyboard()
    await message.reply(
        "Отправь математическое выражение или фото с задачей 🧮.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("topic_"))
async def process_topic_selection(callback: types.CallbackQuery):
    """Handles topic selection and sends 3 examples."""
    topic_id = callback.data.split("_")[1]
    if topic_id not in TOPICS:
        await callback.message.reply("Неверная тема.")
        return

    examples = generate_examples(topic_id)
    USER_STATES[callback.from_user.id] = {"topic": topic_id, "examples": examples}
    
    message_text = f"Тема: {TOPICS[topic_id]}\n\n"
    for i, ex in enumerate(examples, 1):
        message_text += f"{i}) {ex['example']}\n"
    message_text += "\nОтправь ответы в формате:\n1) ответ\n2) ответ\n..."

    keyboard = create_main_keyboard()
    await callback.message.reply(message_text, reply_markup=keyboard)
    await callback.answer()

@dp.message(PhotoFilter())
async def handle_photo(message: types.Message):
    """Handles photo messages with mathematical problems."""
    processing_message = await message.reply("Обрабатываю фото... 📷")
    photo = message.photo[-1]
    image_base64 = await download_image(photo.file_id)

    if not image_base64:
        await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)
        await message.reply("Не удалось загрузить фото.")
        return

    response_text = await invoke_llm_api("Решите задачу на изображении.", image_base64)
    await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)

    keyboard = create_main_keyboard()
    if response_text:
        for i in range(0, len(response_text), 4096):
            await message.reply(response_text[i:i+4096], reply_markup=keyboard)
    else:
        await message.reply("Не удалось обработать задачу.", reply_markup=keyboard)

@dp.message()
async def handle_message(message: types.Message):
    """Handles incoming messages."""
    user_id = message.from_user.id
    keyboard = create_main_keyboard()

    
    if user_id in USER_STATES and message.text:
        examples = USER_STATES[user_id]["examples"]
        answers = re.findall(r'(\d+)\)\s*([\d\.\-]+)', message.text)
        response_text = "Результаты:\n"

        for num, user_answer in answers:
            num = int(num) - 1
            if num < len(examples):
                correct_answer = examples[num]["answer"]
                if user_answer == correct_answer:
                    response_text += f"{num + 1}) Правильно: {correct_answer}\n"
                else:
                    response_text += f"{num + 1}) Неправильно. Ответ: {correct_answer}\n"
                    # Генерирование объясненения
                    explanation = await invoke_llm_api(
                        f"Объясни кратко, как решить: {examples[num]['example']}. Ответ: {correct_answer}"
                    )
                    response_text += f"Объяснение: {explanation}\n"
        
        del USER_STATES[user_id]
        await message.reply(response_text, reply_markup=keyboard)
        return

   
    if not message.text or not MATH_REGEX.search(message.text):
        await message.reply(
            "Отправь математическое выражение или выбери действие 🧮",
            reply_markup=keyboard
        )
        return

    processing_message = await message.reply("Решаю задачу...")
    response_text = await invoke_llm_api(message.text)
    await bot.delete_message(chat_id=processing_message.chat.id, message_id=processing_message.message_id)

    if response_text:
        for i in range(0, len(response_text), 4096):
            await message.reply(response_text[i:i+4096], reply_markup=keyboard)
    else:
        await message.reply("Не удалось решить задачу.", reply_markup=keyboard)

async def main():
    """Starts the bot."""
    if not TELEGRAM_BOT_TOKEN:
        logging.error("Telegram bot token not found.")
        return
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
