import asyncio
import json
import os
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
    titles = []
    descriptions = []
    # FIXME: adhoc implementation to extract the contents
    for element in soup.find_all("h3", attrs={"qa-heading": "issue_title"}):
        titles.append(element.text.replace("\n", "").replace(" ", ""))
    for element in soup.find_all("p", attrs={"qa-content": "issue_description"}):
        descriptions.append(element.text.replace("\n", "").replace(" ", ""))
    assert len(titles) == len(
        descriptions
    ), "The number of titles and descriptions are different."
    contents = [
        {"title": title, "description": description}
        for title, description in zip(titles, descriptions)
    ]
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


async def main(output_file: str):
    start = time.time()
    print(f"Start {start}")
    urls = get_array_from_env("URLS")

    async with aiohttp.ClientSession() as session:
        tasks = [scrape(session, url) for url in urls]

        print("Tasks are running in the background...")
        results = await asyncio.gather(*tasks)
        print("Tasks completed.")

    with open(output_file, mode="wt", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"Elapsed time: {time.time() - start}[sec]")


@app.command()
def run(path_to_file: str = typer.Option("./output.json", help="Output file name")):
    # if output_file's directory is not exist, exit the program
    if not os.path.exists(os.path.dirname(path_to_file)):
        typer.echo("The directory does not exist.")
        raise typer.Exit(code=1)

    asyncio.run(main(path_to_file))


if __name__ == "__main__":
    # load environment variables
    load_dotenv("./settings.env")

    app()
