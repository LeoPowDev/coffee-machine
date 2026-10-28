from prettytable import PrettyTable


class Drink:
    def __init__(self, name, ingredients, price):
        self.name = name
        self.ingredients = ingredients
        self.price = price


class MachineResources:
    def __init__(self, coffee, milk, water, money):
        self.coffee = coffee
        self.milk = milk
        self.water = water
        self.money = money

    def report(self):
        print("=== MACHINE REPORT ===")

        table = PrettyTable()
        table.field_names = ["Resource", "Amount"]

        table.add_row(["Coffee (g)", self.coffee])
        table.add_row(["Milk (ml)", self.milk])
        table.add_row(["Water (ml)", self.water])
        table.add_row(["Money ($)", self.money])

        print(table)
        print()  


class CoffeeMachine:
    def __init__(self):
        self.resources = MachineResources(
            coffee=80,
            milk=250,
            water=500,
            money=0
        )

        self.coins = {
            "quarter": 0.25,
            "nickel": 0.05,
            "penny": 0.01,
            "dollar": 1.00
        }

        self.history = []

        self.menu = {
            "cappuccino": Drink(
                "cappuccino",
                {"Milk": 180, "Water": 120, "Coffee": 24},
                3.00
            ),
            "latte": Drink(
                "latte",
                {"Milk": 150, "Water": 120, "Coffee": 18},
                2.50
            ),
            "espresso": Drink(
                "espresso",
                {"Water": 120, "Coffee": 20},
                1.50
            )
        }

    def show_history(self):
        print("=== PURCHASE HISTORY ===")

        if len(self.history) == 0:
            print("No drinks bought yet.")
            print()
            return

        table = PrettyTable()
        table.field_names = ["#", "Drink", "Change ($)"]

        for i, purchase in enumerate(self.history, start=1):
            table.add_row([
                i,
                purchase["drink"].capitalize(),
                purchase["change"]
            ])

        print(table)
        print()  

    def check_ingredients(self, drink):
        ingredients = drink.ingredients

        if "Milk" in ingredients and self.resources.milk < ingredients["Milk"]:
            print("Sorry, not enough milk.")
            return False

        if "Water" in ingredients and self.resources.water < ingredients["Water"]:
            print("Sorry, not enough water.")
            return False

        if "Coffee" in ingredients and self.resources.coffee < ingredients["Coffee"]:
            print("Sorry, not enough coffee.")
            return False

        return True

    def take_payment(self, price):
        print("Please insert your money.")

        def get_number(text):
            while True:
                try:
                    num = int(input(text))
                    if num < 0:
                        print("Enter a positive number.")
                        continue
                    return num
                except ValueError:
                    print("Enter a whole number.")

        quarters = get_number("How many quarters? ")
        nickels = get_number("How many nickels? ")
        pennies = get_number("How many pennies? ")
        dollars = get_number("How many dollars? ")

        total = (
            quarters * self.coins["quarter"]
            + nickels * self.coins["nickel"]
            + pennies * self.coins["penny"]
            + dollars * self.coins["dollar"]
        )

        print("You paid: $", total)

        if total < price:
            print("Not enough money. Refunding.")
            print()
            return 0

        change = total - price
        print("Payment accepted.")
        print("Your change is: $", change)
        print()

        return total

    def make_coffee(self, drink):
        ingredients = drink.ingredients

        if "Coffee" in ingredients:
            self.resources.coffee -= ingredients["Coffee"]

        if "Milk" in ingredients:
            self.resources.milk -= ingredients["Milk"]

        if "Water" in ingredients:
            self.resources.water -= ingredients["Water"]

    def ask(self):
        print("CoffeeMachine.")

        ask = input(
            "Options: espresso, latte, cappuccino, report, history, off: "
        ).lower().strip()

        print()  
        return ask

    def run(self):
        while True:
            choice = self.ask()

            if choice == "off":
                print("Machine shutting down.")
                break

            if choice == "report":
                self.resources.report()
                continue

            if choice == "history":
                self.show_history()
                continue

            if choice not in self.menu:
                print("Invalid choice.")
                print()
                continue

            drink = self.menu[choice]

            if not self.check_ingredients(drink):
                print()
                continue

            payment = self.take_payment(drink.price)

            if payment == 0:
                continue

            change = payment - drink.price

            self.history.append({
                "drink": drink.name,
                "change": change
            })

            self.resources.money += drink.price

            self.make_coffee(drink)

            print("Here is your", drink.name)
            print("Enjoy!")
            print()


machine = CoffeeMachine()
machine.run()
