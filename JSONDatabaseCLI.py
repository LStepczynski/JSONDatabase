from JSONDatabase import JSONDatabase
from typing import Union
import logging
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
        print("Type \"help\" for the command list")

        while self.run:
            self.take_input()


    def take_input(self) -> None:
        user_input = input("\nJSON Database CLI >  ").strip()
        response = True

        print("")

        # Displays all commands
        if user_input == "help":
            self.help()

        # Exits out of the program
        elif user_input == "exit":
            self.run = False

        # Creates/removes a category
        elif user_input in ["create category", "remove category"]:
            category_action = self.database.add_category if user_input == "create category" else self.database.remove_category
            response = category_action(input("Category Name: "))

        # Creates a new document
        elif user_input == "create document":
            category = input("Category Name: ")
            if self.database.category_exists(category):
                result = self.document_creator()
                if result:
                    self.database.add_document(result, category)
                    print(f"The document was successfully added to \"{category}\"")
            else:
                response = False
                logging.error(f"take_input() | The category \"{category}\" does not exist.")

        # Removes a document
        elif user_input == "remove document":
            print("Provide the category and uuid of the document you want to delete.\n")
            category = input("Category Name: ")
            document = self.database.find_or({"uuid":[input("Document uuid: ")]}, category)
            if document:
                response = self.database.remove_document(document[0], category)
                print("\nDocument succesfuly removed.")
            else:
                response = False

        if not response:
            print("\nThere was a problem executing the command. For more information check the .log file")


    def document_creator(self) -> Union[dict, bool]:
        dictionary = {}
        print("\nCreate a document as a Python dictionary. Enter a key and a value.")
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
                    dictionary[key] = response
                    break


    def help(self):
        print("JSON Database CLI commands:")
        print("help - shows a list of all commands with brief descriptions")
        print("exit - ends the program")
        print("create category | Asks for a category name and creates it")
        print("remove category | Asks for a category name and removes it")
        print("create document | Helps with creating a document and adds it to a choosen category")
        print("remove document | Asks for a category and document uuid and removes it")


    def clear_cmd(self):
        # Check if the operating system is Windows
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')

JSONDatabaseCLI("tables")