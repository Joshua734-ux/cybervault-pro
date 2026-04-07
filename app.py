import os
from flask import Flask
# ... (rest of your imports)

app = Flask(__name__)

# ... (your routes)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
