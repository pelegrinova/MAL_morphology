import csv

DICTIONARY_FILE = "MorfoCzech_dictionary.csv"
INPUT_FILE = "pokus.txt"
OUTPUT_FILE = "vysledek_segmentace_pokus.txt"


# načtení morfologického slovníku jako slovníku (haha)
with open(DICTIONARY_FILE, encoding="UTF-8") as soubor:
    obsah_slovniku = csv.reader(soubor, delimiter=";")

    slovnik = {}
    for polozka in obsah_slovniku:
        slovnik[polozka[0]] = polozka[1]

# načtení slov k segmentaci uspořádaných do sloupce - resp. lze měnit zmenout hodnoty separatoru (a odstranění případné mezery na konci)
with open(INPUT_FILE, encoding="UTF-8") as soubor:
    slova_k_segmentaci = soubor.read().strip().split(sep="\n")

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

# uložení výsledku segmentace do souboru
with open(OUTPUT_FILE, mode="x", encoding="UTF-8") as soubor:
    print(text_segmentovany_slouceny, file=soubor)
