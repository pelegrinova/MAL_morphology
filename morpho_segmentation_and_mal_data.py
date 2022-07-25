import os
from pathlib import Path
import csv
import re
from decimal import Decimal
from collections import Counter
from locale import LC_NUMERIC
from locale import setlocale

# nastavení "lokality"
setlocale(LC_NUMERIC, "cs_CZ.UTF-8")


zanry = ["dop", "poh", "pov", "stud"] 
cisla_textu = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "slouč"]
DICTIONARY_FILE = "MorfoCzech_dictionary.csv"

# převod textu v tokens na text v types
def token_to_types(text):
    text_types = []

    for slovo in text:
        if slovo not in text_types:
            text_types.append(slovo)

    return text_types

# počítadlo frekvencí
def pocitadlo(soubor):
    frekvence = Counter(soubor)
    return frekvence


# funkce s výpočtem MALu
def vypocet_mal(data):
    vysledek = []
    for klic in sorted(data):  # tahá ze seřazeného seznamu klíčů, ale nic nepřepisuje !
        if klic == 0:
            pass
        else:
            prumer = round(Decimal(str(data[klic][0] / (data[klic][1] * klic))), 2)
            mezivysledek_carka = (klic, data[klic][1], f"{prumer:n}")  # to f"..." dělám proto, aby se převedly korektně desetinné tečky na desetinné čárky
            vysledek.append(mezivysledek_carka)
    return vysledek


def uprava_textu(text):
    # odstranění interpunkce a znaků - a co mazání řádků ???
    znaky = [",", ".", "!", "?", "'", "\"", "<", ">", "-", "–", ":", ";", "„", "“", "=", "%", "&", "#", "@", "/", "\\", "+", "(", ")", "[", "]", "§"]

    for znak in znaky:
        text = text.replace(znak, "")

    # odstranění číslic
    text = re.sub(r"[0-9]+", "", text)

    # odstranění mezer
    text = re.sub(r"\s{2,}", " ", text)

    # rozdělení textu na slova
    text_na_slova = text.split(sep=" ")

    # substituce grafiky tak, aby odpovídala realizaci hlásek
    text_na_slova_foneticky = []
    for slovo in text_na_slova: 
        slovo = slovo.replace("pouč", "po@uč")  # joojoo, tohle je prasárna a vím o tom; třeba vyřešit
        slovo = slovo.replace("nauč", "na@uč")
        slovo = slovo.replace("douč", "do@uč")
        slovo = slovo.replace("přeuč", "pře@uč")
        slovo = slovo.replace("přiuč", "při@uč")
        slovo = slovo.replace("vyuč", "vy@uč")
        slovo = slovo.replace("pouka", "po@uka")
        slovo = slovo.replace("pouká", "po@uká")
        slovo = slovo.replace("poukl", "po@ukl")
        slovo = slovo.replace("poulič", "po@ulič")
        slovo = slovo.replace("poum", "po@um")
        slovo = slovo.replace("poupr", "po@upr")
        slovo = slovo.replace("pouráž", "po@uráž")
        slovo = slovo.replace("pousm", "po@usm")
        slovo = slovo.replace("poust", "po@ust")
        slovo = slovo.replace("poute", "po@ute")
        slovo = slovo.replace("pouvaž", "po@uvaž")
        slovo = slovo.replace("pouzen", "po@uzen")
        slovo = slovo.replace("douč", "do@uč")
        slovo = slovo.replace("douprav", "do@uprav")
        slovo = slovo.replace("doužív", "do@užív")
        slovo = slovo.replace("douzov", "do@uzov")
        slovo = slovo.replace("doupřesn", "do@upřesn")
        slovo = slovo.replace("doudit", "do@udit")
        slovo = slovo.replace("doudí", "do@udí")
        slovo = slovo.replace("muzeu", "muzE")  # diftongické "eu"
        slovo = slovo.replace("neutrál", "nEtrál")
        slovo = slovo.replace("eucken", "Ecken")
        slovo = slovo.replace("kreuzmann", "krEzmann")
        slovo = slovo.replace("pilocereus", "pilocerEs")
        slovo = slovo.replace("cephalocereus", "cephalocerEs")
        # části
        slovo = slovo.replace("ie", "ije")
        slovo = slovo.replace("ii", "iji")
        slovo = slovo.replace("ií", "ijí")
        slovo = slovo.replace("dě", "ďe")
        slovo = slovo.replace("tě", "ťe")
        slovo = slovo.replace("ně", "ňe")
        slovo = slovo.replace("mě", "MŇE")
        slovo = slovo.replace("ě", "JE")
        slovo = slovo.replace("x", "KS")
        slovo = slovo.replace("ch", "X")
        slovo = slovo.replace("q", "KW")
        slovo = slovo.replace("ou", "O")
        slovo = slovo.replace("au", "A")
        slovo = slovo.replace("dž", "G")
        # odstranění "@"
        slovo = slovo.replace("@", "")
        text_na_slova_foneticky.append(slovo)

    text_na_slova_uniq_foneticky = set(text_na_slova_foneticky)

    return text_na_slova_foneticky, text_na_slova_uniq_foneticky


