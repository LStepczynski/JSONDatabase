import logging
import json
import uuid
import os

class JSONDatabase:
    def __init__(self, storage_path: str) -> None:
        self.storage_path = storage_path

        logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', filename='JSONDatabaseLogs.log', filemode='a', level=logging.DEBUG)

    
    def add_category(self, name: str) -> None:
        if self.category_exists(name):
            logging.error(f"add_category() | The category \"{name}\" already exists.")
            return

        with open(f"{self.storage_path}/{name}.json", 'w') as f:
            json.dump([], f, indent=4)
        
        logging.info(f"add_category() | A category was succesfuly created: \"{name}\".")


    def remove_category(self, name:str) -> None:
        if not self.category_exists(name):
            logging.error(f"remove_category() | The category does not exist \"{name}\".")
            return
        
        os.remove(f"{self.storage_path}/{name}.json")

        logging.info(f"remove_category() | The category was succesfuly removed \"{name}\".")


    def add_document(self, document:dict, category:str) -> None:
        if not self.category_exists(category):
            logging.error(f"add_document() | The category that the document is being added to does not exist \"{category}\".")
            return
        
        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)
        
        document["uuid"] = str(uuid.uuid4())

        category_json.append(document)

        with open(f"{self.storage_path}/{category}.json", "w") as f:
            json.dump(category_json, f, indent=4)

        logging.info(f"add_document() | A document was succesfuly added to \"{category}\".")

    
    def remove_document(self, document:dict, category:str) -> None:
        if not self.category_exists(category):
            logging.error(f"remove_document() | The category that the document is being removed from does not exist \"{category}\".")
            return
        
        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)

        try:
            category_json.remove(document)
        except ValueError:
            logging.error(f"remove_document() | The document being removed from \"{category}\" does not exist in the category.")

        with open(f"{self.storage_path}/{category}.json", "w") as f:
            json.dump(category_json, f, indent=4)

        logging.info(f"remove_document() | A document was removed from \"{category}\".")


    


    def category_exists(self, name:str) -> bool:
        if os.path.exists(f"{self.storage_path}/{name}.json"):
            return True
        else:
            return False


database = JSONDatabase("tables")

database.add_document({}, "example")
