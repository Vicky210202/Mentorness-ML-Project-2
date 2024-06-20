
-- Creating table 'fastag' in cloud PostgreSQL instance  
DROP TABLE IF EXISTS fastag;
CREATE TABLE fastag (
    id BIGSERIAL NOT NULL PRIMARY KEY,
    vehicle_type TEXT NOT NULL,
    vehicle_plate_number TEXT NOT NULL,
    amount_frauded NUMERIC NOT NULL,
    fraud_indicator TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP 
);

-- After entering some unknown data to classify whether the transaction either fraud or legit,
-- The ML app will record the details of the transaction given by the users
-- To view
SELECT * FROM fastag;
