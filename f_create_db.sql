CREATE EXTENSION dblink;


CREATE OR REPLACE FUNCTION f_create_db(dbname text)
  RETURNS integer AS
$func$
BEGIN

IF EXISTS (SELECT 1 FROM pg_database WHERE datname = dbname) THEN
   RAISE NOTICE 'Database already exists'; 
ELSE
   

PERFORM dblink_exec('dbname=' || current_database() || ' user=postgres' || ' password=1989'   -- current db
                     , 'CREATE DATABASE ' || quote_ident(dbname));
					 
	PERFORM dblink_connect('dbname=user_db user=postgres password=1989');
	
	PERFORM dblink_exec(
         'CREATE TABLE item (
			id numeric(6) PRIMARY KEY,
			name text NOT NULL,
			weight numeric(10),
			price numeric(10) NOT NULL);');
	
	PERFORM dblink_exec(
         'CREATE TABLE transaction (
			current_balance numeric(10) PRIMARY KEY,
			cost numeric(10) NOT NULL,
			counteragent_name text NOT NULL);');
			
	PERFORM dblink_exec(
         'CREATE TABLE purchase (
			id numeric(6) PRIMARY KEY,
			buyer_name text NOT NULL,
			weight numeric(10),
			price numeric(10) NOT NULL,
			status text);');
			
	PERFORM dblink_exec(
         'CREATE TABLE purchase_item (
			order_id numeric(6) PRIMARY KEY,
			item_id numeric(6) REFERENCES item(id));');
			
	PERFORM dblink_exec(
         'CREATE TABLE users (
			user_id numeric(6) PRIMARY KEY,
			username text NOT NULL,
			role text NOT NULL);');
		
	PERFORM dblink_exec(
         'CREATE ROLE admin WITH LOGIN PASSWORD ''admin'' CREATEROLE;
		  CREATE ROLE accountant;
		  CREATE ROLE merchandiser;');
		  
-- 	PERFORM dblink_exec(
--          'GRANT CREATEROLE TO admin;');
		  
	PERFORM dblink_exec(
		'CREATE OR REPLACE FUNCTION create_user(username text, password text, role text)
  			RETURNS void AS
		$func$
		BEGIN
		
		EXECUTE ''CREATE USER '' || username || '' WITH ROLE '' || role || '' LOGIN PASSWORD '' || password;

		END
		$func$ LANGUAGE plpgsql;'
	);


END IF;

END
$func$ LANGUAGE plpgsql;