# načtení morfologického slovníku jako slovníku (haha)
with open(DICTIONARY_FILE, encoding="UTF-8") as soubor:
    obsah_slovniku = csv.reader(soubor, delimiter=";")
    slovnik = {}
    for polozka in obsah_slovniku:
        slovnik[polozka[0]] = polozka[1]

# tu se dějou věci...
for zanr in zanry:
    # vytvářím složky pro ukládání výsledků segmentace
    nadslozka = f"C:\\Users\\peleg\\OneDrive\\doktorát\\experiment_disertace\\výsledky\\fin_výsl\\slovo_morfém_foném"
    slozka_zanr_typ_seg = f"{zanr}_SMF"

    slozka_segmentace = f"segmentované_texty_{zanr}"
    slozka_tokens = f"tokens_{zanr}_SMF"
    slozka_types = f"types_{zanr}_SMF"
    slozka_raw_data_tokens = f"raw_data_SMF_tokens_{zanr}"
    slozka_raw_data_types = f"raw_data_SMF_types_{zanr}"

    cesta_nove_slozky_segmentace = os.path.join(nadslozka, slozka_zanr_typ_seg, slozka_segmentace)
    cesta_nove_slozky_tokens = os.path.join(nadslozka, slozka_zanr_typ_seg, slozka_tokens)
    cesta_nove_slozky_types = os.path.join(nadslozka, slozka_zanr_typ_seg, slozka_types)
    cesta_nove_slozky_tokens_raw_data = os.path.join(nadslozka, slozka_zanr_typ_seg, slozka_tokens, slozka_raw_data_tokens)
    cesta_nove_slozky_types_raw_data = os.path.join(nadslozka, slozka_zanr_typ_seg, slozka_types, slozka_raw_data_types)

    os.makedirs(cesta_nove_slozky_segmentace)
    os.makedirs(cesta_nove_slozky_tokens)
    os.makedirs(cesta_nove_slozky_types)
    os.makedirs(cesta_nove_slozky_tokens_raw_data)
    os.makedirs(cesta_nove_slozky_types_raw_data)

    for cislo_textu in cisla_textu:
        # načítám soubor
        cesta = f"C:\\Users\\peleg\\OneDrive\\doktorát\\experiment_disertace\\texty\\{zanr}\\{zanr}_{cislo_textu}.txt"
        soubor = open(cesta, encoding="UTF-8")
        text = soubor.read().lower().replace("\n", " ").strip()
        soubor.close()

        # "fonologický přepis"
        slova_k_segmentaci, uniq_slova_k_segmentaci = uprava_textu(text)

        # autosegmentace
        segmented_words = []
        for original_word in slova_k_segmentaci:
            try:
                segmented_word = slovnik[original_word]
            except KeyError:
                print(
                    f"POZOR! SLOVO {original_word} CHYBÍ VE SLOVNÍKU A TUDÍŽ"
                    "NEBUDE SEGMENTOVÁNO!"
                )
                segmented_word = original_word
            segmented_words.append(segmented_word)
        
        text_segmentovany_slouceny = " ".join(segmented_words)

        cesta_k_ulozeni = os.path.join(cesta_nove_slozky_segmentace, f"segmentovaný_{zanr}_{cislo_textu}.txt")
        soubor_k_ulozeni = open(cesta_k_ulozeni, mode="w", encoding="UTF-8")
        soubor_k_ulozeni.write(text_segmentovany_slouceny)
        soubor_k_ulozeni.close()

        # výpočet dat pro mal tokens + types

        for typ in ["tokens", "types"]:

            if typ == "tokens":
                # načtení segmentovaného textu
                segmentovany_text = text_segmentovany_slouceny.split(sep=" ") 
            if typ == "types":
                # načtení segmentovaného textu
                segmentovany_text = token_to_types(text_segmentovany_slouceny.split(sep=" "))

            # přípravné výpočty
            # výpočet délky konstruktu v konstituentech
            delka_slov_v_morfech = []
            for slovo in segmentovany_text:
                delka_slova_v_morfech = slovo.count("-") + 1
                delka_slov_v_morfech.append(delka_slova_v_morfech)

            # výpočet délky konstruktu v subkonstituentech
            nesegmentovany_text = []
            for segmentovane_slovo in segmentovany_text:
                hole_slovo = segmentovane_slovo.replace("-", "")
                nesegmentovany_text.append(hole_slovo)

            delka_slov_ve_fonemech = []
            for slovo in nesegmentovany_text:
                delka_slova_ve_fonemech = len(slovo)
                delka_slov_ve_fonemech.append(delka_slova_ve_fonemech)

            # počet x-konstituentových konstruktů
            frekvence_morfu = Counter(delka_slov_v_morfech)

            # slovník: klíč = x-konstituentový konstrukt, hodnota = součet délek všech takových konstruktů (dvou-morfémové slovo, součet délek všech dvou-morfémových slov)
            soucty_delek_x_morfovych_slov = {}
            for i, klic in enumerate(delka_slov_v_morfech):
                if klic not in soucty_delek_x_morfovych_slov:
                    soucty_delek_x_morfovych_slov[klic] = 0
                soucty_delek_x_morfovych_slov[klic] += delka_slov_ve_fonemech[i]

            print(soucty_delek_x_morfovych_slov)

            # slovník: klíč = x-konstituentový konstrukt, hodnota = (součet délek všech takových konstruktů, počet takových konstuktů)
            slovnik_data_pro_mal = {}
            for klic in soucty_delek_x_morfovych_slov:
                slovnik_data_pro_mal[klic] = (soucty_delek_x_morfovych_slov[klic], frekvence_morfu[klic])

            print(dict(sorted(slovnik_data_pro_mal.items())))  # seřazený slovník podle klíčů, pozor na seřazování slovníku - ošemetné, pro zobrazení či tahání infa ale stačí

            vysledek_mal = vypocet_mal(slovnik_data_pro_mal)
            print(vysledek_mal)

            # uložení výsledků do tabulky # with open nahrazuje nutnost uzavřít to .close()
            if typ == "tokens":
                cesta_k_ulozeni = os.path.join(cesta_nove_slozky_tokens_raw_data, f"raw_data_SMF_tokens_{zanr}_{cislo_textu}.csv")
                with open(cesta_k_ulozeni, "w", encoding="UTF-8") as csvfile:
                    vysledek_data = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                    vysledek_data.writerow(["construct", "frq", "mean of constituent"])
                    for i in vysledek_mal:
                        vysledek_data.writerow([i[0], i[1], i[2]])
            if typ == "types":
                cesta_k_ulozeni = os.path.join(cesta_nove_slozky_types_raw_data, f"raw_data_SMF_types_{zanr}_{cislo_textu}.csv")
                with open(cesta_k_ulozeni, "w", encoding="UTF-8") as csvfile:
                    vysledek_data = csv.writer(csvfile, delimiter=';', lineterminator='\n')
                    vysledek_data.writerow(["construct", "frq", "mean of constituent"])
                    for i in vysledek_mal:
                        vysledek_data.writerow([i[0], i[1], i[2]])




