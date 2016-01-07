import os

# Database URI
# Enter your credentials. Use the generated URIs in model.py.
DB_USER="root"
DB_PASS=""
DB_HOST="localhost"
DB_NAME="cat_tax"

if not os.environ.get('IS_HEROKU'):
	MYSQL_KEY="mysql://" + DB_USER + ":" + DB_PASS + "@" + DB_HOST + "/" + DB_NAME
else:
	MYSQL_KEY=os.environ.get('CLEARDB_DATABASE_URL').strip('?reconnect=true')

# API Keys
GoogleAPI=""
