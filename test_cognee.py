from dotenv import load_dotenv
import asyncio
import cognee

load_dotenv()

async def main():
    await cognee.remember(
        "Newton's First Law states that an object remains at rest or in uniform motion unless acted upon by an external force."
    )

    result = await cognee.recall(
        query_text="What is Newton's First Law?"
    )

    print(result)

asyncio.run(main())