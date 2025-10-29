import os
import json
import csv
import requests, uuid, time
from bs4 import BeautifulSoup
import random
from requests.exceptions import ProxyError, SSLError, ConnectTimeout, ReadTimeout
import re


def clean_text(text: str) -> str:
    cleaned = text.replace("\n", " ").replace("\r", " ")
    cleaned = re.sub(r"\s{2,}", " ", cleaned)
    return cleaned.strip()


def url_list_proc(file: str):
    with open(file, "r", encoding="utf-8") as f:
        url_list = f.read().split(',')
    prefix = "https://ru."
    for n, i in enumerate(url_list):
        url = i[i.index('linkedin'):]
        if "?" in url:
            url = url[:url.index('?')]
        if url[-1] == '/':
            url = url[:-1]
        url_list[n] = prefix + url
    return url_list


def headers_creation(url: str) -> dict:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cache-Control": "max-age=0",
        "Referer": "https://google.com/ru/search/" + url[url.index('company/') + 8:],
        "Connection": "close",
    }

    return headers


def make_proxies(us_name: str, passw: str):
    proxy = f"http://{us_name}:{passw}@gate.decodo.com:10001"
    return {"http": proxy, "https": proxy}


def overview(url: str, proxies: dict, headers: dict, max_retries: int = 10):
    last_error = None
    for attempt in range(1, max_retries + 1):
        try:
            # main request
            resp = requests.get(
                url,
                proxies=proxies,
                headers=headers,
                allow_redirects=True,
            )
            code = resp.status_code

            if code == 200 and "text/html" in resp.headers.get("Content-Type", ""):
                soup = BeautifulSoup(resp.content, "html.parser")

                # Company overview extract
                overview = soup.find("p", class_="break-words text-color-text").get_text()
                overview = clean_text(overview)
                base_dict = {"url": url,
                             "overview": overview}

                # Rest info extract
                info = soup.find("dl", class_="mt-6")
                info_keys = info.find_all('dt',
                                          class_="font-sans text-md font-bold text-color-text break-words w-40 papabear:flex-shrink-0 papabear:mr-3 mamabear:flex-shrink-0 mamabear:mr-3 babybear:mb-1")
                info_values = info.find_all('dd',
                                            class_="font-sans px-0.25 text-md text-color-text break-words overflow-hidden")

                info_dict = dict(
                    zip([k.get_text().strip() for k in info_keys], [v.get_text().strip() for v in info_values]))
                try:
                    info_dict['Веб-сайт'] = info_dict.get('Веб-сайт').split('\n')[0]
                except:
                    pass
                try:
                    info_dict["Размер компании"] = info_dict["Размер компании"].split("\xa0")[0]
                except:
                    pass
                return {**base_dict, **info_dict}

            else:
                pass

        except requests.exceptions.RequestException as e:
            print(f"[{attempt}] Request error: {e}")
            last_error = e

        time.sleep(min(1.5 ** attempt, 10)) # Backoff

    raise Exception(f"Failed to fetch {url} after {max_retries} attempts. Last error: {last_error}")


def main(
        input_file: str = "url_list.txt",
        output_file: str = "output_decodo.json",
        username: str = "",
        password: str = ""):

    url_list = url_list_proc(file=input_file)
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump([], f, ensure_ascii=False, indent=4)
    res = []
    for n, u in enumerate(url_list, start=1):
        try:
            proxies = make_proxies(username, password)
            #             proxies = {} # if you don't need proxies
            headers = headers_creation(u)
            result = overview(url=u, proxies=proxies, headers=headers)
            res.append(result)

            with open(output_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            data.append(result)
            with open(output_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)

        except Exception as e:
            print(f"❌ Catch exception with {u}: {e}\n")

    print(f"🎯 Done! It's: {len(res)} URL.")


# RUN
if __name__ == "__main__":
    USERNAME = ''  # username decodo
    PASSWORD = ''  # pass decodo
    PORT = '10001'  # port decodo
    url_list = "url_list.txt" # list wirh URL-s
    output_file = "output_decodo.json" #JSON for result

    main(
        input_file=url_list,
        output_file=output_file,
        username=USERNAME,
        password=PASSWORD,
    )