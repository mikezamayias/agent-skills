\set ON_ERROR_STOP 1
\pset format unaligned
\pset tuples_only on
-- One suite. Suites run in file-name order in one database, so a later suite may rely on
-- an earlier one's rows. Every check is one row: a sentence saying what must hold, and a boolean.
create table if not exists public._smoke_example (n serial, name text, pass boolean);
grant all on public._smoke_example to authenticated;
grant usage on sequence public._smoke_example_n_seq to authenticated;

-- Arrange as the superuser.
insert into auth.users (id, email) values ('00000000-0000-0000-0000-00000000a001', 'a@example.com');

-- Act as a signed-in user, the way the app calls the database.
set role authenticated;
select set_config('request.jwt.claim.sub', '00000000-0000-0000-0000-00000000a001', false),
       set_config('request.jwt.claims', '{"sub":"00000000-0000-0000-0000-00000000a001","role":"authenticated"}', false);
insert into public._smoke_example (name, pass) select '01 a user sees their own profile',
  exists (select 1 from public.profiles where id = '00000000-0000-0000-0000-00000000a001');
reset role;

-- Act as nobody. anon cannot write to the results table, so capture the result into a variable
-- and record it after resetting the role. Row security returns only visible rows. A table with
-- no grant at all raises an error instead, so test that case with has_table_privilege().
set role anon;
select count(*) = 0 as anon_sees_nothing from public.profiles \gset
reset role;
insert into public._smoke_example (name, pass) select '02 an anonymous caller sees no profiles',
  :'anon_sees_nothing'::boolean;

-- Privileges: server-only functions stay closed to the app.
insert into public._smoke_example (name, pass) select '03 a server-only function is not callable by the app',
  not has_function_privilege('authenticated', 'public.server_only_fn()', 'execute');

-- Anything that queues work through triggers (pg_net, queues) is checked inside one transaction,
-- so a background worker cannot drain the queue before the check reads it.
begin;
-- ... act, then assert on the queue ...
commit;

\pset tuples_only off
select n, name, pass from public._smoke_example order by n;
select count(*) filter (where pass) as passed, count(*) as total from public._smoke_example;
