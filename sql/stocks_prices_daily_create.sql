CREATE TABLE pda."2024_felipe_miguel_reto_schema".stocks_prices_daily (
    Date TIMESTAMP,            -- Para manejar fechas con precisión
    Ticker VARCHAR(255),       -- Los tickers suelen ser cadenas de texto, tipo VARCHAR
    Adj_Close FLOAT8,          -- Los precios ajustados como número decimal
    Close FLOAT8,              -- El precio de cierre también como decimal
    High FLOAT8,               -- El precio más alto del día como decimal
    Low FLOAT8,                -- El precio más bajo del día como decimal
    "Open" FLOAT8,               -- El precio de apertura como decimal
    Volume BIGINT              -- El volumen suele ser un número entero grande
);