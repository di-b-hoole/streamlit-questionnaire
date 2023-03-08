USE ROLE SYSADMIN;

CREATE DATABASE POWER_HOUR;

CREATE OR REPLACE TABLE PUBLIC.FAV_PET 
    (
      ID INTEGER NOT NULL AUTOINCREMENT
    , PET STRING
);

SELECT * FROM FAV_PET;

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