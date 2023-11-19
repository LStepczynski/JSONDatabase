from JSONDatabase import JSONDatabase
from typing import Union
import logging
import ast
import os

class JSONDatabaseCLI:
    def __init__(self, storage_path) -> None:
        self.storage_path = storage_path
        self.database = JSONDatabase(self.storage_path)
        self.run = True
        self.initialize()

    def initialize(self) -> None:
        self.clear_cmd()
        print("This is the JSON Database Command Line Interface by Leon Stepczynski")
        print("For additional information check the .log file")
        print('Type "help" for the command list')
        while self.run:
            self.take_input()

    def take_input(self) -> None:
        user_input = input("\nJSON Database CLI >  ").strip()
        response = True
        print("")

        if user_input == "help":
            self.help()
        elif user_input == "exit":
            self.run = False
        elif user_input == "cls" or user_input == "clear":
            self.clear_cmd()
        elif user_input in ["create category", "remove category"]:
            self.handle_category(user_input)
        elif user_input == "create document":
            self.create_document()
        elif user_input == "remove document":
            self.remove_document()
        elif user_input == "find or":
            self.find_or()
        elif user_input == "find and":
            self.find_and()
        elif user_input == "find key":
            self.find_key()

        if not response:
            print("\nThere was a problem executing the command. For more information check the .log file")

    def handle_category(self, user_input) -> bool:
        category_action = self.database.add_category if user_input == "create category" else self.database.remove_category
        return category_action(input("Category Name: "))

    def create_document(self) -> bool:
        category = input("Category Name: ")
        if self.database.category_exists(category):
            result = self.document_creator()
            if result:
                result = self.database.add_document(result, category)
                print(f"The document was successfully added to \"{category}\"")
                if result:
                    return True
        else:
            logging.error(f"create_document() | The category \"{category}\" does not exist.")
        return False

    def remove_document(self) -> bool:
        print("Provide the category and uuid of the document you want to delete.\n")
        category = input("Category Name: ")
        document = self.database.find_or({"uuid": [input("Document uuid: ")]}, category)
        if document:
            result = self.database.remove_document(document[0], category)
            print("\nDocument successfully removed.")
            if result:
                return True
        else:
            pass
        return False

    def find_or(self):
        category = input("Enter category name to search: ")

        print("You will now create a filter that will find documents from a category that match any of the filters.")
        print("Remember that a value has to be a python list\n")

        response = self.document_creator()

        if response:
            search = self.database.find_or(response, category)
            for item in search:
                print(f"\n{item}")

    def find_and(self):
        category = input("Enter category name to search: ")

        print("You will now create a filter that will find documents from a category that match all of the filters.")
        print("Remember that a value has to be a python list and all lists must be of the same length\n")

        response = self.document_creator()

        if response:
            search = self.database.find_and(response, category)
            for item in search:
                print(f"\n{item}")

    def find_key(self):
        category = input("Enter category name to search: ")

        print("You will now provide a list of keys that will be searched for in each document of the category.")
        print("The document will be a match if it contains the key, no matter what the value is.\n")
        print('Type "finish" to complete or "discard" to abort.')

        keys = []

        while True:
            print(f"\nCurrent keys: {keys}")
            response = input("Enter a key: ").strip()
            if response == "discard":
                return True
            elif response == "finish":
                break
            keys.append(response)

        search = self.database.find_key(keys, category)
        for item in search:
            print(f"\n{item}")

    def document_creator(self) -> Union[dict, bool]:
        dictionary = {}
        print("\nYou will now create a document as a Python dictionary. Enter a key and a value.")
        print('Type "finish" to complete or "discard" to abort.')
        while True:
            print(f"\nCurrent document: {dictionary}")

            for prompt in ["Enter a key: ", "Enter a value: "]:
                response = input(prompt).strip()
                if response in ["finish", "discard"]:
                    return dictionary if response == "finish" and dictionary else False
                if prompt == "Enter a key: ":
                    key = response
                else:
                    try:
                        # Safely evaluate the input to handle data types like list, int, etc.
                        evaluated_response = ast.literal_eval(response)
                    except (ValueError, SyntaxError):
                        # If evaluation fails, treat as string
                        evaluated_response = response
                    dictionary[key] = evaluated_response
                    break

    def help(self):
        print("JSON Database CLI commands:")
        print("help - shows a list of all commands with brief descriptions")
        print("exit - ends the program")
        print("create category - Asks for a category name and creates it")
        print("remove category - Asks for a category name and removes it")
        print("create document - Helps with creating a document and adds it to a chosen category")
        print("remove document - Asks for a category and document uuid and removes it")
        print("find or - Asks for a category and search criteria, then performs a search")

    def clear_cmd(self):
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

JSONDatabaseCLI("tables")