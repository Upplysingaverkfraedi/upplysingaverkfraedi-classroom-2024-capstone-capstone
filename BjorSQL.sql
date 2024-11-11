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

-- Update names in Bjór_Vínbúðin to match those in Bjórkort
UPDATE Bjór_Vínbúðin SET Nafn = 'Gull' WHERE Nafn = 'Egils Gull';
UPDATE Bjór_Vínbúðin SET Nafn = 'Boli' WHERE Nafn = 'Boli Premium';
UPDATE Bjór_Vínbúðin SET Nafn = 'Peroni' WHERE Nafn = 'Peroni Nastro Azzurro';
UPDATE Bjór_Vínbúðin SET Nafn = 'Einstök Pale Ale' WHERE Nafn = 'Einstök Arctic Pale Ale';
UPDATE Bjór_Vínbúðin SET Nafn = 'Eldgos' WHERE Nafn = 'Eldgos Flamingo Kokteill';
UPDATE Bjór_Vínbúðin SET Nafn = 'Somersby' WHERE Nafn = 'Somersby Apple';
UPDATE Bjór_Vínbúðin SET Nafn = 'Blanc' WHERE Nafn = 'Kronenbourg 1664 Blanc';
UPDATE Bjór_Vínbúðin SET Nafn = 'Bríó' WHERE Nafn = 'Bríó nr. 1 Pilsner';
UPDATE Bjór_Vínbúðin SET Nafn = 'Garún' WHERE Nafn = 'Garún nr. 19 Icelandic Stout';
UPDATE Bjór_Vínbúðin SET Nafn = 'Helga' WHERE Nafn = 'Helga nr. 69 Raspberry Sour';
UPDATE Bjór_Vínbúðin SET Nafn = 'Snorri' WHERE Nafn = 'Snorri nr. 10 íslenskt öl';
UPDATE Bjór_Vínbúðin SET Nafn = 'Úlfrún' WHERE Nafn = 'Úlfrún nr. 34';
UPDATE Bjór_Vínbúðin SET Nafn = 'Úlfur' WHERE Nafn = 'Úlfur nr. 3 India Pale Ale';
UPDATE Bjór_Vínbúðin SET Nafn = 'Guinness' WHERE Nafn = 'Guinness Draught';
UPDATE Bjór_Vínbúðin SET Nafn = 'Bóndi' WHERE Nafn = 'Bóndi Session IPA';

-- Drop the table if it already exists
DROP TABLE IF EXISTS Bjór;

-- Create the Bjór table with the new "Mynd (url)" column
CREATE TABLE IF NOT EXISTS Bjór (
    Bar TEXT,
    "Stærð (mL)" INTEGER,
    Latitude REAL,
    Longitude REAL,
    "Mynd (url)" TEXT, -- New column for image URLs
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

-- Insert data from "Bjór.csv" including the new "Mynd (url)" column
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

-- Drop the table if it already exists
DROP TABLE IF EXISTS Bjórkort;

-- Create the Bjórkort table with unpivoted data for visualization, including the Mynd (url) column
CREATE TABLE Bjórkort AS
SELECT * FROM (
    SELECT 
        Bar,
        "Stærð (mL)",
        Latitude,
        Longitude,
        "Mynd (url)",  -- Include the image URL column
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

-- Clean up rows with invalid data
DELETE FROM Bjórkort WHERE Verð IS NULL OR trim(Verð) = '';
DELETE FROM Bjórkort WHERE Bar IS 'Bar' OR trim(Bar) = 'Bar';


-- Add the column for average price if it doesn't exist (in case the table was created before)
ALTER TABLE Bjór_Vínbúðin ADD COLUMN "Average Price (Kr)" REAL;

-- Step 1: Calculate and update the average prices for each beer type in Bjór_Vínbúðin based on data from Bjórkort
UPDATE Bjór_Vínbúðin
SET "Average Price (Kr)" = (
    SELECT AVG(Verð)
    FROM Bjórkort
    WHERE Bjórkort.Bjór = Bjór_Vínbúðin.Nafn
);