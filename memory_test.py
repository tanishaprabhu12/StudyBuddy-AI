import asyncio
import cognee

async def main():
    print("Remembering...")

    await cognee.remember(
        "Tanisha likes Python and wants to build an AI StudyBuddy."
    )

    print("Done!")

    print("\nSearching memory...")

    result = await cognee.recall(
        "What does Tanisha like?"
    )

    print(result)

asyncio.run(main())