# Capstone verkefni 

## Uppsetning Gagnagrunns 

Við lesum gögnin úr csv skránni okkar sem heitir **rotten_tomatoes_movies2.csv** sem hægt er að finna í data möppunni. 

Það þarf að hlaða niður þeirri skrá á viðeigandi stað (hentugast að hafa data möppu). 

Til þessu að búa til sql töflu úr csv skránni okkar notum við forritið **create_db2.sql** sem er að finna í code möppunni. 

Hlaða þarf þeirri skrá, og helst hafa hana í code möppu. 

Við búum til töfluna með því að keyra eftirfarandi skipun á terminal/cmd: 

```
sqlite3 data/rotten_tomatoes.db < code/create_db2.sql
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

Síðan þurfum við að bæta við dálkinum movie_id í töfluna okkar. Það er einfaldlega dálkur sem gefur hverri kvikmynd id númer sem hægt er að nýta seinna meir til að gera fleiri töflur. Það eru nokkrar leiðir til að gera þetta en ég gerði þetta í R. Ég keyrði bútinn: 

```
library(DBI)
library(RSQLite)

# Tengist SQLite gagnagrunninum
conn <- dbConnect(RSQLite::SQLite(), "Documents/GitHub/capstone-the-north/data/rotten_tomatoes.db")

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
Til að keyra þennan bút í R þarf að hafa bókasöfnin DBI og RSQLite. Hægt að er að downloada þeim í console með því að keyra: 

```
install.packages(RBI)
```
og 

```
install.packages(RSQLite)
```

Passið að "path/to" sé rétt slóð til að forritið nái að lesa gögnin. En eftir þessa keyrslu ætti dálkurinn movie_id að vera komin inní töfluna ykkar. 

Til að vera viss um að dálkurinn sé kominn inní töfluna er hægt að fara aftur í terminal/cmd og keyra: 

```
sqlite3 data/rotten_tomatoes.db 
```

```
sqlite> select * from rotten_tomatoes_movies limit 10; 
```
til að skoða töfluna. 

Nú getum við síað gögnin okkar og búið til nýja töflu sem inniheldur aðeins myndir sem að Leonardo Dicaprio eða Kate Winslet léku í: 

Til þess að gera það þarf að hlaða niður forritinu leo_kate.sql. Það forrit er staðsett í code möppunni. 

Þegar búið er að hlaða því niður á viðeigandi stað er hægt að búa til töfluna með því að keyra skipunina: 

```
sqlite3 data/rotten_tomatoes.db < leo_kate.sql
```
inná terminal/cmd. 

Nú ætti að verða til tvær töflur inná rotten_tomatoes.db sem heita rotten_tomatoes_movies_dicaprio_winslet og rotten_tomatoes_movies. 
Til að vera viss um að báðar töflur séu til staðar er hægt að gera 

```
sqlite3 data/rotten_tomatoes.db
sqlite> .tables
```
Þá ættuð þið að sjá báðar töflur. Síðan til að sjá innihald töflunnar getið þið gert: 

```
sqlite3 data/rotten_tomatoes.db
sqlite> select * from rotten_tomatoes_movies_dicaprio_winslet limit 10;
```

líkt og áðan 








Nauðsynleg bókasöfn: 

```
import sqlite3
```


  
