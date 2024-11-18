# Capstone verkefni 
### Uppsetning
- Downloadið PowerBI desktop
- Hafið Python sett upp í tölvunni ykkar


## Regex
**Notið þetta til að keyra**

1. Þarft að vera með skjalið 'REGEX_Linkar.txt'
2. Þarft að vera með skjalið 'REGEX_Vinbudin.py'
3. Fara í Terminal og skrifa part 4
4. python3 REGEX_Vinbudin.py
5. Run kóðan sem gefur þér skjal sem heitir 'Bjor_Vinbudin.csv'


##  Mælaborð:
Downloadið eftirfarandi skrám og opnið í PowerBI desktop (Mögulega hægt að opna á vefútgáfu)
- Bjórkort.pbix
- Hjól_Winrate.pbix

**Í þessu verkefni**

Í þessu verkefni er verið að ná í upplýsingar um bjór verð út úr versýðunni vínbúðin.is

Þessi kóði,
1. Imports,
2. Er "load_urls_from_file(file_name)" Þetta les skrá 'REGEX_Linkar.txt' sem inniheldir linka að "vefsíðum"
3. Er "fetch_html" Þetta leyfir okkur að ná í upplýsingar frá vefsýðum á netinu.
4. Er "parse_html" þetta safnar upplýsingar um nafn, verð og rúmmál bjóra sem teknar eru frá vefsýðu "vínbúðin.is"
5.  "save_results" vistar upplýsingarnar sem safnaðar voru úr vefsýðunni og setur þær í dálka "Bjór", "Verð (Kr)" og "Stærð (ml)"
6. Er "__name__" þetta er notað til keyra kóðan sem safna upplýsingum frá "REGEX_Linkar.txt", þannig allir ættu að geta keyrt kóðan og fengið upplýsingarnar.