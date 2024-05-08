from src.data_generator import DataGenerator

ACCOUNT_SETTINGS_PATH = "pkg/settings.json"
CREDENTIALS_FILE_PATH = "pkg/credentials.json"

def main():

    data_generator = DataGenerator(ACCOUNT_SETTINGS_PATH, CREDENTIALS_FILE_PATH)

    connected = data_generator.connect()
    
    metatrader5 = data_generator.get_context_mt5().get_metatrader()

    if (connected):    
        data_generator.create_data_from_quantity(10)
        #data_generator.create_data_from_timestamp(1672531200,1688083200)
        
        """
        symbols = metatrader5.symbols_get("BCHUSD")
        count = 0
        for symbol in symbols:
            print(symbol.name)
            count += 1

        print(count)
        """
if __name__ == '__main__':
    main()