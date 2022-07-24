import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pokemon_app import create_app

from dotenv import load_dotenv

load_dotenv(override=True)
MODE = os.environ.get('MODE')
app = create_app(MODE)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
