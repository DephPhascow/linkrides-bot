import asyncio
from constants import TORTOISE_ORM
from tortoise import Tortoise

PATH_TO_SAVE = "exports"

async def main():
    await Tortoise.init(
        config=TORTOISE_ORM
    )    
    while True:
        print(f"exit - exit the program")
        command = input("Enter command: ")
        if command == "exit":
            break
    await Tortoise.close_connections()
    
if __name__ == '__main__':
    asyncio.run(main())