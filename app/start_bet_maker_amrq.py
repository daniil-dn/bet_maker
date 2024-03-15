import asyncio

from app.armq_service import Consumer

__doc__ = """Запуск консьюмера AMQ для bet maker"""
if __name__ == '__main__':
    asyncio.run(Consumer().run())
