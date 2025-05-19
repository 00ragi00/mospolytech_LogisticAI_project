# Создание Telegram Math Bot: Техническое руководство для новичков

Этот документ описывает руководство по созданию MathBot — Telegram-бота, который поможет вам решать математические задачи с использованием нейронной сети Qwen2.5-VL 7B Instruct. Этот бот умеет решать текстовые уравнения, обрабатывать фотографии с задачами, а также обучать пользователей через интерактивные примеры. Мы создадим проект с нуля, объясняя каждый шаг максимально подробно для новичков. Также добавим схемы на русском языке, которые помогут понять архитектуру и процессы.

---

## Содержание

1. [Что вам понадобится](#что-вам-понадобится)
2. [Установка программного обеспечения](#установка-программного-обеспечения)
3. [Создание проекта](#создание-проекта)
4. [Написание кода MathBot](#написание-кода-mathbot)
5. [Настройка API и токенов](#настройка-api-и-токенов)
6. [Запуск и тестирование бота](#запуск-и-тестирование-бота)
7. [Что делать, если что-то не работает](#что-делать-если-что-то-не-работает)
8. [Как улучшить бота](#как-улучшить-бота)
9. [Заключение](#заключение)

---

## Что вам понадобится

Прежде чем начать, убедитесь, что у вас есть следующее:

- Компьютер с операционной системой: Windows, macOS или Linux.
- Интернет: Для загрузки программ и работы с API.
- Аккаунт в Telegram: Чтобы создать бота.
- Текстовый редактор: Например, Visual Studio Code (бесплатный, скачайте [здесь](https://code.visualstudio.com/)) или любой другой, например, Блокнот.
- Базовые навыки работы с компьютером: Умение открывать терминал, создавать файлы и папки.

---

## Установка программного обеспечения

### Шаг 1: Установите Python
1. Проверьте, установлен ли Python. Откройте терминал (на Windows — cmd или PowerShell, на macOS/Linux — терминал) и введите:
      python --version
   
   Если Python не установлен или версия ниже 3.9, скачайте его с [официального сайта](https://www.python.org/downloads/). Рекомендуем версию 3.11.
2. Во время установки отметьте галочку "Add Python to PATH" (добавить Python в переменную окружения), чтобы команды python и pip работали из терминала.

3. После установки проверьте версию Python и pip (инструмент для установки библиотек):
      python --version
   pip --version
   

### Шаг 2: Установите виртуальное окружение
Виртуальное окружение — это изолированная "песочница", где мы будем устанавливать библиотеки для нашего проекта, чтобы они не конфликтовали с другими проектами.

1. Установите virtualenv, если его нет:
      pip install virtualenv
   
2. Создайте папку для проекта:
      mkdir MathBotProject
   cd MathBotProject
   
   - mkdir MathBotProject создает папку с названием MathBotProject.
   - cd MathBotProject переходит в эту папку.

3. Создайте виртуальное окружение:
      virtualenv venv
   
   Это создаст папку venv внутри MathBotProject.

4. Активируйте виртуальное окружение:
   - На Windows:
          venv\Scripts\activate
     
   - На macOS/Linux:
          source venv/bin/activate
     
   После активации в начале строки терминала появится (venv) — это значит, что вы находитесь в виртуальном окружении.

### Шаг 3: Установите необходимые библиотеки
Теперь установим библиотеки, которые нужны для работы бота. Убедитесь, что виртуальное окружение активировано (видите (venv) в терминале), и выполните:
pip install aiogram aiohttp python-dotenv
- aiogram — библиотека для работы с Telegram API (создание бота).
- aiohttp — для отправки запросов к API нейронной сети.
- python-dotenv — для работы с файлом .env, где будут храниться секретные ключи.

---

## Создание проекта

### Шаг 1: Создайте структуру проекта
Внутри папки MathBotProject создайте следующую структуру:

MathBotProject/<br>
│<br>
├── venv/              **Виртуальное окружение (уже создано)**<br>
├── math.py            **Файл с кодом бота**<br>
└── .env               **Файл с секретными ключами**<br>

1. Создайте файл math.py:
   - Если вы используете Visual Studio Code, откройте папку MathBotProject в редакторе, нажмите правой кнопкой мыши в обозревателе файлов и выберите "New File" → назовите его math.py.
   - Или создайте файл через терминал:
          touch math.py  # На macOS/Linux
     echo > math.py  # На Windows
     

2. Создайте файл .env таким же образом:
      touch .env  # На macOS/Linux
   echo > .env  # На Windows
   

### Шаг 2: Получите Telegram Bot Token
1. Откройте Telegram и найдите бота @BotFather (введите в поиске @BotFather).
2. Напишите /start, затем /newbot.
3. Следуйте инструкциям:
   - Введите имя бота, например, MyMathBot.
   - Введите username бота, заканчивающийся на Bot, например, MyMathBot123Bot.
4. После создания BotFather даст вам токен, например:
   
   5338343211:BAGn72BqH98VRAsIJON-mZtTVmqszIOpi8AI
   
   Скопируйте этот токен, он понадобится позже.

![1](https://github.com/user-attachments/assets/4647a94c-e975-4f77-872c-3336db8d7b48)


### Шаг 3: Получите OpenRouter API ключ
1. Перейдите на сайт [openrouter.ai](https://openrouter.ai) и зарегистрируйтесь.
2. После регистрации зайдите в раздел "API Keys" (Ключи API).
3. Создайте новый ключ и скопируйте его, например:
   
   sk-or-v1-wergwregwrg5468fgnrfgn6869i123sdbvdsf845rdftgn
   
   Этот ключ даст доступ к модели Qwen2.5-VL 7B Instruct.

![2](https://github.com/user-attachments/assets/2251f2a9-577f-4e8a-8a73-3eeb45ca02ec)


### Шаг 4: Настройте файл .env
Откройте файл .env в текстовом редакторе (например, Visual Studio Code или Блокнот) и вставьте туда следующие строки:

    TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
    OPENROUTER_API_KEY=ваш_ключ_от_OpenRouter
    REFERER_URL=http://localhost
    TITLE_NAME=Math Telegram Bot
    
- Замените ваш_токен_от_BotFather на токен, полученный от BotFather.
- Замените ваш_ключ_от_OpenRouter на ключ от OpenRouter.
- REFERER_URL и TITLE_NAME оставьте как есть — они нужны для API.

Сохраните файл .env.

![3](https://github.com/user-attachments/assets/be03f06f-5c0e-4b64-ad51-7af52755ce4e)


---

## Написание кода MathBot

Теперь мы создадим файл math.py с нуля. Откройте файл math.py в текстовом редакторе и добавляйте код по частям, следуя объяснениям.

![4](https://github.com/user-attachments/assets/5a31e599-76eb-4ae7-8016-2229a0d8d78a)


### Шаг 1: Импортируем библиотеки
Начнем с импорта необходимых библиотек. Добавьте в начало файла math.py:

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
    import base64<br>
Объяснение:
- asyncio — для асинхронного выполнения (бота обрабатывает много запросов одновременно).
- logging — для записи логов (чтобы видеть ошибки).
- os и json — для работы с файлами и данными.
- aiohttp — для отправки запросов к API.
- random — для генерации случайных примеров.
- load_dotenv — для чтения .env.
- aiogram — для создания Telegram-бота.
- re — для работы с регулярными выражениями (поиск математических символов).
- base64 — для обработки изображений.

### Шаг 2: Настройка логирования и загрузка переменных
Добавьте следующий код:
# Настройка логирования
    logging.basicConfig(level=logging.INFO)

# Загрузка переменных окружения
    load_dotenv(override=True)
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# Инициализация бота и диспетчера
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
Объяснение:
- logging.basicConfig(level=logging.INFO) — включает логирование, чтобы видеть сообщения об ошибках.
- load_dotenv() — загружает данные из .env.
- os.getenv() — получает токены из .env.
- Bot и Dispatcher — создают бота и диспетчер для обработки сообщений.

### Шаг 3: Определение регулярного выражения для математики
Добавьте код для поиска математических выражений:
# Регулярное выражение для математических выражений
    MATH_REGEX = re.compile(r'[\d+\-*/=^()\[\]{}√π∞∑∫∮∝≠≤≥≈]', re.UNICODE)
Объяснение:
- MATH_REGEX ищет в тексте символы, которые могут быть частью математического выражения, например, числа, знаки +, -, или специальные символы вроде √.

### Шаг 4: Фильтр для фотографий
Создадим фильтр, чтобы бот понимал, что пользователь отправил фото:
# Фильтр для фотографий
    class PhotoFilter(BaseFilter):
        async def __call__(self, message: types.Message) -> bool:
            return message.content_type == ContentType.PHOTO
Объяснение:
- PhotoFilter проверяет, является ли сообщение фотографией, чтобы бот мог обрабатывать изображения отдельно.

### Шаг 5: Темы для обучения
Определим темы для режима обучения:
# Темы для обучения

    TOPICS = {
          "linear": "Решение линейных уравнений",
          "quadratic": "Решение квадратных уравнений",
          "cubic": "Решение уравнений 3-й степени",
          "integrals": "Решение интегралов",
          "fractions": "Операции с дробями",
          "exponential": "Решение экспоненциальных уравнений",
          "logarithms": "Решение логарифмических уравнений"
}

# Хранение состояния пользователей
    USER_STATES = {}
Объяснение:
- TOPICS — словарь с темами, которые пользователь может выбрать в режиме обучения.
- USER_STATES — словарь для хранения текущего состояния пользователя (например, какие примеры он решает).

### Шаг 6: Удаление LaTeX-форматирования

Добавим функцию для очистки ответа от LaTeX-символов:

    def clean_latex(text: str) -> str:
    """Удаляет LaTeX-символы и упрощает математические выражения."""

    text = re.sub(r'\\[\(\[]|\\[\)\]]', '', text)
    text = re.sub(r'\^{([^}]+)}', r'^\1', text)
    text = re.sub(r'\\frac{([^}]+)}{([^}]+)}', r'\1/\2', text)
    text = re.sub(r'\\sqrt{([^}]+)}', r'sqrt(\1)', text)
    text = text.replace(r'\cdot', '*').replace(r'\times', '*')
    text = text.replace('\\', '')
    return text.strip()<br>
Объяснение:
- Эта функция убирает LaTeX-форматирование (например, \frac{a}{b} превращается в a/b), чтобы ответы были проще для чтения.

### Шаг 7: Запрос к API нейронной сети
Добавим функцию для отправки запросов к OpenRouter API:

    async def invoke_llm_api(user_content, image_data=None) -> str:

    """Отправляет запрос к OpenRouter API и возвращает ответ."""
    
    if not OPENROUTER_API_KEY:
        return "Ошибка: Токен OPENROUTER_API_KEY не найден в .env"

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": os.getenv("REFERER_URL", "http://localhost"),
        "X-Title": os.getenv("TITLE_NAME", "Math Telegram Bot")
    }

    # Системный промпт для формата ответа
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
Объяснение:
- Эта функция отправляет запрос к OpenRouter API с текстом или изображением.
- system_prompt указывает модели, как форматировать ответ (сначала ответ, потом решение, в пределах 100 символов).
- Если передан image_data, запрос включает изображение в формате base64.
- Ответ очищается от LaTeX через clean_latex.

### Шаг 8: Загрузка изображений
Добавим функцию для загрузки изображений из Telegram:

    async def download_image(file_id: str) -> str:
    
Скачивает изображение из Telegram и возвращает его в формате base64.
    
    file = await bot.get_file(file_id)
    file_url = f"https://api.telegram.org/file/bot{TELEGRAM_BOT_TOKEN}/{file.file_path}"
    async with aiohttp.ClientSession() as session:
        async with session.get(file_url) as response:
            if response.status == 200:
                image_data = await response.read()
                return base64.b64encode(image_data).decode("utf-8")
            logging.error(f"Failed to download image: {response.status}")
            return None<br>
Объяснение:
- Функция получает изображение по его file_id, скачивает его и преобразует в base64 для отправки в API.

### Шаг 9: Генерация примеров для обучения
Добавим функцию для создания примеров:

    def generate_examples(topic: str) -> list:
    
Генерирует 3 уникальных примера для выбранной темы с возрастающей сложностью.
    
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
Объяснение:
- Функция создает 3 примера для каждой темы.
- Сложность возрастает за счет увеличения коэффициентов или степени.
- Ответы — целые числа или простые десятичные (например, 1.1).

### Шаг 10: Создание клавиатур
Добавим функции для создания клавиатур:

    def create_topics_keyboard() -> InlineKeyboardMarkup:
    
Создает инлайн-клавиатуру с темами для обучения.

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for topic_id, topic_name in TOPICS.items():
        keyboard.inline_keyboard.append(
            [InlineKeyboardButton(text=topic_name, callback_data=f"topic_{topic_id}")]
        )
    return keyboard

    def create_main_keyboard() -> ReplyKeyboardMarkup:
    
Создает основную клавиатуру с кнопками 'Обучение' и 'Решение примеров'.
    
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Обучение"), KeyboardButton(text="Решение примеров")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard<br>
Объяснение:
- create_topics_keyboard создает инлайн-клавиатуру с темами (появляется при выборе "Обучение").
- create_main_keyboard создает основную клавиатуру с двумя кнопками, которые всегда видны внизу.

### Шаг 11: Обработка команды /start
Добавим обработчик для команды /start:

    @dp.message(CommandStart())
    async def send_welcome(message: types.Message):
    
Обрабатывает команду /start.

    keyboard = create_main_keyboard()
    await message.reply(
        "Добро пожаловать в MathBot - ваш помощник в решении примеров! "
        "Этот бот поможет вам освоить математику, решить уравнения и проверить свои знания. "
        "Отправьте выражение, фото или выберите действие ниже:",
        reply_markup=keyboard
    )<br>
Объяснение:
- Этот обработчик отвечает на команду /start, показывая приветственное сообщение и клавиатуру.

![image](https://github.com/user-attachments/assets/f1dfe74a-69a2-4def-ba5d-0c862423d23b)


### Шаг 12: Обработка кнопки "Обучение"
Добавим обработчик для кнопки "Обучение":

    @dp.message(lambda message: message.text == "Обучение")
    async def learn_command(message: types.Message):
    
Обрабатывает кнопку 'Обучение' и показывает темы.

    keyboard = create_topics_keyboard()
    await message.reply("Выбери тему для обучения:", reply_markup=keyboard)<br>
Объяснение:
- Когда пользователь нажимает "Обучение", бот показывает инлайн-клавиатуру с темами.

![image](https://github.com/user-attachments/assets/20e9b8a2-97d5-4a0f-a719-3e5efeed44e2)

![image](https://github.com/user-attachments/assets/52ebfbd5-635e-4e35-bc87-7f5824e9c193)


### Шаг 13: Обработка кнопки "Решение примеров"
Добавим обработчик для кнопки "Решение примеров":

    @dp.message(lambda message: message.text == "Решение примеров")
    async def solve_examples(message: types.Message):
    
Обрабатывает кнопку 'Решение примеров'.

    keyboard = create_main_keyboard()
    await message.reply(
        "Отправь математическое выражение или фото с задачей.",
        reply_markup=keyboard
    )<br>
Объяснение:
- При нажатии "Решение примеров" бот просит пользователя отправить задачу.

![image](https://github.com/user-attachments/assets/196429eb-8021-4c88-b1ea-986c744dd9e9)


### Шаг 14: Обработка выбора темы
Добавим обработчик для выбора темы:

    @dp.callback_query(lambda c: c.data.startswith("topic_"))
    async def process_topic_selection(callback: types.CallbackQuery):
    
Обрабатывает выбор темы и отправляет 3 примера.

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
    await callback.answer()<br>
Объяснение:
- Этот обработчик срабатывает, когда пользователь выбирает тему.
- Бот генерирует 3 примера и сохраняет их в USER_STATES, чтобы потом проверить ответы.

### Шаг 15: Обработка фотографий
Добавим обработчик для фотографий:

    @dp.message(PhotoFilter())
    async def handle_photo(message: types.Message):
    
Обрабатывает сообщения с фотографиями.

    processing_message = await message.reply("Обрабатываю фото...")
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
Объяснение:
- Этот обработчик срабатывает, если пользователь отправил фото.
- Бот скачивает фото, отправляет его в API и показывает ответ.

### Шаг 16: Обработка текстовых сообщений
Добавим обработчик для текстовых сообщений:

    @dp.message()
    async def handle_message(message: types.Message):
Обрабатывает входящие сообщения.

    user_id = message.from_user.id
    keyboard = create_main_keyboard()

    # Проверка, находится ли пользователь в режиме обучения
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
                    explanation = await invoke_llm_api(
                        f"Объясни кратко, как решить: {examples[num]['example']}. Ответ: {correct_answer}"
                    )
                    response_text += f"Объяснение: {explanation}\n"
        
        del USER_STATES[user_id]
        await message.reply(response_text, reply_markup=keyboard)
        return

    # Обработка обычных математических выражений
    if not message.text or not MATH_REGEX.search(message.text):
        await message.reply(
            "Отправь математическое выражение или выбери действие.",
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
Объяснение:
- Этот обработчик проверяет, находится ли пользователь в режиме обучения:
  - Если да, он проверяет ответы пользователя и дает пояснения к ошибкам.
- Если пользователь отправил текстовое выражение, бот отправляет его в API и возвращает решение.

### Шаг 17: Запуск бота
Добавим функцию для запуска бота:

    async def main():
Запускает бота.

    if not TELEGRAM_BOT_TOKEN:
        logging.error("Telegram bot token not found.")
        return
    await dp.start_polling(bot)

    if __name__ == '__main__':
        asyncio.run(main())
Объяснение:
- main запускает бота и начинает принимать сообщения.
- asyncio.run(main()) — точка входа для асинхронного выполнения.

---

## Настройка API и токенов

1. Убедитесь, что .env заполнен правильно:
   
       TELEGRAM_BOT_TOKEN=ваш_токен_от_BotFather
       OPENROUTER_API_KEY=ваш_ключ_от_OpenRouter
       REFERER_URL=http://localhost
       TITLE_NAME=Math Telegram Bot
   
2. Проверьте работу API OpenRouter. Вы можете отправить тестовый запрос через терминал:
   
       curl -X POST https://openrouter.ai/api/v1/chat/completions \
       -H "Authorization: Bearer ваш_ключ_от_OpenRouter" \
       -H "Content-Type: application/json" \
       -d '{"model": "qwen/qwen-2-vl-7b-instruct", "messages": [{"role": "user", "content": "2+2"}]}'
   
   Если вы видите ответ с результатом 4, API работает.

---

## Запуск и тестирование бота

1. Активируйте виртуальное окружение, если еще не сделали:
   
       venv\Scripts\activate  # На Windows
       source venv/bin/activate  # На macOS/Linux
   
3. Запустите бота:
      python math.py
   
4. Откройте Telegram, найдите своего бота (например, @MyMathBot123Bot) и отправьте /start.
5. Попробуйте:
   - Отправить выражение, например, 2x = 4.
   - Отправить фото с задачей.
   - Нажать "Обучение", выбрать тему и решить 3 примера.

---

## Что делать, если что-то не работает

1. Бот не запускается:
   - Проверьте, правильно ли указаны токены в .env.
   - Убедитесь, что виртуальное окружение активировано ((venv) должно быть в терминале).
   - Проверьте, установлены ли все библиотеки (pip install aiogram aiohttp python-dotenv).
2. API возвращает ошибку:
   - Убедитесь, что ваш ключ OpenRouter API действителен. Попробуйте тестовый запрос через curl (см. раздел "Настройка API и токенов").
   - Проверьте, есть ли у вас доступ к модели Qwen2.5-VL 7B Instruct (на OpenRouter может быть ограничение по тарифу).
3. Фото не обрабатывается:
   - Проверьте, правильно ли работает функция download_image. Возможно, проблема с токеном Telegram.
   - Убедитесь, что фото содержит читаемое математическое выражение.

---

## Как улучшить бота

- Добавьте новые темы для обучения (например, "Тригонометрия" или "Производные").
- Включите поддержку голосовых сообщений для ввода задач.
- Добавьте статистику: сколько задач пользователь решил правильно.
- Сделайте бота мультиязычным, добавив поддержку английского языка.

---

## Заключение

Поздравляем! Вы создали MathBot — Telegram-бота, который решает математические задачи с помощью нейронной сети Qwen2.5-VL 7B Instruct. Этот проект — отличный старт для изучения Python, работы с API и создания чат-ботов. Теперь вы можете улучшать бота, добавляя новые функции, и делиться им с друзьями.
