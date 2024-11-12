**Notið þetta til að keyra**

Þarft að vera með skjalið 'REGEX_Linkar.txt'

python REGEX_Vinbudin_kodi.py


**Í þessu verkefni**

Í þessu verkefni er verið að ná í upplýsingar um bjór verð út úr versýðunni vínbúðin.is

Þessi kóði,
1. Imports,
2. Er "load_urls_from_github" Þetta nær í lista af url frá github frá "REGEX_Linkar.txt".
3. Er "fetch_html" Þetta leyfir okkur að ná í upplýsingar frá vefsýðum á netinu.
4. Er "parse_html" þetta safnar upplýsingar um bjór, sem teknar eru frá vefsýðu "vínbúðin.is"
5.  "save_results" vistar upplýsingarnar sem safnaðar voru úr vefsýðunni og setur þær í dálka "Nafn", "Verð (Kr)" og "ml"
6. Er "__name__" þetta er notað til að sýna hvaða versýður linka á að safna upplýsingum frá "REGEX_Linkar.txt" frá github main, þannig allir ættu að geta keyrt kóðan og fengið upplýsingarnar.