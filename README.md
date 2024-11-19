# Capstone verkefni - Samanburður leikarana Kate Winslet og Leonardo Dicaprio

## TL;DR
Í þessu verkefni er borið saman feril og vinsældir Leonardo DiCaprio og Kate Winslet út frá gögnunum á Rotten Tomatoes og IMDb. Markmiðið var að greina þróun ferils þeirra, árangur út frá gagnrýnenda- og áhorfendaeinkunnum, og aðra mælikvarða eins og tegundir kvikmynda, leikstjóra og áhorfendafjölda.
    Gögnin voru sótt frá Rotten Tomatoes og IMDb, unnin með SQL og Python, og sett fram á mælaborði í RStudio Shiny. Myndrænar greiningar sýna að DiCaprio hefur hækkað í áliti bæði gagnrýnenda og áhorfenda með árunum, á meðan Winslet sýnir meiri sveiflur og lægri meðaleinkunn. Báðir leikarar leika að mestu í dramatískum myndum og eru vinsælastir í kvikmyndum með strangari aldurstakmörkun (R og PG-13).
    Mælaborðið, ásamt tengslaneti fyrir kvikmyndir, auðveldaði greiningu og framsetningu. Í verkefninu voru notuð SQL, RegEx, og önnur greiningartól sem tengjast námsefninu, sem skilaði bæði dýpri innsýn á gögnin og dró fram áhugaverðar niðurstöður. Verkefnið varpar ljósi á hvernig gögn má nýta til að svara spurningum um feril leikara og þróun þeirra.


## Strúktúr

- `code`mappan: Inniheldur öll nauðsynleg forrit sem þarf til að búa til gagnagrunn
- `data` mappan: Inniheldur gagnagrunninn í formi binary skrár og csv skránna sem notuð var við gerð gagnagrunns
- `capstone_docs` mappan: Inniheldur rmd skjal með mælaborðinu ásamt skýrslu í formi html skráar.


## Uppsetning Gagnagrunns 

### Nauðsynleg bókasöfn 

### í python: 

```
import sqlite3
from imdb import Cinemagoer
import time
import re
import pandas as pd
import unicodedata
from difflib import get_close_matches
import requests
from bs4 import BeautifulSoup
import networkx as nx
import dash
from dash import dcc, html, Input, Output, State
import plotly.graph_objects as go
from itertools import combinations
```

Við útfærðum skjalið, `requirements.txt`, sem má finna í code möppunni sem inniheldur þá pakka sem eru ekki innbyggðir í python. Til að hlaða þeim pökkum er hægt að keyra skipunina:

```
pip3 install -r code/requirements.txt
```

### Í R: 

```
library(shiny)
library(dplyr)
library(tidyr)
library(ggplot2)
library(DBI)
library(RSQLite)
library(stringr)
library(bslib)
library(plotly)
library(lubridate)
```
Hægt er að downloada pökkunum í console með skipuninni: 

```
install.packages("Nafn_pakka")
```

Einnig þarf að hafa python3, sjá vefsíðu: https://www.python.org/downloads/

og R, sjá vefsíðu: https://cran.r-project.org/

Þegar búið er að hlaða inn öllum viðeigandi pökkum er hægt að hefjast við gerð gagnagrunnsins.

### 1. rotten_tomatoes_movies

Við lesum gögnin úr csv skránni okkar sem heitir `rotten_tomatoes_movies2.csv` sem hægt er að finna í data möppunni. 
Til þessu að búa til sql töflu úr csv skránni okkar notum við forritið `create_db2.sql` sem er að finna í code möppunni. 

Við búum til töfluna með því að keyra eftirfarandi skipun ef unnið er á unix-skel (macOS eða Linux): 

```
sqlite3 data/rotten_tomatoes.db < code/create_db2.sql
```
En ef unnið er á Windows PowerShell er keyrst skipunina:
```
Get-Content code/create_db2.sql | sqlite3 data/rotten_tomatoes.db
```

Nú verður til rotten_tomatoes.db skjal í data möppunni ykkar sem inniheldur töfluna rotten_tomatoes_movies. 
Til að skoða töfluna betur er hægt að keyra: 

```
sqlite3 data/rotten_tomatoes.db 
```
í terminal/cmd og síðan:
```
sqlite> select * from rotten_tomatoes_movies limit 10; 
```
Þá ættuð þið að sjá fyrstu tíu línurnar í töflunni. 

Síðan þarf að bæta við dálkinum movie_id í töfluna okkar. Það er einfaldlega dálkur sem gefur hverri kvikmynd id númer sem hægt er að nýta seinna meir til að gera fleiri töflur. Það eru nokkrar leiðir til að gera þetta en við gerðum þetta í R, það hefði líklegra verið hentugra og einfaldara að nota AUTOINCREMENT þegar búið var til töfluna, það hefði verið hægt með því að hafa efst í forritinu `create_db2.sql`:

