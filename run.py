import os

from app import app

if __name__ == "__main__":
    app.run(debug=True, load_dotenv=True, port=os.environ.get("PORT"))
