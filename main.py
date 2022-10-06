from bs4 import BeautifulSoup
from prettytable import PrettyTable
import asyncio
import aiohttp

class ScraperError(Exception):
    pass

class Scraper:
    def __init__(self):
        self.session = aiohttp.ClientSession
        self.BASE_URL = "http://cerpenmu.com"

    async def make_request(self, link: str):
        async with self.session() as session:
            async with session as ses:
                req = await ses.get(link)
                return await req.text()

    async def kategori_cerpen(self):
        response = await self.make_request(self.BASE_URL)
        soup = BeautifulSoup(response, "html.parser")
        cats = None
        for i in soup.select("div.box"):
            if i.find("h4") and i.find("h4").text.lower() == "kategori cerpen":
                cats = i
        if not cats:
            raise ScraperError("Gagal scrape data")
        table = PrettyTable()
        table.field_names = ["No", "Kategori", "Link"]
        data = [[i, a.text, a['href']] for i, a in enumerate(cats.select("a"), start=1)]
        table.add_rows([
            a for a in data
        ])
        return table, data

    async def perkategori(self, link: str):
        response = await self.make_request(link)
        soup = BeautifulSoup(response, "html.parser")
        table = PrettyTable()
        table.field_names = ["No", "Judul"]
        for i, post in enumerate(soup.select("article.post")[1:]):
            if (a := post.find("a")):
                table.add_row([i + 1, a['title']])
        return table


loop = asyncio.new_event_loop()
scraper = Scraper()
while True:
    a, b = (loop.run_until_complete(scraper.kategori_cerpen()))
    print(a)
    choice_1 = input("Silahkan pilih kategori : ")
    if not choice_1.isdigit():
        print("Masukkan hanya angka")
        continue
    if int(choice_1) > len(b):
        print("Masukkan hanya 1 - %s" % len(b))
        continue

    if input("Lanjutkan Program [Y/N] ? : ").lower() == "n":
        break


# kategori_cerpen = 
# print(kategori_cerpen)
# table = loop.run_until_complete(scraper.perkategori('http://cerpenmu.com/category/cerpen-anak/page/4'))
# print(table)
