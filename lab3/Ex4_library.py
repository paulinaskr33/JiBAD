import json  # zalecone przez dr Gajeckiego
from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self):
        self.books = []
        self.users = []
        self.current_user = None

    def load_data(self):
        try:
            with open("library_data.json", "r") as file:
                data = json.load(file)
                self.books = data["books"]
                self.users = data["users"]
        except FileNotFoundError:
            pass

    def save_data(self):
        data = {"books": self.books, "users": self.users}
        with open("library_data.json", "w") as file:
            json.dump(data, file)

    def login(self, username, role):
        for user in self.users:
            if user["username"] == username and user["role"] == role:
                self.current_user = user
                return True
        return False

    def search_catalog(self, keyword):
        results = []
        for book in self.books:
            if keyword.lower() in book["title"].lower() or keyword.lower() in book["author"].lower() or keyword.lower() in book["keywords"]:
                results.append(book)
        return results

    def borrow_book(self, book_title):
        for book in self.books:
            if book["title"].lower() == book_title.lower() and not book["borrowed"]:
                book["borrowed"] = True
                book["borrower"] = self.current_user["username"]
                book["due_date"] = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
                return f"Book '{book_title}' borrowed successfully. Due date: {book['due_date']}"
        return f"Book '{book_title}' is not available for borrowing."

    def reserve_book(self, book_title):
        for book in self.books:
            if book["title"].lower() == book_title.lower() and not book["borrowed"] and not book["reserved"]:
                book["reserved"] = True
                book["reserver"] = self.current_user["username"]
                return f"Book '{book_title}' reserved successfully."
        return f"Book '{book_title}' cannot be reserved."

    def extend_loan(self, book_title):
        for book in self.books:
            if book["title"].lower() == book_title.lower() and book["borrowed"] and self.current_user["role"] == "reader":
                book["due_date"] = (datetime.strptime(book["due_date"], "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")
                return f"Loan for '{book_title}' extended successfully. New due date: {book['due_date']}"
        return f"Loan extension for '{book_title}' not possible."

    def return_book(self, book_title):
        for book in self.books:
            if book["title"].lower() == book_title.lower() and book["borrowed"]:
                book["borrowed"] = False
                book["borrower"] = None
                book["due_date"] = None
                return f"Book '{book_title}' returned successfully."
        return f"Book '{book_title}' is not currently on loan."

    def add_book(self, book_details):
        self.books.append(book_details)
        return f"Book '{book_details['title']}' added to the catalog."

    def remove_book(self, book_title):
        for book in self.books:
            if book["title"].lower() == book_title.lower():
                self.books.remove(book)
                return f"Book '{book_title}' removed from the catalog."
        return f"Book '{book_title}' not found in the catalog."

    def add_user(self, user_details):
        self.users.append(user_details)
        return f"User '{user_details['username']}' added to the system."

    def browse_catalog(self):
        return self.books

if __name__ == '__main__':
    library_system = LibrarySystem()
    library_system.load_data()