```
CREATE TABLE rotten_tomatoes_movies (
    movie_id INTEGER PRIMARY KEY AUTOINCREMENT,
```

Við bjuggum til dálkinn með því að keyra í R markdown skjali: 

```
library(DBI)
library(RSQLite)

# Tengist SQLite gagnagrunninum
conn <- dbConnect(RSQLite::SQLite(), "path/to/your/data/rotten_tomatoes.db")

# Les gögnin inn úr töflunni í gagnagrunninum til að skoða gögnin ef þú vilt
rotten_tomatoes_data <- dbReadTable(conn, "rotten_tomatoes_movies")

# Býr til nýjan dálk með einkvæmum ID fyrir hverja mynd
rotten_tomatoes_data$movie_id <- seq.int(nrow(rotten_tomatoes_data))

# Fjarlægir gamla útgáfu af töflunni ef hún er til
if ("rotten_tomatoes_movies" %in% dbListTables(conn)) {
  dbRemoveTable(conn, "rotten_tomatoes_movies")
}

# Skrifar uppfærðu gögnin með movie_id dálknum aftur inn í gagnagrunninn
dbWriteTable(conn, "rotten_tomatoes_movies", rotten_tomatoes_data, overwrite = TRUE)

# Lokar tengingunni
dbDisconnect(conn)
```
Passa þarf að "path/to" sé rétt slóð til að forritið nái að lesa gögnin. En eftir þessa keyrslu ætti dálkurinn movie_id að vera komin inní töfluna. 

### 2. rotten_tomatoes_movies_dicaprio_winslet

Nú getum við síað gögnin okkar og búið til nýja töflu sem inniheldur aðeins myndir sem að Leonardo Dicaprio eða Kate Winslet léku í: 
Til þess að gera það er notað forritið `leo_kate.sql`. Það forrit er staðsett í code möppunni. 

Hægt að búa til töfluna með því að keyra skipunina í cmd/terminal: 

Í macOS epa Linux:
```
sqlite3 data/rotten_tomatoes.db < code/leo_kate.sql
```
En í Windows tölvu: 

```
Get-Content code/leo_kate.sql | sqlite3 data/rotten_tomatoes.db
```

Nú ætti að verða til tvær töflur inná rotten_tomatoes.db sem heita rotten_tomatoes_movies_dicaprio_winslet og rotten_tomatoes_movies. 

Einnig þarf að uppfæra genres dálkinn sem að lætur óalgengar tegundir verða að "other". Þetta er gert með forritinu `genres.py`:
Keyra þarf skipunina:

```
python3 code/genres.py
```
Þá ætti genres dálkurinn í töflunni `rotten_tomatoes_movies_dicaprio_winslet` að vera uppfærður.

## 3. leo_movies og kate_movies

Einnig þarf að búa til töflurnar `leo_movies` og `kate movies`, sem aðskilur töfluna `rotten_tomatoes_movies_dicaprio_winslet`. Þetta er einfaldlega gert með forritunum leo_movies.py og kate_movies.py

Keyra þarf skipanirnar:
```
python3 code/kate_movies.py
```
og 

```
python3 code/leo_movies.py
```
Þegar búið er að gera þessar töflur þarf að búa til töfluna `content_rating_count` sem að mun hjálpa við hönnun mælaborðsins. Þetta er gert með forritinu `content_rating_count.py`. Keyra þarf skipunina:

```
python3 code/content_rating_count.py
```


### 4. movie_actors

Til að gera töfluna okkar, `movie_actors` notum við forritið `create_actor.py` í code möppunni.
Til að búa til töfluna getum keyrt skipunina: 

```
python3 code/create_actor.py
```
Þá ætti að verða til þriðja taflan í rotten_tomatoes.db filenum okkar sem heitir movie_actors. Athugið að actor_id dálkurinn er bara með NA gildum, en það er í lagi því að við eigum eftir að setja inn viðeigandi id í þann dálk seinna. 

### 5. actors_info

Forritið sem við notum heitir `createactors_info` og er að finna í code möppunni. Búið er til töfluna með því að keyra skipunina:

```
python3 code/createactors_info.py
```
Ef það kemur upp villa við þessa keyrslu, þarf líklegast að keyra með python, ekki python3 (jafnvel þó að python3 sé þegar í tölvunni).

