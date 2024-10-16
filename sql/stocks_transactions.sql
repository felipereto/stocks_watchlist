CREATE TABLE pda."2024_felipe_miguel_reto_schema".stocks_transactions (
    ticker VARCHAR(10),
    type VARCHAR(10),
    date DATE,
    nominal_quantity INT,
    face_value INT,
    gross_cost INT
);

INSERT INTO pda."2024_felipe_miguel_reto_schema".stocks_transactions (ticker, type, date, nominal_quantity, face_value, gross_cost) VALUES
('BBAR.BA', 'buy', '2024-10-10', 15, 4621, 69315),
('CEPU.BA', 'buy', '2024-10-08', 30, 1190, 35700),
('AAPL.BA', 'buy', '2024-09-12', 50, 13980, 699000),
('TGNO4.BA', 'buy', '2024-09-17', 60, 3243, 194580),
('PAMP.BA', 'buy', '2024-09-10', 500, 2858, 1429000),
('AMZN.BA', 'buy', '2024-09-13', 20, 1616, 32320);
