## Regex
Notið þetta til að keyra

python REGEX_Vinbudin.py


##  Mælaborð:
Downloadið eftirfarandi skrá og opnið í PowerBI desktop (Mögulega hægt að opna á vefútgáfu)

Mælaborð.pbix

**Í þessu verkefni**

Í þessu verkefni er verið að ná í upplýsingar um bjór, verð og stærð (ml) út úr HTML frá versýðunni vínbúðin.is

Þessi kóði var gerður með gömul verkefni -martell hóps við hlið

Stutt útskýring á kóðanum,
Part 1. Imports,
Part 2. Er "load_urls_from_file(file_name)" Þetta les skrá 'REGEX_Linkar.txt' sem inniheldir linka að "vefsíðum"
Part 3. Er "fetch_html" Þetta leyfir okkur að ná í upplýsingar frá vefsýðum á netinu.
Part 4. Er "parse_html" þetta safnar upplýsingar um nafn, verð og rúmmál bjóra sem teknar eru frá vefsýðunni "vínbúðin.is"
Part 5. "save_results" vistar upplýsingarnar sem safnaðar voru úr vefsýðunni og setur þær í dálka "Bjór", "Verð (Kr)" og "Stærð (ml)"
Part 6. Er "__name__" þetta er notað til keyra kóðan sem safna upplýsingum frá "REGEX_Linkar.txt", þannig allir ættu að geta keyrt kóðan og fengið upplýsingarnar.