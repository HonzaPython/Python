import requests
from bs4 import BeautifulSoup
import pandas as pd
import os
import glob
from openpyxl import load_workbook

def vycisti_stare_soubory():
    for soubor in glob.glob("produkty_activa*.xlsx"):
        try:
            os.remove(soubor)
        except Exception:
            print("Zavři soubor Excel, aby šel přepsat!")

def ziskej_data_z_url(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Získání kategorie a typu z URL
    # Příklad: www.activa.cz/papir/barevny-papir/?count=48
    casti = url.split('/')
    typ = casti[3] # 'papir'
    kategorie = casti[4].split('?')[0] # 'barevny-papir'
    
    data = []
    for karta in soup.find_all('div', class_='pcard'):
        try:
            nazev = karta.find('h2', class_='pcard__title').get_text(strip=True)
            id_cislo = karta.find('div', class_='pcard__desc').find('strong').get_text(strip=True)
            
            container = karta.find('div', class_='pcvar__container')
            cena_bez = container.find('span', class_='currency_main').find('strong').get_text(strip=True) if container else "N/A"
            cena_s = container.find('span', class_='pcvar__vat').find('strong').get_text(strip=True) if container else "N/A"
            
            data.append({
                'Jméno': nazev, 'ID číslo': id_cislo, 
                'Cena bez DPH': cena_bez, 'Cena s DPH': cena_s,
                'Typ': typ, 'Kategorie': kategorie
            })
        except Exception:
            continue
    return data

seznam_url = [
    "https://www.activa.cz/archivacni-potreby/aktovky-na-dokumenty/?count=1000",
    "https://www.activa.cz/archivacni-potreby/archivacni-krabice/?count=1000",
    "https://www.activa.cz/archivacni-potreby/boxy-na-dokumenty/?count=1000",
    "https://www.activa.cz/archivacni-potreby/desky-na-dokumenty-spisovky/?count=1000",
    "https://www.activa.cz/archivacni-potreby/desky-s-klipem-psaci-podlozky/?count=1000",
    "https://www.activa.cz/archivacni-potreby/euroobaly-zakladaci-desky/?count=1000",
    "https://www.activa.cz/archivacni-potreby/kartoteky-na-zavesne-desky/?count=1000",
    "https://www.activa.cz/archivacni-potreby/katalogove-knihy/?count=1000",
    "https://www.activa.cz/archivacni-potreby/kozene-desky-portfolia/?count=1000",
    "https://www.activa.cz/archivacni-potreby/podpisove-a-tridici-knihy/?count=1000",
    "https://www.activa.cz/archivacni-potreby/rozlisovace/?count=1000",
    "https://www.activa.cz/archivacni-potreby/rychlovazace/?count=1000",
    "https://www.activa.cz/archivacni-potreby/sanony-poradace/?count=1000",
    "https://www.activa.cz/archivacni-potreby/stojanky-odkladace-zasuvky/?count=1000",
    "https://www.activa.cz/archivacni-potreby/vizitkare/?count=1000",
    "https://www.activa.cz/archivacni-potreby/zavesne-zakladaci-desky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/derovacky-na-papir/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/dratky-do-sesivacky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/kancelarske-nuzky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/rezacky-na-papir/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/rozesivace/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/sesivacky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/derovacky-sesivacky-nuzky/soupravy/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/gumicky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/gumy/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/kancelarske-klipy/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/kancelarske-sponky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/magnety/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/orezavatka/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/podlozky-na-stul/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/drobne-potreby/rezaci-podlozky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/lepici-strojky-rollery/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/lepici-tycinky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/lepidla-ve-spreji/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/oboustranne-lepici-pasky/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/samolepici-pasky-izolepy/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/tekuta-lepidla/?count=1000",
    "https://www.activa.cz/drobne-kancelarske-potreby/lepidla-lepici-potreby/vterinova-lepidla/?count=1000",
    "https://www.activa.cz/papir/barevny-papir/?count=1000",
    "https://www.activa.cz/papir/bloky/?count=1000",
    "https://www.activa.cz/papir/diare/?count=1000",
    "https://www.activa.cz/papir/fotopapir/?count=1000",
    "https://www.activa.cz/papir/kancelarsky-papir/?count=1000",
    "https://www.activa.cz/papir/kotoucky-do-pokladen/?count=1000",
    "https://www.activa.cz/papir/manazerske-bloky-zapisniky/?count=1000",
    "https://www.activa.cz/papir/planovaci-mapy/?count=1000",
    "https://www.activa.cz/papir/plotterovy-pauzovaci-uhlovy-papir/?count=1000",
    "https://www.activa.cz/papir/poznamkove-blocky/?count=1000",
    "https://www.activa.cz/papir/recyklovany-papir/?count=1000",
    "https://www.activa.cz/papir/samolepici-blocky/?count=1000",
    "https://www.activa.cz/papir/sesity/?count=1000",
    "https://www.activa.cz/papir/specialni-papir/?count=1000",
    "https://www.activa.cz/papir/tabelacni-papir/?count=1000",
    "https://www.activa.cz/papir/tiskopisy/?count=1000",
    "https://www.activa.cz/papir/vizitkove-kartony/?count=1000",
    "https://www.activa.cz/papir/zaznamni-knihy/?count=1000",
    "https://www.activa.cz/psaci-potreby/jednorazove-propisky/?count=1000",
    "https://www.activa.cz/psaci-potreby/luxusni-psaci-potreby/?count=1000",
    "https://www.activa.cz/psaci-potreby/mikrofixy-linery/?count=1000",
    "https://www.activa.cz/psaci-potreby/mikrotuzky-versatilky/?count=1000",
    "https://www.activa.cz/psaci-potreby/multifunkcni-propisky/?count=1000",
    "https://www.activa.cz/psaci-potreby/naplne-do-psacich-potreb/?count=1000",
    "https://www.activa.cz/psaci-potreby/popisovace/?count=1000",
    "https://www.activa.cz/psaci-potreby/propisky-kulickova-pera/?count=1000",
    "https://www.activa.cz/psaci-potreby/psaci-soupravy/?count=1000",
    "https://www.activa.cz/psaci-potreby/rollery/?count=1000",
    "https://www.activa.cz/psaci-potreby/tuhy-do-mikrotuzky/?count=1000",
    "https://www.activa.cz/psaci-potreby/tuzky/?count=1000",
    "https://www.activa.cz/psaci-potreby/zvyraznovace/?count=1000"
]
vycisti_stare_soubory()
vsechna_data = []

for url in seznam_url:
    print(f"Stahuji: {url}")
    vsechna_data.extend(ziskej_data_z_url(url))

if vsechna_data:
    df = pd.DataFrame(vsechna_data)
    nazev = 'produkty_activa_komplet.xlsx'
    df.to_excel(nazev, index=False)
    
    # Formátování šířky
    wb = load_workbook(nazev)
    ws = wb.active
    for col in ['A', 'B', 'C', 'D', 'E', 'F']:
        ws.column_dimensions[col].width = 20
    wb.save(nazev)
    print(f"Hotovo! Uloženo {len(vsechna_data)} produktů do {nazev}")