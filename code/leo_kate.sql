-- Eyða ef taflan er nú þegar til
DROP TABLE IF EXISTS rotten_tomatoes_movies_dicaprio_winslet;

-- Búa til nýju töfluna
CREATE TABLE IF NOT EXISTS rotten_tomatoes_movies_dicaprio_winslet AS
SELECT * 
FROM rotten_tomatoes_movies
WHERE actors LIKE '%Leonardo DiCaprio%' 
   OR actors LIKE '%Kate Winslet%';

-- Sýna fjölda mynda þar sem Leonardo DiCaprio eða Kate Winslet eru nefnd
SELECT COUNT(*) FROM rotten_tomatoes_movies_dicaprio_winslet;

-- Búa til nýja gagnagrunnsskrá
ATTACH DATABASE 'leo_kate_movies.db' AS leo_kate;

-- Búa til töflu í nýja gagnagrunninum með þeim myndum sem þú vilt
CREATE TABLE leo_kate.movies AS
SELECT * 
FROM rotten_tomatoes_movies
WHERE actors LIKE '%Leonardo DiCaprio%' 
   OR actors LIKE '%Kate Winslet%';

-- Losa við tengingu
DETACH DATABASE leo_kate;