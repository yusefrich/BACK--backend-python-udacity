# "Database code" for the DB Forum.

import psycopg2, bleach

DBNAME = "forum"

def get_posts():
  """Return all posts from the 'database', most recent first."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  query = "select content, time from posts order by time desc;"
  c.execute(query)
  values = c.fetchall()
  db.close()
  return values

def add_post(content):
  """Add a post to the 'database' with the current timestamp."""
  db = psycopg2.connect(database=DBNAME)
  c = db.cursor()
  c.execute("insert into posts values (%s) ", (content,))
  db.commit()
  db.close()



