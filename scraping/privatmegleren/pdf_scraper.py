from playwright.sync_api import sync_playwright

url = "https://privatmegleren.no/alle/186220233/lys-og-luftig-2-roms-med-solrik-balkong-og-fantastisk-utsikt-varmtvann-og-fyring-ink-gjennomg-ende-planl-sning/komplettsalgsoppgave"


def write_dict_to_file(path, dict):
    with open(path, "w", encoding="utf-8") as file: 
        for type, content in dict.items():
            content = content.replace("\n", "\t")
            content = content.replace(",", ".")
            file.write(type + "," + content)
            file.write("\n")


def parse_paragraphs(page):
    # Scraper paragrafene. 
    totale_kostnader = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[1]').inner_text()
    eiendoms_type = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[3]/div').inner_text()
    eierform = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[4]/div').inner_text()
    etasje = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[6]/div').inner_text()
    bygge_år = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[7]/div').inner_text()
    forretningsfører = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[10]').inner_text()
    parkering = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[18]').inner_text()
    energimerking = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[27]').inner_text()
    prim_rom= page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[4]/p').inner_text()
    bruks_areal= page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[5]/p').inner_text()
    brutto_areal = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[6]/p').inner_text()
    antall_sov = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[8]/p').inner_text()
    prisantydning =  page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[1]/p').inner_text()
    total_pris = page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[1]/div[10]/p').inner_text()
    tomt_strl = page.locator('xpath = //*[@id="routeWrapper"]/div[2]/section/div[1]/div[7]/p').inner_text()
    leilighet_id = page.locator('xpath = //*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/div[5]/div[1]').inner_text()
    adresse = page.locator('xpath = //*[@id="routeWrapper"]/div[1]/h1').inner_text()
    postnummer_uren= page.locator('xpath = //*[@id="routeWrapper"]/div[1]/h2[1]').inner_text()



    return {
        "eiendoms_type" : eiendoms_type,
        "eierform": eierform,
        "etasje": etasje, 
        "bygge_år": bygge_år,
        "forretningsfører": forretningsfører,
        "energimerking": energimerking,
        "totale_kostnader" : totale_kostnader,
        "parkering": parkering,
        "prim_rom": prim_rom,
        "bruks_areal": bruks_areal,
        "brutto_areal": brutto_areal,
        "antall_sov": antall_sov, 
        "prisantydning": prisantydning,
        "total_pris": total_pris,
        "tomt_strl": tomt_strl,
        "leilighet_id": leilighet_id,
        "adresse": adresse,
        "postnummer_uren": postnummer_uren
    }

def scrape_and_download_pdf(page):
    # Scraper PDFen. 
    with page.expect_download() as download_info:
        page.locator('xpath=//*[@id="routeWrapper"]/div[2]/section/div[2]/div[1]/div/div[2]/div/a[1]').click()
    download = download_info.value
    download.save_as("data/haha.pdf")

def parse_house_page(url):
    with sync_playwright() as p:
        browser_type = p.firefox

        # Åpner siden
        browser = browser_type.launch()
        page = browser.new_page()
        page.goto(url)
        # Godtar cookies 
        page.locator('text=Ja, det er greit').click()
        
        # Henter inn paragrafene og skriver til fil. 
        page_info = parse_paragraphs(page)
        write_dict_to_file("data/page_info.csv", page_info)

        # Henter inn PDF og skriver til fil. TODO Bare kommenter inn igjen når det trengs :) 
        # scrape_and_download_pdf(page)

        browser.close()

parse_house_page(url)