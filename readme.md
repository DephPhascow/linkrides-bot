# SimpleDoIt

## Мультиязык

```bash
pybabel extract --ignore-dirs="env" --ignore-dirs="git" --input-dirs=. -o locales/messages.pot - Вытянуть текста
pybabel extract -k _:1,1t -k __ --ignore-dirs="env" --ignore-dirs="git"  --input-dirs=. -o locales/messages.pot
pybabel init -i locales/messages.pot -d locales -D messages -l en
pybabel update -d locales -D messages -i locales/messages.pot
pybabel compile -d locales -D messages
```

## Тестирование производительности

```python

import cProfile
import pstats
from aiogram import types

async def process_message(message: types.Message):
    # Какие-то операции, например, обращение к базе данных
    pass

# Профилирование функции обработки сообщения
pr = cProfile.Profile()
pr.enable()
await process_message(message)
pr.disable()

stats = pstats.Stats(pr)
stats.sort_stats('cumulative').print_stats(10)  # Печать 10 самых затратных операций
```
