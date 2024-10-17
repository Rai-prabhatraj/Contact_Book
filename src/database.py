import pymongo

class Database:
    def __init__(self):
        # Connect to MongoDB
        self.client = pymongo.MongoClient("mongodb://localhost:27017/contact")
        self.db = self.client["contact_book"]
        self.collection = self.db["contacts"]

    def add_contact(self, name, phone_number):
        """Add a contact to the MongoDB collection."""
        contact = {"name": name, "phone_number": phone_number}
        self.collection.insert_one(contact)
        print(f"Contact {name} with phone number {phone_number} added successfully!")

    def view_contacts(self):
        """Return all contacts in the collection."""
        return list(self.collection.find())
