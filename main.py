
"""
This program shows a business management system by using two classes.
Business class represent business name, money available and dictionary to store items and
deals. Ware class has items with name and price. Furthermore, this Python program allows
the user to create a new business or manage existing ones, restocking items by decreasing available money
and increasing item quantities, checking item prices with deals, checking item availability,
sell items, add and remove deals, and quit the program.

So why did we use the pickle module?
The dictionary holding details about the business are stored in a file using pickle,
then it allows the program to load and save data between sessions.
"""
import pickle

# Ware class to store information about ware
class Ware:
    def __init__(self, name, buy_price):
        self.name = name
        self.buy_price = buy_price
        self.discount = 0  # Discount applied to the ware's price
        self.quantity = 0  # Quantity of the ware in stock

    # Calculate the current price of the ware considering the discount
    def calculate_price(self):
        return self.buy_price * (1 - self.discount)

# Business class created to store information about the business
class Business:
    def __init__(self, name, money_available):
        self.name = name
        self.money_available = money_available
        self.wares = {}  # Dictionary to store wares and their quantities

    # Restock a ware, decreasing money available and increasing ware quantity
    def restock_ware(self, ware_name, quantity, buy_price):
        if ware_name in self.wares:
            self.wares[ware_name].buy_price = buy_price  # Update the ware's buy price
            self.wares[ware_name].discount = 0  # Reset the ware's discount
            self.wares[ware_name].quantity += quantity
        else:
            self.wares[ware_name] = Ware(ware_name, buy_price)  # Create a new ware object with discount 0
            self.wares[ware_name].quantity = quantity

        self.money_available -= quantity * buy_price

    # Check the price of a ware
    def check_price(self, ware_name):
        if ware_name in self.wares:
            return self.wares[ware_name].calculate_price()
        return None

    # Check the availability of a ware
    def check_availability(self, ware_name):
        if ware_name in self.wares:
            return self.wares[ware_name].quantity
        return 0

    # Sell a ware, decreasing ware quantity and increasing money earned
    def sell_ware(self, ware_name, quantity):
        if ware_name in self.wares and self.wares[ware_name].quantity >= quantity:
            earnings = quantity * self.wares[ware_name].calculate_price()
            self.wares[ware_name].quantity -= quantity
            self.money_available += earnings
            return earnings
        return None

    # Add a deal to a ware, providing a discount percentage
    def add_deal(self, ware_name, discount_percentage):
        if ware_name in self.wares:
            # Apply the discount to the ware's price
            self.wares[ware_name].discount = discount_percentage / 100
            print(f"Deal added for {ware_name} with a {discount_percentage}% discount.")
        else:
            print(f"Failed to add deal: Ware '{ware_name}' does not exist.")

    # Remove a deal from a ware
    def remove_deal(self, ware_name):
        if ware_name in self.wares:
            # Reset the ware's discount
            self.wares[ware_name].discount = 0
            print(f"Deal removed for {ware_name}.")
        else:
            print(f"Failed to remove deal: Ware '{ware_name}' does not exist.")

    # Get a list of available wares and their details
    def get_available_wares(self):
        available_wares = []
        for ware_name, ware in self.wares.items():
            available_wares.append(f"{ware_name} - Quantity: {ware.quantity}, Price: {ware.calculate_price()}")
        return available_wares

# Save data to a file using pickle
def save_data(data, filename):
    with open(filename, 'wb') as file:
        pickle.dump(data, file)

# Load data from a file using pickle
def load_data(filename):
    try:
        with open(filename, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return {}

# Main program
businesses = load_data('businesses_data.pkl')

while True:
    print("Available businesses:")
    for business_name in businesses.keys():
        print(business_name)

    choice = input("Enter the name of the business (or 'new' to create a new business): ").strip()

    if choice.lower() == 'new':
        # Create a new business
        business_name = input("Enter the name of the new business: ")
        money_available = float(input("Enter the initial money available for the business: "))
        businesses[business_name] = Business(business_name, money_available)
    elif choice in businesses:
        # Access an existing business
        current_business = businesses[choice]
        print(f"Current money available for {current_business.name}: {current_business.money_available}")
        action = input("Enter 'restock', 'price', 'availability', 'sell', 'add deal', 'remove deal', 'available wares', 'delete', or 'quit': ").strip()

        if action.lower() == 'restock':
            # Restock a ware
            ware_name = input("Enter the name of the ware: ")
            quantity = int(input("Enter the quantity: "))
            buy_price = float(input("Enter the buy price per unit: "))
            current_business.restock_ware(ware_name, quantity, buy_price)
        elif action.lower() == 'price':
            # Check the price of a ware
            ware_name = input("Enter the name of the ware: ")
            price = current_business.check_price(ware_name)
            if price is not None:
                print(f"Price of {ware_name}: {price}")
            else:
                print(f"{ware_name} not available in stock.")
        elif action.lower() == 'availability':
            # Check the availability of a ware
            ware_name = input("Enter the name of the ware: ")
            availability = current_business.check_availability(ware_name)
            print(f"Available quantity of {ware_name}: {availability}")
        elif action.lower() == 'sell':
            # Sell a ware
            ware_name = input("Enter the name of the ware: ")
            quantity = int(input("Enter the quantity to sell: "))
            earnings = current_business.sell_ware(ware_name, quantity)
            if earnings is not None:
                print(f"Earnings from selling {quantity} {ware_name}: {earnings}")
            else:
                print(f"Not enough stock of {ware_name} to sell.")
        elif action.lower() == 'add deal':
            # Add a deal to a ware
            ware_name = input("Enter the name of the ware: ")
            discount_percentage = float(input("Enter the discount percentage: "))
            current_business.add_deal(ware_name, discount_percentage)
        elif action.lower() == 'remove deal':
            # Remove a deal from a ware
            ware_name = input("Enter the name of the ware: ")
            current_business.remove_deal(ware_name)
        elif action.lower() == 'available wares':
            # Get a list of available wares and their details
            available_wares = current_business.get_available_wares()
            if available_wares:
                print("Available Wares:")
                for ware_details in available_wares:
                    print(ware_details)
            else:
                print("No wares available in stock.")
        elif action.lower() == 'delete':
            # Delete a business
            del businesses[choice]
            print(f"Business '{choice}' has been deleted.")
            save_data(businesses, 'businesses_data.pkl')
        elif action.lower() == 'quit':
            # Save data before exiting the program
            save_data(businesses, 'businesses_data.pkl')
            break
        else:
            print("Invalid input, please try again.")
    else:
        print("Business not available, please try again.")