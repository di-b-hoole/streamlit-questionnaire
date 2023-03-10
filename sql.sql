USE ROLE SYSADMIN;

CREATE DATABASE POWER_HOUR;

CREATE OR REPLACE TABLE PUBLIC.FAV_PET 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , NAME STRING 
    , PET STRING
);

SELECT * FROM FAV_PET;
SELECT PET , COUNT(1) AS NO_OF_PICKS FROM FAV_PET GROUP BY PET ORDER BY COUNT(1) DESC;

CREATE OR REPLACE TABLE PUBLIC.ANSWERS 
    (
         ID INTEGER NOT NULL AUTOINCREMENT
        ,NAME STRING
        ,AGE INT
        ,NO_DOGS INT
        ,NO_CATS INT
        ,NO_BIRDS INT
        ,NO_FISH INT
        ,NO_REPTILES INT
        ,GENDER STRING
    );

SELECT * FROM ANSWERS;


SELECT DISTINCT BIRTH_YEAR FROM TRANSFORMED_HIST ORDER BY 1;


select *
from POWER_HOUR.PUBLIC.TRANSFORMED_HIST
where DWELLING_TYPE not like 'nan' and GENDER not like 'nan' and LIVING_AREA not like 'nan';

CREATE OR REPLACE TABLE PUBLIC.DWELLING_TYPE 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , DWELLING_TYPE STRING
);


INSERT INTO DWELLING_TYPE (DWELLING_TYPE) 
SELECT DISTINCT DWELLING_TYPE
from POWER_HOUR.PUBLIC.TRANSFORMED_HIST
where DWELLING_TYPE not like 'nan' ;


CREATE OR REPLACE TABLE PUBLIC.DWELLING_TYPE 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , DWELLING_TYPE STRING
);


INSERT INTO DWELLING_TYPE (DWELLING_TYPE) 
SELECT DISTINCT DWELLING_TYPE
from POWER_HOUR.PUBLIC.TRANSFORMED_HIST
where DWELLING_TYPE not like 'nan' ;

CREATE OR REPLACE TABLE PUBLIC.GENDER 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , GENDER STRING
);


INSERT INTO GENDER (GENDER) 
SELECT DISTINCT GENDER
from POWER_HOUR.PUBLIC.TRANSFORMED_HIST
where GENDER not like 'nan' ;


CREATE OR REPLACE TABLE PUBLIC.LIVING_AREA 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , LIVING_AREA STRING
);


INSERT INTO LIVING_AREA (LIVING_AREA) 
SELECT DISTINCT LIVING_AREA
from POWER_HOUR.PUBLIC.TRANSFORMED_HIST
where LIVING_AREA not like 'nan' ;


CREATE OR REPLACE TABLE TRANSFORMED_HIST_NEW AS
SELECT 
     UNIQUE_KEY
    ,IFF(CAT_IND='Cat',1,0)     AS CAT_IND
    ,IFF(DOG_IND='Cat',1,0)     AS DOG_IND
    ,IFF(FISH_IND='Cat',1,0)    AS FISH_IND
    ,IFF(BIRD_IND='Cat',1,0)    AS BIRD_IND
    ,IFF(REPTILE_IND='Cat',1,0) AS REPTILE_IND
    ,DOG_AMOUNT
    ,CAT_AMOUNT 
    ,FISH_AMOUNT
    ,BIRD_AMOUNT
    ,REPTILE_AMOUNT
    ,BIRTH_YEAR
    ,D.ID                       AS DWELLING_TYPE
    ,G.ID                       AS GENDER
    ,L.ID                       AS LIVING_AREA
FROM POWER_HOUR.PUBLIC.TRANSFORMED_HIST H
LEFT JOIN PUBLIC.DWELLING_TYPE D ON H.DWELLING_TYPE = D.DWELLING_TYPE
LEFT JOIN PUBLIC.GENDER G ON H.GENDER = G.GENDER
LEFT JOIN PUBLIC.LIVING_AREA L ON H.LIVING_AREA = L.LIVING_AREA;



SELECT G.ID, D.ID
FROM PUBLIC.GENDER AS G, PUBLIC.DWELLING_TYPE AS D
WHERE 
    GENDER = 'Male'
    OR DWELLING_TYPE = 'House';