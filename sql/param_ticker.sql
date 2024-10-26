CREATE TABLE pda."2024_felipe_miguel_reto_schema".param_ticker (
    id_ticker   VARCHAR(10) NOT NULL,
    description VARCHAR(255),
    industry    VARCHAR(100),
    PRIMARY KEY (id_ticker)
);

INSERT INTO pda."2024_felipe_miguel_reto_schema".param_ticker (id_ticker, description, industry) VALUES
    ('BBAR.BA', 'Banco BBVA Argentina S.A.',       'Financial Services'),
    ('CEPU.BA', 'Central Puerto S.A.',             'Energy'),
    ('AAPL.BA', 'Apple Inc.',                      'Technology'),
    ('TGNO4.BA', 'Transportadora de Gas del Norte S.A.', 'Energy'),
    ('PAMP.BA', 'Pampa Energía S.A.',              'Energy'),
    ('AMZN.BA', 'Amazon.com Inc.',                 'Technology');
