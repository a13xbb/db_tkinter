
BEGIN
-- проверка на существование БД с таким же именем
IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   -- Возвращаем сообщение (не ошибку)
   RAISE NOTICE 'Database already exists';
ELSE
   -- выполняем SQL запрос на создание БД. оператор || - конкатенация
   -- current_database() - возврашает название БД в которой сейчас выполняется транзакция
   -- принцип работы dblink_exec: подключается к указанной бд(в примере - текущая), и выполняет запрос,
   -- переданный вторым аргументом.
   -- для доп.информации можно добавить hostaddr=127.0.0.1 port=5432 dbname=mydb user=postgres password=mypasswd
   	PERFORM dblink_exec('dbname=' || current_database() || ' user=postgres' || ' password=1989'   -- current db
                     , 'CREATE DATABASE ' || quote_ident(dbname));

	PERFORM dblink_connect('dbname=user_db user=postgres password=1989');

	PERFORM dblink_exec(
         'CREATE TABLE item (
			id serial PRIMARY KEY,
			name text UNIQUE NOT NULL,
			weight numeric(10),
			quantity integer CHECK (quantity>=0),
			price numeric(10) NOT NULL);');

	PERFORM dblink_exec(
         'CREATE TABLE transaction (
			current_balance numeric(10),
			cost numeric(10) CHECK(cost>0),
			counteragent_name text NOT NULL);');

	PERFORM dblink_exec(
         'CREATE TABLE purchase (
			id serial PRIMARY KEY,
			buyer_name text NOT NULL,
			weight numeric(10) CHECK (weight>=0),
			price numeric(10) CHECK (price>0),
			status text);');

	PERFORM dblink_exec(
         'CREATE TABLE purchase_item (
			purchase_id integer,
			item_name text REFERENCES item(name),
            quantity integer CHECK (quantity>0));');

	PERFORM dblink_exec(
         'CREATE TABLE users (
			user_id serial PRIMARY KEY,
			username text UNIQUE NOT NULL,
			role text NOT NULL);');

	PERFORM dblink_exec(
         'CREATE ROLE admin WITH LOGIN PASSWORD ''admin'' SUPERUSER;
		  CREATE ROLE accountant;
		  CREATE ROLE merchandiser;');

	PERFORM dblink_exec(
		'GRANT USAGE ON SCHEMA public TO merchandiser;
		 GRANT USAGE ON SCHEMA public TO accountant;
		 GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO merchandiser;
		 GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO accountant;
		 GRANT ALL PRIVILEGES ON TABLE item TO merchandiser;
		 GRANT ALL PRIVILEGES ON TABLE purchase TO merchandiser;
		 GRANT ALL PRIVILEGES ON TABLE purchase_item TO merchandiser;
		 GRANT ALL PRIVILEGES ON TABLE transaction TO accountant;');

-- 	PERFORM dblink_exec(
--          'EXECUTE ''GRANT INSERT ON users TO admin;''');

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION create_user(username text, password text, role text)
  			RETURNS void AS
		$func$
		BEGIN

		EXECUTE ''CREATE USER '' || username || '' WITH ROLE '' || role || '' LOGIN PASSWORD '' || password;

		END
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION is_in_items(my_item text, my_quantity integer)
  			RETURNS SETOF boolean AS
		$func$
		BEGIN

			RETURN QUERY
			EXECUTE ''SELECT EXISTS (SELECT 1 FROM item WHERE name='' || my_item || '' AND quantity>='' || my_quantity ||  '')'';

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION get_price(my_item text)
  			RETURNS SETOF numeric(10) AS
		$func$
		BEGIN

			RETURN QUERY
			EXECUTE ''SELECT price FROM item WHERE name='' || my_item;

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION get_weight(my_item text)
  			RETURNS SETOF numeric(10) AS
		$func$
		BEGIN

			RETURN QUERY
			EXECUTE ''SELECT weight FROM item WHERE name='' || my_item;

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION create_order(my_buyer_name text, my_weight numeric(10), my_price numeric(10), status text)
  			RETURNS void AS
		$func$
		BEGIN

			EXECUTE ''INSERT INTO purchase(buyer_name, weight, price, status) VALUES('' || my_buyer_name || '', '' || my_weight || '', '' || my_price || '', '' || status || '')'';

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION take_from_storage(item_name text, my_quantity integer)
  			RETURNS void AS
		$func$
		BEGIN

			EXECUTE ''UPDATE item
					  SET quantity=quantity-'' || my_quantity || '' WHERE name='' || item_name;

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION get_last_order_id()
  			RETURNS SETOF bigint AS
		$func$
		BEGIN

			RETURN QUERY
			EXECUTE ''SELECT count(*) FROM purchase'';

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION add_item_to_order(order_id integer, item_name text, my_quantity integer)
  			RETURNS void AS
		$func$
		BEGIN

			EXECUTE ''INSERT INTO purchase_item(purchase_id, item_name, quantity) VALUES('' || order_id || '', '' || item_name || '', '' || my_quantity || '')'';

		END;
		$func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION search_purchase_by_name(name text)
  		 RETURNS TABLE(id integer,
						buyer_name text,
						weight numeric(10),
						price numeric(10),
						status text)
  		 AS
		 $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT p.id, p.buyer_name, p.weight, p.price, p.status FROM purchase AS p WHERE p.buyer_name=name;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION search_purchase_by_id(my_id integer)
  		 RETURNS TABLE(id integer,
						buyer_name text,
						weight numeric(10),
						price numeric(10),
						status text)
  		 AS
		 $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT p.id, p.buyer_name, p.weight, p.price, p.status FROM purchase AS p WHERE p.id=my_id;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);


	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION search_purchase_by_weight(my_weight numeric(10))
  		 RETURNS TABLE(id integer,
						buyer_name text,
						weight numeric(10),
						price numeric(10),
						status text)
  		 AS
		 $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT p.id, p.buyer_name, p.weight, p.price, p.status FROM purchase AS p WHERE p.weight>=my_weight;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION search_purchase_by_price(my_price numeric(10))
  		 RETURNS TABLE(id integer,
						buyer_name text,
						weight numeric(10),
						price numeric(10),
						status text)
  		 AS
		 $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT p.id, p.buyer_name, p.weight, p.price, p.status FROM purchase AS p WHERE p.price>=my_price;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION search_purchase_by_status(my_status text)
  		 RETURNS TABLE(id integer,
						buyer_name text,
						weight numeric(10),
						price numeric(10),
						status text)
  		 AS
		 $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT p.id, p.buyer_name, p.weight, p.price, p.status FROM purchase AS p WHERE p.status=my_status;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);

	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION get_purchase_items(my_id integer) RETURNS
		 TABLE (purchase_id integer,
				item_name text,
            	quantity integer)
		 AS $func$
		 BEGIN

		    RETURN QUERY
		 	SELECT pi.purchase_id, pi.item_name, pi.quantity FROM purchase_item AS pi WHERE pi.purchase_id=my_id;

		 END;
		 $func$ LANGUAGE plpgsql;'
	);

END IF;

END
