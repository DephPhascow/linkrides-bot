# SimpleDoIt

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
