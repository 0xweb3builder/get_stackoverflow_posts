# Statement for enabling the development environment
DEBUG = True

# Define the application directory
import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  

# Define the database - we are working with
# SQLite for this example
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(BASE_DIR, 'app.db')
DATABASE_CONNECT_OPTIONS = {}

# Application threads. A common general assumption is
# using 2 per available processor cores - to handle
# incoming requests using one and performing background
# operations using the other.
THREADS_PER_PAGE = 2

# Enable protection agains *Cross-site Request Forgery (CSRF)*
CSRF_ENABLED     = False

# Use a secure, unique and absolutely secret key for
# signing the data. 
CSRF_SESSION_KEY = "TOPCODER_KEY"

# Secret key for signing cookies
SECRET_KEY = "TOPCODER_KEY"

# StackExchange API key
#SE_API_KEY = "pXlviKYs*UZIwKLPwJGgpg(("
SE_API_KEY = "STfed*aS9LYUSEFMNwALZQ(("

# StackExchange Get Posts Api filter
FILTER_TITLE_BODY = "!-*f(6qnw-e4e" # Include title and body

STACKOVERFLOW_CLIENT_ID = 11156
STACKOVERFLOW_CLIENT_SECRET = "VBIfdwwTXnk4at2v6LVPUw(("

OAUTH_CREDENTIALS={
        'stackoverflow': {
            'id': STACKOVERFLOW_CLIENT_ID,
            'secret': STACKOVERFLOW_CLIENT_SECRET
        }
}
