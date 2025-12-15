import asyncio
from pickledb import PickleDB

async def main():
    db = await PickleDB("data.json").load()

    await db.set("score", 42)
    value = await db.get("score")
    print(value)  # → 42

    await db.save()

asyncio.run(main())
