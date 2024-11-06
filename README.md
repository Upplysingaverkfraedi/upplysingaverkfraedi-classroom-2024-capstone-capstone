## Keyrsla
Til þess að keyra þarftu að setja allt í sama directory þ.e:

```bash
Logos-mappa með öllum png myndum sem eru
Premier_league.db
```
Þú opnar síðan kóðann:
```bash
ShinyR.Rmd
```
inn í RStudio umhverfi í R Markdown skjali

# ATH: Passaðu að downloada í console eftirfarandi pökkum með skipun!!

```bash
install.packages("tidyverse")
install.packages("rvest")
install.packages("dplyr")
install.packages("DBI")
install.packages("RSQLite")
install.packages("shiny")
install.packages("ggplot2")
install.packages("plotly")
install.packages("shinyjs")
install.packages("shinydashboard")
install.packages("DT")
install.packages("sf")
install.packages("leaflet")
install.packages("ggimage")
```

# ATH: Passaðu sérstaklega að breyta file-paths þannig þau passi við hvar t.d. Logos mappan er á ÞINNI tölvu sama á við með premier_league.db!!
T.d. svona 
- con <- dbConnect(RSQLite::SQLite(), "C:/Users/jakob/Desktop/capstone-thereach/premier_league.db") kemur tvisvar fyrir í skjalinu
- mutate(Logo_url = paste0("C:/Users/jakob/Desktop/capstone-thereach/Logos/", str_replace_all(Team, " ", "_"), ".png")) kemur einu sinni í skjalinu


Þegar kóðinn uppsettur inn í RStudio þá keyriru eftirfarandi "chunk" af kóðum einn í einu byrjar efst. Keyrir þá með keyrsluhnapp í horni hvers kóðabúts. 
Þangað til að lokum kemuru að:

```{r}
shinyApp(ui, server)
```

og með því að keyra hann ætti vefsíðan að opnast



## Mælaborðin
Þú ættir þá að fá upp Shiny með mælaborðunum:
- Heim
- Síðustu ár
- Stöðutafla
- Staðsetningar
- Færanýtni
- BetStatistics
- Dómararýni
- Liðin

Í hverju mælaborði eru mismunandi takkar og hlutir til að fikta í gröfunum og niðurstöðunum