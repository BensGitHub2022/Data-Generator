from src.data_generator import DataGenerator

ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

def main():

    data_generator = DataGenerator(ACCOUNT_SETTINGS_PATH, CREDENTIALS_FILE_PATH)

    connected = data_generator.connect()
    
    if (connected):    
        #data_generator.create_data_from_quantity(1000000)
        data_generator.create_data_from_timestamp(1672531200,1704067200)

if __name__ == '__main__':
    main()