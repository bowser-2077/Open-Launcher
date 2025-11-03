import psycopg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

create_games_table = """
create table if not exists games (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  author text not null,
  description text,
  image_url text,
  download_url text,
  donation_enabled boolean default false,
  donation_link text
);
"""

create_users_table = """
create table if not exists users (
    pseudo text primary key,
    password_hash text not null
);
"""

def main():
    try:
        with psycopg.connect(DATABASE_URL) as conn:
            with conn.cursor() as cur:
                cur.execute(create_games_table)
                cur.execute(create_users_table)
                conn.commit()
                print("✅ Tables 'games' & 'users' created (or already exist)!")
    except Exception as e:
        print("❌ Error:", e)

if __name__ == "__main__":
    main()
