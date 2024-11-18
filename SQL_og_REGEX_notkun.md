# SQL, REGEX og notkun þess til að setja upp gagnagrunn

## SQLite
SQL kóðinn: [Mælaborð.sql](Mælaborð.sql) býr til gagnagrunninn [Bjórgrunnur.db](Bjórgrunnur.db), býr til eftirfarandi 5 töflur:
- Bjór_Vínbúðin úr csv-skránni:  [Bjor_Vinbudin.csv](data/Bjor_Vinbudin.csv) þar sem kemur fram nafn bjórs, verð hans og stærð í mL.
- Bjór úr csv-skránni:           [Bjor.csv](data/Bjor.csv) þar sem kemur fram nafn bars, verð allra bjóra á dælu sem seldir eru á þeim stað og stærð þeirra í mL. Þar að auki kemur fram meðalverð á bjórum á hverjum stað ásamt meðal lítraverði. Einnig eru upplýsingar um staðsetningu hvers bars ásamt slóða af myndum.
- Happy_Hour úr csv-skránni:     [Happy_Hour.csv](data/Happy_Hour.csv) þar sem kemur fram nafn bars, byrjunar- og endatíma Happy Hour verð allra bjóra á dælu sem seldir eru á þeim stað og stærð þeirra í mL. Líkt og í töflunni að ofan kemur einnig fram meðalverð á bjórum á hverjum stað ásamt meðal lítraverði.
- Lukkuhjól úr csv-skránni:      [Lukkuhjol.csv](data/Lukkuhjol.csv) þar sem kemur fram verð hvers snúnings, allir möguleikir vinningar. Einnig kemur fram líkur þess að græða pening, tapa pening, enda á sléttu, vinna eitthvað eða vinna ekkert.
- Bjórkort úr töflunni "Bjór" þar sem taflan er sett upp með unpivot-sniði. Þá er Ein lína fyrir hvern bjór á hverjum bar í stað þess að hver lína innihaldi alla bjóra á hverjum stað. Einnig voru línum með engum bjór teknar út. Þetta leiddi til þess að taflan er t.d. með 3 línur fyrir bar sem selur 3 bjóra o.s.frv.

Loks voru bættir við dálkar fyrir meðalverð á hverjum bjór og meðal lítraverðum í miðbænum inn í Bjór_Vínbúðin töfluna ásamt lítraverðum á bjórum í vínbúðinni inn í Bjór_Vínbúðin töfluna.

## Regex
Kóðinn les skrána: [REGEX_Linkar.txt](REGEX_Linkar.txt) sem inniheldur slóðir að bjórum í vínbúðinni.
Þar næst sækir kóðinn html upplýsingar og notar REGEX skipun til að safna upplýsingum um nafn, verð og stærð bjóranna.
Upplýsingarnar eru vistaðar í skrána: [Bjor_Vinbudin.csv](data/Bjor_Vinbudin.csv) með dálkunum "Bjór", "Verð (Kr)" og "Stærð (ml)"


# Keyrsla kóðanna - Uppsetning gagnagrunns
## Uppsetning
Til að keyra kóðanna gaktu úr skugga að eftirfarandi sé sett upp á tölvunni þinni:
- Python
- SQLite3

- Eftirfarandi pakka þarf að setja upp í python með:
```python
pip install re
pip install requests
pip install pandas
pip install datetime
pip install os
```

### Gakktu úr skugga um að þú sért með eftirfarandi skrár:
[REGEX_Linkar.txt](REGEX_Linkar.txt)
Data möppu með:
- [Bjor.csv](data/Bjor.csv)
- [Happy_Hour.csv](data/Happy_Hour.csv)
- [Lukkuhjol.csv](data/Lukkuhjol.csv)

## Keyrsla
Keyrið í þessarri röð:
#### 1
```bash
python3 REGEX_Vinbudin.py
```
Gakktu úr skugga um að skráin [Bjor_Vinbudin.csv](data/Bjor_Vinbudin.csv) hafi birtst í [Data](data) möppuna.

#### 2
```bash
sqlite3 Bjórgrunnur.db ".read Mælaborð.sql"
```
Gakktu úr skugga um að [Bjórgrunnur.db](Bjórgrunnur.db) hafi verið búinn til. 

## Tengja gagnagrunn við PowerBI ()
1. Opnaðu ODBC Data Sources (64-bit) forrtið (ætti að vera til staðar, annars þarf að downloada því)-
   a. Veljið Add og finnið "SQLite3 ODBC Driver" (ætti að vera til staðar annars þarf að downloada driver [hér]([Bjórgrunnur.db](https://marketplace.visualstudio.com/items?itemName=DevartSoftware.SQLiteODBCDriver3264bit)) og nota hann.
   b. Skýrið gagnagrunninn einhverju nafni og veljið þrjá punktana hjá "Database" of finnið [Bjórgrunnur.db](Bjórgrunnur.db) skrána.
   c. Veljið "Ok"
2. Opnið Power BI og búið til "Blank Report" ef vilji er fyrir að byrja frá grunni, annars opnið [Mælaborð.pbix](Mælaborð.pbix)
3. Veljið "Get Data" og leitið að "ODBC"
4. Veljið gagnagrunnin sem þið skýrðuð í skrefi 1b
5. Veljið Windows og "Use my current credentials" í ODBC driver 
