import os
import json

class JsonReader(object):

    file_path: str
    json_data: dict

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path
        self.json_data = self.get_json_from_file(self.file_path)

    def get_json_from_file(self, file_path: str) -> dict:
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf8") as file:
                # Convert to json object
                json_data = json.load(file)
                return json_data
        raise FileExistsError(f"Could not locate resource: {file_path}")
    
    def get_json_data(self) -> dict:
        return self.json_data
    
    def get_symbol(self) -> str:
        return self.json_data["mt5"]["symbol"]
    
    def get_timeframe(self) -> str:
        return self.json_data["mt5"]["timeframe"]