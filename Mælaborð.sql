-- Gagnagrunnur búinn til
.open Bjórgrunnur.db

------------------------------------------------------------------------------------------------
-- 1

-- Tafla með bjórum úr Vínbúðinni
------------------------------------------------------------------------------------------------

-- Tafla búin til
DROP TABLE IF EXISTS Bjór_Vínbúðin;
CREATE TABLE IF NOT EXISTS Bjór_Vínbúðin (
    Bjór TEXT,
    "Verð (Kr)" INTEGER,
    "Stærð (mL)" INTEGER
);

-- Gögn frá "Bjor_Vinbudin.csv" sett inn í töflu og aukadálk eytt
.mode csv
.import ".\\data\\Bjor_Vinbudin.csv" Bjór_Vínbúðin
DELETE FROM Bjór_Vínbúðin WHERE Bjór = 'Bjór';

-- Nöfn uppfærð í samræmi við Bjór töfluna
UPDATE Bjór_Vínbúðin SET Bjór = 'Gull' WHERE Bjór = 'Egils Gull';
UPDATE Bjór_Vínbúðin SET Bjór = 'Boli' WHERE Bjór = 'Boli Premium';
UPDATE Bjór_Vínbúðin SET Bjór = 'Peroni' WHERE Bjór = 'Peroni Nastro Azzurro';
UPDATE Bjór_Vínbúðin SET Bjór = 'Einstök Pale Ale' WHERE Bjór = 'Einstök Arctic Pale Ale';
UPDATE Bjór_Vínbúðin SET Bjór = 'Eldgos' WHERE Bjór = 'Eldgos Flamingo Kokteill';
UPDATE Bjór_Vínbúðin SET Bjór = 'Somersby' WHERE Bjór = 'Somersby Apple';
UPDATE Bjór_Vínbúðin SET Bjór = 'Blanc' WHERE Bjór = 'Kronenbourg 1664 Blanc';
UPDATE Bjór_Vínbúðin SET Bjór = 'Bríó' WHERE Bjór = 'Bríó nr. 1 Pilsner';
UPDATE Bjór_Vínbúðin SET Bjór = 'Garún' WHERE Bjór = 'Garún nr. 19 Icelandic Stout';
UPDATE Bjór_Vínbúðin SET Bjór = 'Helga' WHERE Bjór = 'Helga nr. 69 Raspberry Sour';
UPDATE Bjór_Vínbúðin SET Bjór = 'Snorri' WHERE Bjór = 'Snorri nr. 10 íslenskt öl';
UPDATE Bjór_Vínbúðin SET Bjór = 'Úlfrún' WHERE Bjór = 'Úlfrún nr. 34';
UPDATE Bjór_Vínbúðin SET Bjór = 'Úlfur' WHERE Bjór = 'Úlfur nr. 3 India Pale Ale';
UPDATE Bjór_Vínbúðin SET Bjór = 'Guinness' WHERE Bjór = 'Guinness Draught';
UPDATE Bjór_Vínbúðin SET Bjór = 'Bóndi' WHERE Bjór = 'Bóndi Session IPA';


------------------------------------------------------------------------------------------------
-- 2

-- Tafla með bjórum úr bænum
------------------------------------------------------------------------------------------------

-- Tafla búin til
DROP TABLE IF EXISTS Bjór;
CREATE TABLE IF NOT EXISTS Bjór (
    Bar TEXT,
    "Stærð (mL)" INTEGER,
    Latitude REAL,
    Longitude REAL,
    "Meðalverð (kr)" INTEGER,
    "Meðal Lítraverð (kr)" INTEGER,
    Gull INTEGER,
    "Gull Lite" INTEGER,
    "Tuborg Grön" INTEGER,
    "Tuborg Classic" INTEGER,
    "Víking Gylltur" INTEGER,
    "Víking Lite" INTEGER,
    "Víking Lite Classic" INTEGER,
    Thule INTEGER,
    Carlsberg INTEGER,
    Boli INTEGER,
    Peroni INTEGER,
    "Stella Artois" INTEGER,
    "Einstök White Ale" INTEGER,
    "Einstök Pale Ale" INTEGER,
    "Einstök Arctic Lager" INTEGER,
    Kaldi INTEGER,
    "Ölvisholt Lite" INTEGER,
    Eldgos INTEGER,
    Somersby INTEGER,
    Blanc INTEGER,
    Bríó INTEGER,
    Garún INTEGER,
    Helga INTEGER,
    Snorri INTEGER,
    Úlfrún INTEGER,
    Úlfur INTEGER,
    Guinness INTEGER,
    Bóndi INTEGER,
    "Heimabrugg/Annar IPA" INTEGER,
    "Mynd (url)" TEXT
);

