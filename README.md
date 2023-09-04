
# Zápočtový program

## Zadání problému

Aplikace pro doporučování filmů, která využívá zpětné vazbě uživatele ke konrétním návrhům.
Vytváří si uživatelský profil, na jehož základě vybírá nejvíce vhodné filmy. Je přidáná možnost si oblíbené filmy uchovat pro zpětné nalezení.


## Uživatelská část

Program se spustí pomocí souboru **main.py**.

Na uživatele vyskočí okénko s grafickým rozhraním, které nabízí uživateli film a relevantní informace.
Uživatel má 2 volby: Like a Dislike. Tímto vyjádří svůj názor na aktuálně doporučovaný film.

Pokud uživatel zaklikne tlačítko Like, program vezme v potaz jeho reakci pro další doporučení. Zároveň vyskočí nové okénko s nabídkou přidat film do seznamu filmů, které by si mohl uživatel chtít pustit, tzv. **„watchlistu“**.

Pokud uživatel zaklikne tlačítko Dislike, program pouze využije zpětné vazby pro další práci. Žádná další akce se nekoná a program doporučí další film.

Z počátku se uživateli postupně ukáže 10 náhodných filmů, aby se mohl vybudovat jeho uživatelský profil a program tak zjistil jeho preference. Po těchto 10 filmech začíná program doporučovat filmy na základě podobnosti jednotlivých filmů s uživatelským profilem.

Pro skončení programu je neustále zobrazeno tlačítko **End Program**. Po jeho stisknutí se uživateli zobrazí jeho **watchlist** a na závěr mu doporučí 10 filmů, které mají největší shodu s jeho uživatelským profilem.


## Programátorská část

### Filmová databáze

Pro tento program jsem použil databázi filmů [IMDB 5000 Movie Dataset](https://www.kaggle.com/datasets/carolzhangdc/imdb-5000-movie-dataset/).

Po sérii úprav pro zlepšení práce s databází zbylo 4660 filmů, z nichž kždý obsahuje tyto informace: ***Název filmu, Rok vydání, Skóre z IMDb, Délka trvání filmu, Režisér, Herec v hlavní roli, Žánry*** a ***Klíčová slova popisující děj***. 

Původní databáze obsahovala více informací, avšak pro zjednodušení chodu programu jsem databázi redukoval na výše uvedené informace. Kompletní databáze je uložena v souboru **movie_metadata.csv** ve složce **additional data** společně s dalšími soubory, které byly použity během tvorby programu.

### Uživatelský profil a pojetí filmů jako vektory

Každému filmu z celková databáze **A_complete_data.csv** je vytvořen vektor o dimenzi 1399 reprezentující 24 žánrů, 974 nejčastějších klíčových slov, 188 nejčastějších herců a 213 nejčastějších herců.

Jednotlivé hodnoty jsou vypočteny pomocí metody **TF-IDF** (=Term Frequency - Inverse Document Frequency). Hodnota TF určuje počet výskytů pojmu u jednoho filmu a hodnota IDF důležitost pojmu pro celou databázi. Proto u každého pojmu, který je použit pro tvorbu vektoru je spočten jeho výskyt v celé databázi a také jeho hodnota IDF, která se počítá jako **ln(počet všech filmů = 4660 / počet výskytů daného pojmu)**. Pro vypočtení a zápis byl použit soubor **idf_calculation.py**.

Kromě žánrů, kterých není mnoho, jsou ostatní pojmy vybrány tak, aby se v celkové databázi objevili alespoň 5krát. Jednak pro zmenšení dimenze vektorů, které by reprezentovaly filmy. A taky proto, že filmy, které obsahují pojmy, jež se v databázi moc nevyskytují, nejsou příliš relevantní pro doporučování dalších filmů, které pravděpodobně tyto pojmy obsahovat nebudou.

Filmové vektory byly vytvořeny pomocí souboru **vector.py**.
Tyto filmové vektory jsou znormovány pomocí souboru **normalize.py** pro jednodušší počítání a zacházení při dalších operacích.

Uživatelský profil je z počátku def. jako nulový vektor o dimenzi 1399. 

Pokud uživatel na film reaguje kladně, uživatelský vektor se aktualizuje jako aritmetický průměr mezi dosavadním uživatel. vektorem a znormovaným vektorem filmu, na které právě reagoval.
Při negativní reakce se dělá aritmetický průměr s opačným filmovým vektorem, tj. vynásobený (-1). Jelikož je většina prvků vektoru 0, nesníží se u uživatelského vektoru jiné hodnoty, než ty, které film obsahoval.

### Doporučování filmů

Po prvních 10 filmech začne program sám doporučovat filmy, které si myslí, že by se uživateli mohli líbit. Tutuo měřitelnou hodnotu počítá pomocí _Kosinové podobnosti_ vektoru uživatele a vektoru filmu. Jelikož jsou oba vektory znormované, je jejich podobnost rovna skalárnímu součinu. 

Pro výpočet kosinové podobnosti je využita funkce **cosine_similarity** v souboru **backend.py**. Pro doporučování filmů je použita funkce **get_recommendation**, která vybere film s největší kosinovou podobností a navrhne ho uživateli. Zároveň každý již doporučený film je přidán do seznamu **already_recommended**, který uchovává identifikační čísla doporučených filmů, aby žádný film nebyl navržen dvakrát.

## Závěr
V programu jsou použité knihovny jako **csv, numpy, random a tkinter** pro snadnější práci s csv soubory, složité výpočty a pro tvorbu grafického rozhraní. 

Ve většině souborů se nachází poznámky (v angličitně) vysvětlující jednotlivé kroky a pro lepší pochopení. 

U několika csv souborů je použit středník („ ; “) z důvodu čárek, které se vyskytují v názvu některých filmů. Zároveň jsem zahrnul i soubory použité pro úpravu a prácí s databází, které byly často použity pro vícero souborů, a proto jsou označení v nich velmi neurčitá a neutrální.

