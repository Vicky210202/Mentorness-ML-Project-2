-- Creating database 'mentorness' in PostgrSQL
CREATE DATABASE mentorness;

-- Creating table 'fastag' in PostgreSQL 
DROP TABLE fastag;
CREATE TABLE fastag (
    id SERIAL PRIMARY KEY,
    vehicle_type TEXT,
    vehicle_plate_number TEXT,
    amount_frauded NUMERIC,
    fraud_indicator TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