-- Gögn frá "Bjor.csv" sett inn í töflu og aukadálk eytt
.mode csv
.import ".\\data\\Bjor.csv" Bjór
DELETE FROM Bjór WHERE Bar = 'Bar';

------------------------------------------------------------------------------------------------
-- 3

-- Tafla með bjórum úr Vínbúðinni
------------------------------------------------------------------------------------------------

-- Tafla búin til
DROP TABLE IF EXISTS Happy_Hour;
CREATE TABLE IF NOT EXISTS Happy_Hour (
    Bar TEXT,
    "Stærð (mL)" INTEGER,
    Byrjar TEXT,
    Endar TEXT,
    "Meðalverð (kr)" INTEGER,
    "Meðal Lítraverð (kr)" INTEGER,
    Gull INTEGER,
    "Gull Lite" INTEGER,
    "Tuborg Grön" INTEGER,
    "Tuborg Classic" INTEGER,
    "Víking Gylltur" INTEGER,
    "Víking Lite" INTEGER,
    "Víking Lite Classic" INTEGER,
    Thule INTEGER,
    Carlsberg INTEGER,
    Boli INTEGER,
    Peroni INTEGER,
    "Stella Artois" INTEGER,
    "Einstök White Ale" INTEGER,
    "Einstök Pale Ale" INTEGER,
    "Einstök Arctic Lager" INTEGER,
    Kaldi INTEGER,
    "Ölvisholt Lite" INTEGER,
    Eldgos INTEGER,
    Somersby INTEGER,
    Blanc INTEGER,
    Bríó INTEGER,
    Garún INTEGER,
    Helga INTEGER,
    Snorri INTEGER,
    Úlfrún INTEGER,
    Úlfur INTEGER,
    Guinness INTEGER,
    Bóndi INTEGER,
    "Heimabrugg/Annar IPA" INTEGER
);

-- Gögn frá "Happy_Hour.csv" sett inn í töflu og aukadálk eytt
.mode csv
.import ".\\data\\Happy_Hour.csv" Happy_Hour
DELETE FROM Happy_Hour WHERE Bar = 'Bar';

------------------------------------------------------------------------------------------------
-- 4

-- Tafla með gögnum úr Lukkuhjólum
------------------------------------------------------------------------------------------------

-- Tafla búin til
DROP TABLE IF EXISTS Lukkuhjól;
CREATE TABLE IF NOT EXISTS Lukkuhjól (
    Bar TEXT,
    Verð INTEGER,
    "Bjór mL" INTEGER,
    "Win Rate" REAL,
    "Lose Rate" REAL,
    "Even Rate" REAL,
    "Win Something Rate" REAL,
    "Lose All Rate" REAL,
    "Stærsta Win (Kr)" INTEGER,
    "1" TEXT,
    "2" TEXT,
    "3" TEXT,
    "4" TEXT,
    "5" TEXT,
    "6" TEXT,
    "7" TEXT,
    "8" TEXT,
    "9" TEXT,
    "10" TEXT,
    "11" TEXT,
    "12" TEXT,
    "13" TEXT,
    "14" TEXT,
    "15" TEXT,
    "16" TEXT
);

-- Gögn frá "Lukkuhjol.csv" sett inn í töflu og aukadálk eytt
.mode csv
.import ".\\data\\Lukkuhjol.csv" Lukkuhjól
DELETE FROM Lukkuhjól WHERE Bar = 'Bar';
DROP TABLE IF EXISTS Bjórkort;

------------------------------------------------------------------------------------------------
-- 5

-- Tafla búin til fyrir kort á mælaborði
------------------------------------------------------------------------------------------------

