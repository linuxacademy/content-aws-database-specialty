create function slow_version() RETURNS text AS
    $$
      select pg_sleep(5);
      select version();
    $$
    LANGUAGE SQL;
