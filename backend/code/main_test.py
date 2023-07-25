from website import create_app
import os

# Drop Table for Testing
path = "C:/Users/cownj/OneDrive/Desktop/4050/CSCI4050Project/backend/code/instance/"
if not os.path.isfile(path + "database.db"):
    os.remove(path + "database.db")

# Init App
app = create_app()

# Run App
if __name__ == '__main__':
    app.run(debug=True)