from re import A
import sys 
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from pokemon_app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
