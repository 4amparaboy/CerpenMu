from cerpen import scraper
import asyncio

loop = asyncio.new_event_loop()
while (1 > 0):
    a, b = (loop.run_until_complete(scraper.kategori_cerpen()))
    print(a)
    choice_1 = input("Silahkan pilih kategori : ")
    if not choice_1.isdigit():
        print("Masukkan hanya angka")
        continue
    if int(choice_1) > len(b):
        print("Masukkan hanya 1 - %s" % len(b))
        continue
    c, d = loop.run_until_complete(scraper.perkategori(b[int(choice_1) - 1][- 1]))
    while True:
        print(c)
        choice_2 = input("Silahkan pilih cerpen : ")
        if not choice_2.isdigit():
            print("Masukkan hanya angka")
            continue
        if int(choice_2) > len(d):
            print("Masukkan hanya 1 - %s" % len(d))
            continue
        print(loop.run_until_complete(scraper.get_cerpen(d[int(choice_2) - 1][- 1])))
        break

    if input("Lanjutkan Program [Y/N] ? : ").lower() == "n":
        break
