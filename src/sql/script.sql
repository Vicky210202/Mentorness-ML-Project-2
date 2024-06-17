-- Creating database 'mentorness' in PostgrSQL
CREATE DATABASE mentorness;

-- Creating table 'fastag' in PostgreSQL 
DROP TABLE fastag;
CREATE TABLE fastag (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    vehicle_type TEXT NOT NULL,
    vehicle_plate_number TEXT NOT NULL,
    amount_frauded NUMERIC NOT NULL,
    fraud_indicator TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