Athugið að þessi keyrsla mun taka mjög langan tíma þar sem að Cinemagoer er frekar hægvirkur pakki og einnig erum við með mikið af leikurum í töflunni okkar. Það er þó hægt að stoppa keyrsluna og upplýsingarnar sem forritið var búið að sækja mun commitast inni á töfluna. Síðan þegar hafið er aftur keyrslu mun forritið aðeins sækja þau gögn sem hafa ekki verið "processed". Eftir þessa keyrslu ætti einnig actor_id dálkurinn í töflunni `movie-actors` að vera uppfærður með viðeigandi IMDb ID. Fyrir þetta verkefni þurfum við helst upplýsingar um Kate Winslet og Leonardo DiCaprio. Því er hægt að ljúka keyrslunni þegar þau eru komin inn, til að stytta tíma. 

Til að sækja fleiri upplýsingar í actors_info töfluna, þ.e mini_biography, trivia og highest paid movie og salary er notað forritið `get_biography.py`. Hægt er að keyra forritið með skipuninni:

```
python3 code/get_biography.py
```
Ef það kemur upp villa við þessa keyrslu, þarf líklegast að keyra með python, ekki python3 (jafnvel þó að python3 sé þegar í tölvunni).

Athugið að þessi keyrsla tekur tíma, en ef stoppað er keyrslu munu þær upplýsingar sem forritið er búið að sækja commitast, því er nóg að stoppa keyrslu þegar upplýsingar fyrir Leonardo DiCaprio og Kate Winslet eru komin inn, uppá virkni mælaborðsins. En það er þó auðvitað hægt að keyra þetta fyrir alla leikarana, ætti ekki að taka jafn langan tíma og að keyra `createactors_info`

### 6. main_actors_in_info

Til að búa til töfluna `main_actors_in_info`, sem seinna meir verður notuð til að byggja upp tengslanet, notum við forritið `actors_in_info`. Keyra skal skipunina: 

```
python3 code/actors_in_info.py
```
### 7. Töflur fyrir directors graf

Að lokum þarf að bæta við töflunum `all_movies_audience_directors` , `all_movies_tomatometer_directors` , `top10_audience_movies` og `top10_tomatometer_movies` til að gera graf til að skoða dreifni einkunna meðal top 10 leikstjóra. Notað er forritið `directors.py`, sem býr til allar 4 töflurnar. Keyrt er skipunina: 
```
python3 code/directors.py
```


Eftir þetta ferli ættu töflurnar `rotten_tomatoes_movies`, `rotten_tomatoes_movies_dicaprio_winslet`, `leo_movie`, `kate_movies`, `content_rating_count`, `movie_actors`, `actors_info`, `main_actors_in_info`, `all_movies_audience_directors` , `all_movies_tomatometer_directors` , `top10_audience_movies` og `top10_tomatometer_movies` að vera komnar í gagnagrunninn rotten_tomatoes.db



## Uppsetning mælaborðs

Mælaborðið er hannað í R Markdown skjali, við notuðum Rstudios. Í capstone_docs möppunni er skjal sem heitir Maelabord.rmd. Hlaðið því niður í tölvuna ykkar. 

Þið þurfið að breyta path to í viðeigandi heiti: 

conn <- dbConnect(SQLite(), "path/to/your/data/rotten_tomatoes.db")


Áður en keyrt er skjalið þarf fyrst að keyra forritið `tengslanet3.py` sem má finna í code möppunni. Þetta gerum við til að skoða tengslanetið í mælaborðinu.
Hægt er að keyra forritið með skipuninni: 

```
python3 code/tengslanet3.py
```
**Athugið: Python-forritið verður að vera í keyrslu á meðan mælaborðið er keyrt.**

Þegar búið er að skoða mælaborðið er mikilvægt að hætta keyrslunni á `tengslanet3.py` með `Ctrl + C`, **Ekki hætta keyrslu með `Ctrl + Z`**. Ef það er gert, mun forritið áfram halda sambandi við port númerið, sem veldur því að portið verður óaðgengilegt næst þegar forritið er keyrt.

Í því ólíklega tilfelli að óvart er ýtt á `Ctrl+Z` til að hætta keyrslu, og þið viljið aftur skoða mælaborðið er hægt að laga vandamálið með því að breyta portnúmerinu í forritinu, og síðan þarf að breyta portnúmerinu í mælaborðinu. 

Getið breytt inni á tengslanet3.py: 

```
# breyta í t.d bara 8064
app.run_server(debug=True, port=8063)
```
og síðan breyta í mælaborðinu:
```
  tabPanel(
      "Tengslanet",
      h3("Tengslanet fyrir aðalleikara"),
      tags$iframe(src = "http://127.0.0.1:8063/", height = "600", width = "100%")
    )
# Breyta http://127.0.0.1:8063/ yfir í //127.0.0.1:8064/
# Þarf að vera sama port númer og er í forritinu
```
En þetta vandamál ætti ekki að koma upp ef það er notað bara `Ctrl + C`











  
