import json
import os

class Expense:
    def __init__(self, description, amount, category, date):
        self.description = description
        self.amount = amount
        self.category = category
        self.date = date

    def to_dict(self):
        return {
            "description": self.description,
            "amount": self.amount,
            "category": self.category,
            "date": self.date
        }

    def __str__(self):
        return f"{self.date} | {self.description} | ${self.amount:.2f} | Category: {self.category}"

class ExpenseManager:
    def __init__(self, filename="expenses.json"):
        self.filename = filename
        self.expenses = self.load_expenses()

    # Load expenses from JSON file
    def load_expenses(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                return [Expense(**item) for item in data]
        return []

    # Save expenses to JSON file
    def save_expenses(self):
        with open(self.filename, "w") as f:
            json.dump([exp.to_dict() for exp in self.expenses], f, indent=4)

    # Add new expense
    def add_expense(self, expense):
        self.expenses.append(expense)
        self.save_expenses()
        print(f"✅ Expense '{expense.description}' in category '{expense.category}' added!")

    # View all expenses
    def view_expenses(self):
        if not self.expenses:
            print("🚫 No Expenses recorded yet.")
            return
        print("\n--- All Expenses ---")
        for i, exp in enumerate(self.expenses, start=1):
            print(f"{i}. {exp}")

    # Search expenses
    def search_expenses(self, keyword):
        results = [exp for exp in self.expenses if keyword.lower() in exp.description.lower() or keyword.lower() in exp.category.lower()]
        if results:
            print(f"\n🔍 Search results for '{keyword}':")
            for exp in results:
                print(exp)
        else:
            print(f"No expenses found for '{keyword}'.")

    # Delete expense
    def delete_expense(self, index):
        if 0 <= index < len(self.expenses):
            removed = self.expenses.pop(index)
            self.save_expenses()
            print(f"❌ Deleted expense: {removed}")
        else:
            print("Invalid expense number.")

    # Edit expense
    def edit_expense(self, index, new_description=None, new_amount=None, new_category=None, new_date=None):
        if 0 <= index < len(self.expenses):
            exp = self.expenses[index]
            if new_description:
                exp.description = new_description
            if new_amount:
                exp.amount = new_amount
            if new_category:
                exp.category = new_category
            if new_date:
                exp.date = new_date
            self.save_expenses()
            print(f"✏️ Updated expense #{index + 1}: {exp}")
        else:
            print("Invalid expense number.")

    # Total spent overall
    def total_spent(self):
        total = sum(exp.amount for exp in self.expenses)
        print(f"\n💰 Total Spent: ${total:.2f}")

    # Total spent by category
    def total_by_category(self):
        summary = {}
        for exp in self.expenses:
            summary[exp.category] = summary.get(exp.category, 0) + exp.amount
        print("\n📊 Total Spent by Category:")
        for cat, amt in summary.items():
            print(f"{cat}: ${amt:.2f}")


# ----------------- Main Menu -----------------
def main():
    manager = ExpenseManager()

    while True:
        print("\n=== Expense Tracker ===")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. Search Expenses")
        print("4. Delete Expense")
        print("5. Show Total Spent")
        print("6. Show Total by Category")
        print("7. Modify Expense")
        print("8. Exit")

        choice = input("Enter Choice: ")

        if choice == "1":
            desc = input("Enter description: ")
            amount = float(input("Enter amount: "))
            category = input("Enter category: ")
            date = input("Enter Date (YYYY-MM-DD): ")
            exp = Expense(desc, amount, category, date)
            manager.add_expense(exp)
        elif choice == "2":
            manager.view_expenses()
        elif choice == "3":
            keyword = input("Enter search keyword: ")
            manager.search_expenses(keyword)
        elif choice == "4":
            manager.view_expenses()
            num = int(input("Enter expense number to delete: ")) - 1
            manager.delete_expense(num)
        elif choice == "5":
            manager.total_spent()
        elif choice == "6":
            manager.total_by_category()
        elif choice == "7":
            manager.view_expenses()
            num = int(input("Enter expense number to edit: ")) - 1
            new_desc = input("Enter new description (leave blank to keep same): ")
            new_amt_input = input("Enter new amount (leave blank to keep same): ")
            new_amt = float(new_amt_input) if new_amt_input else None
            new_cat = input("Enter new category (leave blank to keep same): ")
            new_date = input("Enter new date (YYYY-MM-DD) (leave blank to keep same): ")
            manager.edit_expense(num, new_desc or None, new_amt, new_cat or None, new_date or None)
        elif choice == "8":
            print("Goodbye! 👋")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
