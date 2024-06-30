import os

import psycopg2

conn = psycopg2.connect(f"""dbname={os.getenv("POSTGRES_DB")} 
                           user={os.getenv("POSTGRES_USER")}
                           password={os.getenv("POSTGRES_PASSWORD")}
                           port=5432
                           host=postgres
                        """)
