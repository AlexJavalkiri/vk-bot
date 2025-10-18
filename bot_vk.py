# Импортируем нужные модули
from vkbottle import Bot
from vkbottle.bot import Message, Payload
import random, os

# Читаем токен из переменной окружения (настраивается в Render)
TOKEN = os.getenv("TOKEN")  # Пример: "1234567890:NEW_TOKEN_HERE" из Render

# Матерные фразы для ответа
ROASTS = [
    "Блять, ты чё, внатуре охуел?",
    "Похер, твой текст — полная хуйня!",
    "Ебать, это что за пиздец ты написал?",
    "Сука, да ты заебал уже!",
    "Похуй, твой месседж — говно!",
    "Чё за херня, бери и вали нахуй!",
    "Пиздец, ты реально ебанулся?",
    "Блять, это ж надо так обосраться!",
    "Хули ты трындишь, дебил?",
    "Ебаный в рот, завали ебало!",
    "Чё, блять, опять хуйню несёшь?",
    "Похуй мне, твой пиздец не катит!",
    "Сука, ты как из жопы вылез!",
    "Ебать, это не текст, а ебаный стыд!",
    "На хуй иди, мудила ебаный!"
]

# Слова, на которые бот реагирует
TRIGGER_WORDS = [
    "привет", "похер", "бля", "хуй", "пиздец",
    "ебать", "сука", "охуеть", "ебаный", "нахуй",
    "хули", "ебало", "говно", "похуй", "заебал",
    "мудила", "пиздецки", "хуета", "ебан", "жопа"
]

# Специфические ответы на слова
SPECIFIC_RESPONSES = {
    "нет": "Минет",
    "да": "Пизда",
    "первый": "Пидорас",
    "привет": "Здарова, заебал!",
    "циркулярная": "Да ты заебал",
    "похуй": "Мне тоже",
    "хахаха": "Дохуя смешно тебе?",
    "хпхп": "Дохуя смешно тебе?",
    "хпхпхп": "Дохуя смешно тебе?",
    "хаха": "Дохуя смешно тебе?",
    "матроскин": "Ты тоже такой медленный?"
}

# Создаём бота с токеном
bot = Bot(token=TOKEN)

# Команда /start (или сообщение "start")
@bot.on.message(text="start")
async def start(message: Message):
    await message.answer(
        f"Привет! Добавь меня в группу, будет весело! и упомяни @{bot.username}"
    )

# Команда /who (Кто сегодня пиздализ?)
@bot.on.message(text="who")
async def who(message: Message):
    if message.peer_id < 2000000000:  # Проверяем, что это группа
        await message.answer("Эта команда работает только в группах!")
        return

    # Проверяем, была ли команда уже вызвана в этой группе
    if "pizdaliz_called" in message.peer_id:
        await message.answer("я же блять сказал, кто сегодня пиздализ :)")
        return

    try:
        # Получаем список участников группы
        members = await bot.api.groups.getMembers(group_id=message.peer_id - 2000000000, fields="first_name,last_name")
        users = [member for member in members.items if not member.is_hidden_from_feed]  # Фильтруем ботов и скрытых
        
        if len(users) < 2:
            await message.answer("В группе слишком мало людей, чтобы выбрать пиздализов!")
            return

        # Выбираем двух случайных участников
        pizdalizs = random.sample(users, 2)
        pizdaliz1 = pizdalizs[0]
        pizdaliz2 = pizdalizs[1]

        # Формируем ссылки на пользователей
        pizdaliz1_link = f"@{pizdaliz1.screen_name}" if pizdaliz1.screen_name else f"{pizdaliz1.first_name} {pizdaliz1.last_name}"
        pizdaliz2_link = f"@{pizdaliz2.screen_name}" if pizdaliz2.screen_name else f"{pizdaliz2.first_name} {pizdaliz2.last_name}"

        # Отправляем ответ
        await message.answer(f"Сегодня пиздализы: {pizdaliz1_link} и {pizdaliz2_link}!")

        # Помечаем, что команда была вызвана
        message.peer_id["pizdaliz_called"] = True

    except Exception as e:
        await message.answer(f"Ошибка, блять: {str(e)}")

# Реакция на слова или упоминания в группах
@bot.on.message(text=TRIGGER_WORDS)
async def roast(message: Message):
    if message.peer_id < 2000000000:  # Проверяем, что это группа
        text = message.text.lower()
        for word in TRIGGER_WORDS:
            if word in text:
                # Если есть специфический ответ, используем его
                response = SPECIFIC_RESPONSES.get(word, random.choice(ROASTS))
                await message.answer(response)
                return
        if f"@{bot.username}".lower() in text:
            await message.answer(random.choice(ROASTS))

# Приветствие новичков и реакция на выход из группы
@bot.on.message_event("group_new_member")
async def welcome_new_member(event):
    new_member = event.new_member
    await bot.api.messages.send(
        peer_id=event.peer_id,
        message=f"Добро пожаловать, пидор, в наш гей-клуб, {new_member.first_name}!",
        random_id=random.randint(1, 100000)
    )

@bot.on.message_event("group_leave")
async def leave_member(event):
    old_member = event.old_member
    await bot.api.messages.send(
        peer_id=event.peer_id,
        message=f"Пошёл нахуй, ебанный натурал, {old_member.first_name}!",
        random_id=random.randint(1, 100000)
    )

# Запуск бота
if __name__ == "__main__":
    bot.run_forever()
