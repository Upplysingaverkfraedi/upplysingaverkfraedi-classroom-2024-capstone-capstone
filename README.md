# Capstone verkefni 
### Uppsetning
- Downloadið PowerBI desktop
- Hafið Python sett upp í tölvunni ykkar


## Regex
Notið þetta til að keyra

python REGEX_Vinbudin_kodi2.py --output_dir ./data --debug

##  Mælaborð:
Downloadið eftirfarandi skrám og opnið í PowerBI desktop (Mögulega hægt að opna á vefútgáfu)
- Bjórkort.pbix
- Hjól_Winrate.pbix



# Upplýsingar um regex
Í þessu verkefni er verið að ná í upplýsingar um bjór verð út úr versýðunni vínbúðin.is

Þessi kóði,

- Imports, 
- Er "load_urls_from_github" Þetta nær í lista af url frá github frá "REGEX_Linkar.txt".

- Er "fetch_html" Þetta leyfir okkur að ná í upplýsingar frá vefsýðum á netinu.

- Er "parse_html" þetta safnar upplýsingar um bjór, sem teknar eru frá vefsýðu "vínbúðin.is"

- "save_results" vistar upplýsingarnar sem safnaðar voru úr vefsýðunni og setur þær í dálka "Nafn", "Verð (Kr)" og "ml"

- Er "name" þetta er notað til að sýna hvaða versýður linka á að safna upplýsingum frá "REGEX_Linkar.txt" frá github main, þannig allir ættu að geta keyrt kóðan og fengið upplýsingarnar.