-- Tafla búin til úr Bjór töflunni með unpivot uppsetningu
CREATE TABLE Bjórkort AS
SELECT * FROM (
    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)", 
        'Gull' AS Bjór,
        Gull AS Verð
    FROM Bjór WHERE Gull IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Gull Lite' AS Bjór,
        "Gull Lite" AS Verð
    FROM Bjór WHERE "Gull Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Tuborg Grön' AS Bjór,
        "Tuborg Grön" AS Verð
    FROM Bjór WHERE "Tuborg Grön" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Tuborg Classic' AS Bjór,
        "Tuborg Classic" AS Verð
    FROM Bjór WHERE "Tuborg Classic" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Víking Gylltur' AS Bjór,
        "Víking Gylltur" AS Verð
    FROM Bjór WHERE "Víking Gylltur" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Víking Lite' AS Bjór,
        "Víking Lite" AS Verð
    FROM Bjór WHERE "Víking Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Víking Lite Classic' AS Bjór,
        "Víking Lite Classic" AS Verð
    FROM Bjór WHERE "Víking Lite Classic" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Thule' AS Bjór,
        Thule AS Verð
    FROM Bjór WHERE Thule IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Carlsberg' AS Bjór,
        Carlsberg AS Verð
    FROM Bjór WHERE Carlsberg IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Boli' AS Bjór,
        Boli AS Verð
    FROM Bjór WHERE Boli IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Peroni' AS Bjór,
        Peroni AS Verð
    FROM Bjór WHERE Peroni IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Stella Artois' AS Bjór,
        "Stella Artois" AS Verð
    FROM Bjór WHERE "Stella Artois" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Einstök White Ale' AS Bjór,
        "Einstök White Ale" AS Verð
    FROM Bjór WHERE "Einstök White Ale" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Einstök Pale Ale' AS Bjór,
        "Einstök Pale Ale" AS Verð
    FROM Bjór WHERE "Einstök Pale Ale" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Einstök Arctic Lager' AS Bjór,
        "Einstök Arctic Lager" AS Verð
    FROM Bjór WHERE "Einstök Arctic Lager" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Kaldi' AS Bjór,
        Kaldi AS Verð
    FROM Bjór WHERE Kaldi IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Ölvisholt Lite' AS Bjór,
        "Ölvisholt Lite" AS Verð
    FROM Bjór WHERE "Ölvisholt Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Eldgos' AS Bjór,
        Eldgos AS Verð
    FROM Bjór WHERE Eldgos IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Somersby' AS Bjór,
        Somersby AS Verð
    FROM Bjór WHERE Somersby IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Blanc' AS Bjór,
        Blanc AS Verð
    FROM Bjór WHERE Blanc IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Bríó' AS Bjór,
        Bríó AS Verð
    FROM Bjór WHERE Bríó IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Garún' AS Bjór,
        Garún AS Verð
    FROM Bjór WHERE Garún IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Helga' AS Bjór,
        Helga AS Verð
    FROM Bjór WHERE Helga IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Snorri' AS Bjór,
        Snorri AS Verð
    FROM Bjór WHERE Snorri IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Úlfrún' AS Bjór,
        Úlfrún AS Verð
    FROM Bjór WHERE Úlfrún IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Úlfur' AS Bjór,
        Úlfur AS Verð
    FROM Bjór WHERE Úlfur IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Guinness' AS Bjór,
        Guinness AS Verð
    FROM Bjór WHERE Guinness IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Bóndi' AS Bjór,
        Bóndi AS Verð
    FROM Bjór WHERE Bóndi IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",
        'Heimabrugg/Annar IPA' AS Bjór,
        "Heimabrugg/Annar IPA" AS Verð
    FROM Bjór WHERE "Heimabrugg/Annar IPA" IS NOT NULL
) ORDER BY Bar, Bjór;

-- Aukalínum eytt
DELETE FROM Bjórkort WHERE Verð IS NULL OR trim(Verð) = '';
DELETE FROM Bjórkort WHERE Bar IS 'Bar' OR trim(Bar) = 'Bar';

------------------------------------------------------------------------------------------------
-- 6

-- Dálkum með meðalverðum bætt í Bjór Vínbúð töflu
------------------------------------------------------------------------------------------------

-- Dálk bætt við með meðalverðum á bjór í bænum
ALTER TABLE Bjór_Vínbúðin ADD COLUMN "Meðalverð í bæ (Kr)" INTEGER;
UPDATE Bjór_Vínbúðin
SET "Meðalverð í bæ (Kr)" = (
    SELECT CAST(ROUND(AVG(Verð)) AS INTEGER)
    FROM Bjórkort
    WHERE Bjórkort.Bjór = Bjór_Vínbúðin.Bjór
);

-- Dálk bætt við með meðal lítraverðum á bjórum í bænum
ALTER TABLE Bjór_Vínbúðin ADD COLUMN "Meðal lítraverð í bæ (Kr)" INTEGER;
UPDATE Bjór_Vínbúðin
SET "Meðal lítraverð í bæ (Kr)" = (
    SELECT CAST(ROUND("Meðalverð í bæ (Kr)" / (AVG("Stærð (mL)") / 1000)) AS INTEGER)
    FROM Bjórkort
    WHERE Bjórkort.Bjór = Bjór_Vínbúðin.Bjór
);

-- Dálk bætt við með meðal lítraverðum á bjórum í vínbúðinni
ALTER TABLE Bjór_Vínbúðin ADD COLUMN "Lítraverð (Kr)" INTEGER;
UPDATE Bjór_Vínbúðin
SET "Lítraverð (Kr)" = ("Verð (Kr)" / ("Stærð (mL)" / 1000.0))
WHERE "Stærð (mL)" IS NOT NULL AND "Stærð (mL)" > 0;