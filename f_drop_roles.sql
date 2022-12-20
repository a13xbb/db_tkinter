CREATE EXTENSION dblink;


CREATE OR REPLACE FUNCTION f_drop_roles()
  RETURNS void AS
$func$
BEGIN

	PERFORM dblink_connect('dbname=' || current_database() || ' user=postgres' ||
						  ' password=1989');
	
	PERFORM dblink_exec('
						DROP ROLE admin;
						DROP ROLE merchandiser;
						DROP ROLE accountant;');

END
$func$ LANGUAGE plpgsql;
