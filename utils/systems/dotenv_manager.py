# check if dotenv file exists if not, create it
import os

def setup_dotenv():
    print("Checking for .env file")
    if not os.path.isfile('.env'):
        print("No .env file found, creating one")
        with open('.env', 'w') as f:
            f.write("CLIENT_ID=""\n" \
                    "CLIENT_SECRET=""\n" \
                    "CHANNEL_NAME=")
        print("Please fill out the .env file with the appropriate values")
        exit()
    else:
        print(".env file found. Continuing...")