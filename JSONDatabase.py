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


    def edit_document(self, old_document:dict, new_document:dict, category:str) -> None:
        if not self.category_exists(category):
            logging.error(f"edit_document() | The category that the document is being edited in does not exist \"{category}\".")
            return
        
        if type(new_document) != dict:
            logging.error(f"edit_document() | The document being edited in \"{category}\" isn't a dictionary.")

        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)

        try:
            category_json.remove(old_document)
        except ValueError:
            logging.error(f"edit_document() | The document being edited in \"{category}\" does not exist in the category.")
        
        category_json.append(new_document)

        with open(f"{self.storage_path}/{category}.json", "w") as f:
            json.dump(category_json, f, indent=4)

        logging.info(f"edit_document() | A document was edited in \"{category}\".")


    def find_or(self, filter:dict, category:str) -> list:
        """Method that will search a category and return documents as a list that match any of the filters. 
        The filter must be a dictionary which values are a list. Example:
        {"key1":["value1", "value2", "value3"], "key2":["value1", "value2", "value3"]}"""

        if not self.category_exists(category):
            logging.error(f"find_or() | The category that the document is being searched for in does not exist \"{category}\".")
            return

        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)

        elements = []

        for document in category_json:
            flag = True
            for key, values in filter.items():
                if type(values) != list:
                    logging.error(f"find_or() | The filter is not properly formated \"{filter}\".")
                    return []
                for value in values:
                    try:
                        if document[f"{key}"] == value:
                            elements.append(document)
                            flag = False
                            break
                    except KeyError:
                        pass
                if not flag:
                    break
        
        return elements


    def find_and(self, filter:dict, category:str) -> list:
        """Method that will search a category and return documents as a list that match all of the filters. 
        The filter must be a dictionary. The values of the filter must be a list and be of the same length. Example:
        {"key1":["value1", "value2", "value3"], "key2":["value1", "value2", "value3"]}"""

        if not self.category_exists(category):
            logging.error(f"find_and() | The category that the document is being searched for in does not exist \"{category}\".")
            return

        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)

        elements = []
        length = None

        for document in category_json:
            fit = True
            flag = True
            for key, values in filter.items():
                if type(values) != list:
                    logging.error(f"find_and() | The filter is not properly formated \"{filter}\".")
                    return []
                
                if len(values) != length and length != None:
                    logging.error(f"find_and() | The length of the values in the filter are not the same.")
                    return []
                
                length = len(values)

                for value in values:
                    try:
                        if document[f"{key}"] == value:
                            continue
                    except KeyError:
                        pass
                    fit = False
                    flag = False
                    break

                if not flag:
                    break
            
            if fit:
                elements.append(document)
        
        return elements
    

    def find_key(self, filter:list, category:str) -> list:
        """Method that will search a category and return documents as a list that match any of the filters. 
        The filter must be a list. Example:
        ["key1", "key2", "key3"]"""

        if not self.category_exists(category):
            logging.error(f"find_key() | The category that the document is being searched for in does not exist \"{category}\".")
            return

        with open(f"{self.storage_path}/{category}.json", "r") as f:
            category_json = json.load(f)

        elements = []

        for document in category_json:
            for key in filter:
                if key in document:
                    elements.append(document)

        return elements


    def category_exists(self, name:str) -> bool:
        if os.path.exists(f"{self.storage_path}/{name}.json"):
            return True
        else:
            return False

