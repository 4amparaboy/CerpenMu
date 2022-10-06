from bs4 import BeautifulSoup
from prettytable import PrettyTable
import aiohttp

class ScraperError(Exception):
    pass

class Scraper:
    def __init__(self):
        self.session = aiohttp.ClientSession
        self.BASE_URL = "http://cerpenmu.com"

    async def request(self, link: str):
        async with self.session() as session:
            async with session as ses:
                req = await ses.get(link)
                return BeautifulSoup(await req.text(), "html.parser")

    async def kategori_cerpen(self):
        soup = await self.request(self.BASE_URL)
        cats = None
        for i in soup.select("div.box"):
            if i.select_one("h4") and i.select_one("h4").text.lower() == "kategori cerpen":
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
        soup = await self.request(link)
        table = PrettyTable()
        table.field_names = ["No", "Judul", "Link"]
        data = []
        for i, post in enumerate(soup.select("article.post")[1:], start=1):
            if (a := post.select_one("a")):
                data.append([i, a['title'], a['href']])
        table.add_rows([
            a for a in data
        ])
        return table, data

    async def get_cerpen(self, link: str):
        soup = await self.request(link)
        judul = soup.select_one("#content > article > h1").text
        cerpen = ""
        for p in soup.select("#content > article > p")[:-3]:
            cerpen += p.text + '\n'
        return f'{judul}\n\n{cerpen}'


scraper = Scraper()