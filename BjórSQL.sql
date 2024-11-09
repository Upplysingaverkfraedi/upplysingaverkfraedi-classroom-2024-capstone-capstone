-- Open or create the Bjórgrunnur.db database
.open Bjórgrunnur.db

-- 1. Create table for "Bjór Vínbúðin.csv"
CREATE TABLE IF NOT EXISTS Bjór_Vínbúðin (
    Nafn TEXT,
    "Verð (Kr)" INTEGER,
    ml INTEGER
);

-- Insert data from "Bjór Vínbúðin.csv"
.mode csv
.import "C:\\Users\\valur\\Downloads\\Drasl\\Bjór Vínbúðin.csv" Bjór_Vínbúðin

-- 2. Býr til töflu fyrir "Bjór.csv"
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
.import "C:\\Users\\valur\\Downloads\\Drasl\\Bjór.csv" Bjór

-- 3. Create table for "Happy Hour.csv"
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
.import "C:\\Users\\valur\\Downloads\\Drasl\\Happy Hour.csv" Happy_Hour

-- 4. Create table for "Lukkuhjól.csv"
CREATE TABLE IF NOT EXISTS Lukkuhjol (
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
.import "C:\\Users\\valur\\Downloads\\Drasl\\Lukkuhjól.csv" Lukkuhjol

-- Drop the table if it already exists
DROP TABLE IF EXISTS Bjórkort;

-- Create the Bjorkort table with unpivoted data for visualization
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