-- Open or create the Bjórgrunnur.db database
.open Bjórgrunnur.db

-- 1. Create table for "Bjór Vínbúðin.csv"
DROP TABLE IF EXISTS Bjór_Vínbúðin;
CREATE TABLE IF NOT EXISTS Bjór_Vínbúðin (
    Nafn TEXT,
    "Verð (Kr)" INTEGER,
    ml INTEGER
);

-- Insert data from "Bjór Vínbúðin.csv"
.mode csv
.import ".\\data\\Bjor_Vinbudin.csv" Bjór_Vínbúðin

-- 2. Býr til töflu fyrir "Bjór.csv"
DROP TABLE IF EXISTS Bjór;
CREATE TABLE IF NOT EXISTS Bjór (
    Bar TEXT,
    "Stærð (mL)" INTEGER,
    Latitude REAL,
    Longitude REAL,
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

-- Insert data from "Bjór.csv"
.mode csv
.import ".\\data\\Bjor.csv" Bjór

-- 3. Create table for "Happy Hour.csv"
DROP TABLE IF EXISTS Happy_Hour;
CREATE TABLE IF NOT EXISTS Happy_Hour (
    Bar TEXT,
    "Stærð (mL)" INTEGER,
    Byrjar TEXT,
    Endar TEXT,
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

-- Insert data from "Happy Hour.csv"
.mode csv
.import ".\\data\\Happy_Hour.csv" Happy_Hour

-- 4. Create table for "Lukkuhjól.csv"
DROP TABLE IF EXISTS Lukkuhjól;
CREATE TABLE IF NOT EXISTS Lukkuhjól (
    Bar TEXT,
    Verð INTEGER,
    "Bjór mL" INTEGER,
    "Win Rate" REAL,
    "Lose Rate" REAL,
    "Even Rate" REAL,
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

-- Insert data from "Lukkuhjól.csv"
.mode csv
.import ".\\data\\Lukkuhjol.csv" Lukkuhjól

-- Create the Bjorkort table with unpivoted data for visualization
DROP TABLE IF EXISTS Bjórkort;
CREATE TABLE Bjórkort AS
SELECT * FROM (
    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Gull' AS Bjór,
        Gull AS Verð
    FROM Bjór WHERE Gull IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Gull Lite' AS Bjór,
        "Gull Lite" AS Verð
    FROM Bjór WHERE "Gull Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Tuborg Grön' AS Bjór,
        "Tuborg Grön" AS Verð
    FROM Bjór WHERE "Tuborg Grön" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Tuborg Classic' AS Bjór,
        "Tuborg Classic" AS Verð
    FROM Bjór WHERE "Tuborg Classic" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Víking Gylltur' AS Bjór,
        "Víking Gylltur" AS Verð
    FROM Bjór WHERE "Víking Gylltur" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Víking Lite' AS Bjór,
        "Víking Lite" AS Verð
    FROM Bjór WHERE "Víking Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Víking Lite Classic' AS Bjór,
        "Víking Lite Classic" AS Verð
    FROM Bjór WHERE "Víking Lite Classic" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Thule' AS Bjór,
        Thule AS Verð
    FROM Bjór WHERE Thule IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Carlsberg' AS Bjór,
        Carlsberg AS Verð
    FROM Bjór WHERE Carlsberg IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Boli' AS Bjór,
        Boli AS Verð
    FROM Bjór WHERE Boli IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Peroni' AS Bjór,
        Peroni AS Verð
    FROM Bjór WHERE Peroni IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Stella Artois' AS Bjór,
        "Stella Artois" AS Verð
    FROM Bjór WHERE "Stella Artois" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Einstök White Ale' AS Bjór,
        "Einstök White Ale" AS Verð
    FROM Bjór WHERE "Einstök White Ale" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Einstök Pale Ale' AS Bjór,
        "Einstök Pale Ale" AS Verð
    FROM Bjór WHERE "Einstök Pale Ale" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Einstök Arctic Lager' AS Bjór,
        "Einstök Arctic Lager" AS Verð
    FROM Bjór WHERE "Einstök Arctic Lager" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Kaldi' AS Bjór,
        Kaldi AS Verð
    FROM Bjór WHERE Kaldi IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Ölvisholt Lite' AS Bjór,
        "Ölvisholt Lite" AS Verð
    FROM Bjór WHERE "Ölvisholt Lite" IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Eldgos' AS Bjór,
        Eldgos AS Verð
    FROM Bjór WHERE Eldgos IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Somersby' AS Bjór,
        Somersby AS Verð
    FROM Bjór WHERE Somersby IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Blanc' AS Bjór,
        Blanc AS Verð
    FROM Bjór WHERE Blanc IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Bríó' AS Bjór,
        Bríó AS Verð
    FROM Bjór WHERE Bríó IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Garún' AS Bjór,
        Garún AS Verð
    FROM Bjór WHERE Garún IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Helga' AS Bjór,
        Helga AS Verð
    FROM Bjór WHERE Helga IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Snorri' AS Bjór,
        Snorri AS Verð
    FROM Bjór WHERE Snorri IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Úlfrún' AS Bjór,
        Úlfrún AS Verð
    FROM Bjór WHERE Úlfrún IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Úlfur' AS Bjór,
        Úlfur AS Verð
    FROM Bjór WHERE Úlfur IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Guinness' AS Bjór,
        Guinness AS Verð
    FROM Bjór WHERE Guinness IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Bóndi' AS Bjór,
        Bóndi AS Verð
    FROM Bjór WHERE Bóndi IS NOT NULL

    UNION ALL

    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        'Heimabrugg/Annar IPA' AS Bjór,
        "Heimabrugg/Annar IPA" AS Verð
    FROM Bjór WHERE "Heimabrugg/Annar IPA" IS NOT NULL
) ORDER BY Bar, Bjór;

DELETE FROM Bjórkort WHERE Verð IS NULL OR trim(Verð) = '';
DELETE FROM Bjórkort WHERE Bar IS 'Bar' OR trim(Bar) = 'Bar';

-- Add the column for average price if it doesn't exist (in case the table was created before)
ALTER TABLE Bjór_Vínbúðin ADD COLUMN "Average Price (Kr)" REAL;

-- 2. Update the new column with the average price of each beer from the Bjór table
UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Gull")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Egils Gull' AND "Gull" IS NOT NULL
)
WHERE Nafn = 'Egils Gull';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Gull Lite")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Gull Lite' AND "Gull Lite" IS NOT NULL
)
WHERE Nafn = 'Gull Lite';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Tuborg Grön")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Tuborg Grön' AND "Tuborg Grön" IS NOT NULL
)
WHERE Nafn = 'Tuborg Grön';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Tuborg Classic")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Tuborg Classic' AND "Tuborg Classic" IS NOT NULL
)
WHERE Nafn = 'Tuborg Classic';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Víking Gylltur")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Víking Gylltur' AND "Víking Gylltur" IS NOT NULL
)
WHERE Nafn = 'Víking Gylltur';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Víking Lite")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Víking Lite' AND "Víking Lite" IS NOT NULL
)
WHERE Nafn = 'Víking Lite';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Víking Lite Classic")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Víking Lite Classic' AND "Víking Lite Classic" IS NOT NULL
)
WHERE Nafn = 'Víking Lite Classic';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Thule")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Thule' AND Thule IS NOT NULL
)
WHERE Nafn = 'Thule';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Carlsberg")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Carlsberg' AND Carlsberg IS NOT NULL
)
WHERE Nafn = 'Carlsberg';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Boli")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Boli Premium' AND Boli IS NOT NULL
)
WHERE Nafn = 'Boli Premium';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Peroni")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Peroni Nastro Azzurro' AND Peroni IS NOT NULL
)
WHERE Nafn = 'Peroni Nastro Azzurro';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Stella Artois")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Stella Artois' AND "Stella Artois" IS NOT NULL
)
WHERE Nafn = 'Stella Artois';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Einstök White Ale")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Einstök White Ale' AND "Einstök White Ale" IS NOT NULL
)
WHERE Nafn = 'Einstök White Ale';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Einstök Pale Ale")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Einstök Arctic Pale Ale' AND "Einstök Pale Ale" IS NOT NULL
)
WHERE Nafn = 'Einstök Arctic Pale Ale';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Kaldi")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Kaldi' AND Kaldi IS NOT NULL
)
WHERE Nafn = 'Kaldi';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Ölvisholt Lite")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Ölvisholt Lite' AND "Ölvisholt Lite" IS NOT NULL
)
WHERE Nafn = 'Ölvisholt Lite';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Eldgos")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Eldgos Flamingo Kokteill' AND "Eldgos" IS NOT NULL
)
WHERE Nafn = 'Eldgos Flamingo Kokteill';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Somersby")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Somersby Apple' AND Somersby IS NOT NULL
)
WHERE Nafn = 'Somersby Apple';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Blanc")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Kronenbourg 1664 Blanc' AND "Blanc" IS NOT NULL
)
WHERE Nafn = 'Kronenbourg 1664 Blanc';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Bríó")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Bríó nr. 1 Pilsner' AND "Bríó" IS NOT NULL
)
WHERE Nafn = 'Bríó nr. 1 Pilsner';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Garún")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Garún nr. 19 Icelandic Stout' AND "Garún" IS NOT NULL
)
WHERE Nafn = 'Garún nr. 19 Icelandic Stout';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Helga")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Helga nr. 69 Raspberry Sour' AND "Helga" IS NOT NULL
)
WHERE Nafn = 'Helga nr. 69 Raspberry Sour';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Snorri")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Snorri nr. 10 íslenskt öl' AND "Snorri" IS NOT NULL
)
WHERE Nafn = 'Snorri nr. 10 íslenskt öl';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Úlfrún")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Úlfrún nr. 34' AND "Úlfrún" IS NOT NULL
)
WHERE Nafn = 'Úlfrún nr. 34';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Úlfur")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Úlfur nr. 3 India Pale Ale' AND "Úlfur" IS NOT NULL
)
WHERE Nafn = 'Úlfur nr. 3 India Pale Ale';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Guinness")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Guinness Draught' AND "Guinness" IS NOT NULL
)
WHERE Nafn = 'Guinness Draught';

UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG("Bóndi")
    FROM Bjór
    WHERE Bjór_Vínbúðin.Nafn = 'Bóndi Session IPA' AND "Bóndi" IS NOT NULL
)
WHERE Nafn = 'Bóndi Session IPA';