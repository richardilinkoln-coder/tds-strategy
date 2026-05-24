# Roblox TDS Strategy Bot

Telegram-бот для Roblox TDS (Tower Defense Simulator), который показывает стратегии через inline-кнопки и **не спамит новыми сообщениями** при навигации: вся логика работает через `edit_message_text` и `edit_message_reply_markup`.

## Возможности

- реакция на слово `стратегия`
- красивое меню с эмодзи
- выбор режима и party size через inline keyboard
- редактирование текущего сообщения вместо отправки новых
- работа в личке и группах
- защита от:
  - несуществующего режима
  - отсутствующего party size
  - отсутствующей ссылки
- логирование
- современный `aiogram 3.x`

## Структура

```text
bot/
├── main.py
├── config/
│   ├── settings.py
│   └── strategies.py
├── handlers/
│   └── strategy.py
├── keyboards/
│   └── strategy.py
└── utils/
    ├── callbacks.py
    └── logger.py
```

## Установка

1. Скопируй проект в отдельную папку.
2. Установи зависимости:

```bash
pip install -r requirements.txt
```

## Создание `.env`

Создай файл `.env` рядом с `main.py` и добавь:

```env
BOT_TOKEN=123456:ABCDEF_your_token_here
```

Можно взять пример из `.env.example`.

Если запускаешь из папки `bot/`, команда будет `python main.py`.

## Запуск

```bash
python bot/main.py
```

## Как добавлять режимы

Открой `bot/config/strategies.py` и добавь новый блок в `STRATEGIES`:

```python
"newmode": {
    "name": "New Mode",
    "emoji": "⭐",
    "modes": {
        "duo": "https://docs.google.com/...",
        "trio": "https://docs.google.com/...",
    },
}
```

После этого бот автоматически покажет новую кнопку в меню.

## Как менять ссылки

В том же файле `bot/config/strategies.py` замени значение в `modes`:

```python
"duo": "https://your-new-link",
```

## Как отключать party size

Просто удали нужный ключ из `modes`.

Например, если у режима есть только:

```python
"modes": {
    "duo": "https://...",
    "trio": "https://...",
}
```

Тогда кнопки `Solo` и `Quad` не появятся вообще.

## Callback data

Формат короткий и удобный:

- `strat:pw2`
- `party:pw2:duo`
- `nav:strategy:pw2`
- `nav:menu:_`

## Замечания

- Бот отвечает только на точное слово `стратегия`
- Если бот используется в группе, может понадобиться отключить privacy mode в BotFather, если хочешь, чтобы он видел обычные сообщения
- Если Telegram вернёт `message is not modified`, код это уже обрабатывает без падения
