import asyncio
import os
import pprint
import time

import aiohttp
import typer
from bs4 import BeautifulSoup
from dotenv import load_dotenv

app = typer.Typer()


async def scrape(session: aiohttp.ClientSession, url: str):
    print(f"Fetching {url} and parsing the title...")
    # to simulate a slow connection
    # await asyncio.sleep(10)

    async with session.get(url) as response:
        data = await response.text()
        results = extract(data)
        results["url"] = url
        return results


def extract(data: str):
    soup = BeautifulSoup(data, "lxml")
    contents = []
    # FIXME: adhoc implementation to extract the contents
    for element in soup.find_all("a", attrs={"data-test-element": "update-entry-link"}):
        contents.append(element.text)
    return {
        "title": soup.title.string,
        "contents": contents,
    }


def get_array_from_env(env_name: str):
    try:
        env_str = os.getenv(env_name)
        return env_str.replace("\n", "").replace(" ", "").split(",")
    except Exception as e:
        print(e)
        return []


async def main():
    start = time.time()
    print(f"Start {start}")
    urls = get_array_from_env("URLS")

    async with aiohttp.ClientSession() as session:
        tasks = [scrape(session, url) for url in urls]

        print("Tasks are running in the background...")
        results = await asyncio.gather(*tasks)
        print("Tasks completed.")

    for result in results:
        pprint.pprint(result, width=500)
    print(f"Elapsed time: {time.time() - start}[sec]")


@app.command()
def run():
    asyncio.run(main())


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
