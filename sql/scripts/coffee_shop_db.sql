-- Tabellen erstellen:
CREATE TABLE backstock 
(
	id SERIAL PRIMARY KEY,
	name VARCHAR(255) NOT NULL,
	in_stock INT NOT NULL				
);

CREATE TABLE latte 
(
	id SERIAL PRIMARY KEY,
	price NUMERIC(10,2) NOT NULL,
	order_date TIMESTAMPTZ NOT NULL				
);

CREATE TABLE americano 
(
	id SERIAL PRIMARY KEY,
	price NUMERIC(10,2) NOT NULL,
	order_date TIMESTAMPTZ NOT NULL				
);

CREATE TABLE lemonade 
(
	id SERIAL PRIMARY KEY,
	price NUMERIC(10,2) NOT NULL,
	order_date TIMESTAMPTZ NOT NULL				
);

CREATE TABLE apple_spritzer 
(
	id SERIAL PRIMARY KEY,
	price NUMERIC(10,2) NOT NULL,
	order_date TIMESTAMPTZ NOT NULL				
);

CREATE TABLE logs
(
	id SERIAL PRIMARY KEY,
	table_name VARCHAR(255) NOT NULL,
	item_id INT NOT NULL,
	operation VARCHAR(255) NOT NULL,
	old_data JSONB,
	new_data JSONB,
	timestamp TIMESTAMPTZ NOT NULL DEFAULT now()
);

-- trigger function:
CREATE OR REPLACE
FUNCTION log_ops_with_data() RETURNS TRIGGER AS $$
BEGIN
    INSERT INTO logs
    (
	    table_name,
		item_id,
	    operation,
	    old_data,
	    new_data
    )
    VALUES 
    (
        TG_TABLE_NAME,
		CASE
            WHEN TG_OP IN ('INSERT', 'UPDATE') THEN NEW.id
            WHEN TG_OP = 'DELETE' THEN OLD.id
        END,
        TG_OP,
	    CASE
			WHEN TG_OP IN ('UPDATE', 'DELETE') THEN to_jsonb(OLD)
			ELSE NULL
	    END,
	    CASE
			WHEN TG_OP IN ('UPDATE', 'INSERT') THEN to_jsonb(NEW)
			ELSE NULL
	    END
    );

RETURN NEW;
END;

$$ LANGUAGE plpgsql;

-- trigger auf tabellen setzen:
CREATE TRIGGER logs_on_backstock
AFTER INSERT OR UPDATE OR DELETE ON backstock
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_latte
AFTER INSERT OR UPDATE OR DELETE ON latte
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_americano
AFTER INSERT OR UPDATE OR DELETE ON americano
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_lemonade
AFTER INSERT OR UPDATE OR DELETE ON lemonade
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

CREATE TRIGGER logs_on_apple_spritzer
AFTER INSERT OR UPDATE OR DELETE ON apple_spritzer
FOR EACH ROW
EXECUTE FUNCTION log_ops_with_data();

-- Load CSV data
COPY backstock(id, name, in_stock)
FROM '/docker-entrypoint-initdb.d/data/coffee_shop/backstock.csv'
DELIMITER ','
CSV HEADER;

COPY latte(id, price, order_date)
FROM '/docker-entrypoint-initdb.d/data/coffee_shop/latte.csv'
DELIMITER ','
CSV HEADER;

COPY americano(id, price, order_date)
FROM '/docker-entrypoint-initdb.d/data/coffee_shop/americano.csv'
DELIMITER ','
CSV HEADER;

COPY lemonade(id, price, order_date)
FROM '/docker-entrypoint-initdb.d/data/coffee_shop/lemonade.csv'
DELIMITER ','
CSV HEADER;

COPY apple_spritzer(id, price, order_date)
FROM '/docker-entrypoint-initdb.d/data/coffee_shop/apple_spritzer.csv'
DELIMITER ','
CSV HEADER;


-- sequences setzen nach den eintragen der testdaten
SELECT setval(pg_get_serial_sequence('backstock', 'id'), (SELECT MAX(id) FROM backstock));
SELECT setval(pg_get_serial_sequence('latte', 'id'), (SELECT MAX(id) FROM latte));
SELECT setval(pg_get_serial_sequence('americano', 'id'), (SELECT MAX(id) FROM americano));
SELECT setval(pg_get_serial_sequence('lemonade', 'id'), (SELECT MAX(id) FROM lemonade));
SELECT setval(pg_get_serial_sequence('apple_spritzer', 'id'), (SELECT MAX(id) FROM apple_spritzer));