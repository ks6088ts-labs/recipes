import asyncio
import json
import os
import time

import aiohttp
import typer
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from lxml import etree

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
    for element in soup.find_all("h3", attrs={"qa-heading": "issue_title"}):
        title = element.text.replace("\n", "").replace(" ", "")
        description_element = element.find_next(
            "p", attrs={"qa-content": "issue_description"}
        )
        description = description_element.text.replace("\n", "").replace(" ", "")
        contents.append({"title": title, "description": description})
    return {
        "title": soup.title.string,
        "contents": contents,
    }


def get_array_from_env(env_name: str):
    # convert comma-separated string to array
    try:
        env_str = os.getenv(env_name)
        return env_str.replace("\n", "").replace(" ", "").split(",")
    except Exception as e:
        print(e)
        return []


async def sites2json_impl(output_file: str):
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
def html2json(
    xpath="//td[@class='left']/a",
    path_to_html="./index.html",
    path_to_output_json: str = typer.Option(
        "./output.json", help="Output JSON file path"
    ),
):
    # if output_file's directory is not exist, exit the program
    path_to_dir = os.path.dirname(path_to_output_json)
    if not os.path.exists(path_to_dir):
        typer.echo(f"The output directory {path_to_dir} does not exist.")
        raise typer.Exit(code=1)

    with open(path_to_html, mode="rt", encoding="utf-8") as f:
        data = f.read()
        tree = etree.HTML(data)
        texts = tree.xpath(f"{xpath}/text()")
        links = tree.xpath(f"{xpath}/@href")
        assert len(texts) == len(links), "The number of texts and links are different."
        results = [{"text": text, "link": link} for text, link in zip(texts, links)]
        with open(path_to_output_json, mode="wt", encoding="utf-8") as f:
            json.dump(results, f, ensure_ascii=False, indent=2)


@app.command()
def sites2json(
    env_file_path="./settings.env",
    path_to_output_json: str = typer.Option(
        "./output.json", help="Output JSON file path"
    ),
):
    # if env_file_path is not exist, exit the program
    if not os.path.exists(env_file_path):
        typer.echo(f"The file {env_file_path} does not exist.")
        raise typer.Exit(code=1)
    # if output_file's directory is not exist, exit the program
    path_to_dir = os.path.dirname(path_to_output_json)
    if not os.path.exists(path_to_dir):
        typer.echo(f"The output directory {path_to_dir} does not exist.")
        raise typer.Exit(code=1)

    load_dotenv(env_file_path)
    asyncio.run(sites2json_impl(path_to_output_json))


if __name__ == "__main__":
    app()
