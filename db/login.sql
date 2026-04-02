-- SQL*Plus Session Formatting Script
-- This file is automatically loaded by SQL*Plus because it is named 'login.sql' 
-- and its location is included in the ORACLE_PATH environment variable.
-- It handles console output formatting (column widths, page sizes, etc.) 
-- for the 'customers' and 'payments' tables.

SET LINESIZE 150
SET PAGESIZE 50
COLUMN ID FORMAT 9999
COLUMN CUSTOMER_ID FORMAT 9999
COLUMN NAME FORMAT A25
COLUMN EMAIL FORMAT A35
COLUMN PHONE FORMAT A15
COLUMN CARD_NUMBER FORMAT A20
COLUMN AMOUNT FORMAT 9999.99
