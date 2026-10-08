-- Stubs for what the Supabase services (GoTrue, Storage, Realtime) create on a real project.
create or replace function auth.jwt() returns jsonb language sql stable as $$
  select coalesce(nullif(current_setting('request.jwt.claims', true), '')::jsonb, '{}'::jsonb) $$;
create table if not exists auth.sessions (
  id uuid primary key default gen_random_uuid(), user_id uuid references auth.users(id) on delete cascade,
  created_at timestamptz default now(), updated_at timestamptz default now(), refreshed_at timestamp,
  user_agent text, ip inet);
create table if not exists realtime.messages (
  id bigserial, topic text not null, extension text not null default 'broadcast', payload jsonb,
  event text, private boolean default true, inserted_at timestamp default now(), updated_at timestamp default now(),
  primary key (id));
alter table realtime.messages enable row level security;
create or replace function realtime.topic() returns text language sql stable as $$
  select nullif(current_setting('realtime.topic', true), '')::text $$;
create or replace function realtime.send(payload jsonb, event text, topic text, private boolean default true)
returns void language plpgsql as $$
begin insert into realtime.messages (payload, event, topic, private) values (payload, event, topic, private); end $$;
create table if not exists storage.buckets (id text primary key, name text not null unique, owner uuid,
  public boolean default false, created_at timestamptz default now(), updated_at timestamptz default now());
create table if not exists storage.objects (id uuid primary key default gen_random_uuid(), bucket_id text references storage.buckets(id),
  name text, owner uuid, created_at timestamptz default now(), updated_at timestamptz default now(),
  last_accessed_at timestamptz default now(), metadata jsonb);
alter table storage.objects enable row level security;
create or replace function storage.foldername(name text) returns text[] language plpgsql as $$
declare _parts text[]; begin select string_to_array(name, '/') into _parts; return _parts[1:array_length(_parts,1)-1]; end $$;
grant usage on schema realtime, storage to authenticated, anon;
grant select, insert on realtime.messages to authenticated;
grant select, insert, update, delete on storage.objects to authenticated;
alter table auth.users add column if not exists email_confirmed_at timestamptz;
alter table auth.users add column if not exists phone text;
alter table auth.users add column if not exists phone_confirmed_at timestamptz;
alter table auth.users add column if not exists last_sign_in_at timestamptz;
alter table auth.users add column if not exists raw_user_meta_data jsonb;
alter table auth.users add column if not exists deleted_at timestamptz;
