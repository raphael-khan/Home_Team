from app import app
from app.controllers import public, private

if __name__ == "__main__":
    app.run(debug=True)