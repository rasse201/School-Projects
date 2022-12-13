from math import floor, ceil

class Category:
    def __init__(self, category_name):
        self.category_name = category_name
        self.ledger = []

    def deposit(self, amount, description = ''):
        self.ledger.append({'amount': float(amount), 'description': description})

    def withdraw(self, amount, description = ''):
        if self.check_funds(amount):
            self.ledger.append({'amount': -float(amount), 'description': description})
            return True
        else:
            return False

    def get_balance(self):
        balance = 0
        for element in self.ledger:
            balance += element['amount']
        return balance

    def transfer(self, amount, transfer_category):
        if not self.check_funds(amount):
            return False

        self.withdraw(amount, 'Transfer to %s'%transfer_category.category_name)
        transfer_category.deposit(amount, 'Transfer from %s'%self.category_name)
        return True

    def check_funds(self, amount):
        balance = self.get_balance()
        
        if balance - amount < 0:
            return False
        else:
            return True

    def __str__(self):
        rows = []
        side_stars = (30 - len(self.category_name)) / 2
        rows.append('*' * floor(side_stars) + self.category_name + '*' * ceil(side_stars))

        for element in self.ledger:
            amount = str(element['amount']).split('.')[0] + '.' + str(element['amount']).split('.')[1].ljust(2, '0')
            description = element['description']

            if len(amount) > 7:
                amount = amount[:7]

            if len(element['description']) > 23:
                description = description[:23]

            spaces = ' ' * (30 - len(description) - len(amount))
            rows.append(description + spaces + amount)

        rows.append('Total: %s'%self.get_balance())

        return '\n'.join(rows)

def create_spend_chart(categories):
    rows = []
    spends = []
    percentages = []
    category_names = []
    total_spent = 0

    rows.append('Percentage spent by category')
    for category in categories:
        amount = 0
        for element in category.ledger:
            if element['amount'] < 0:
                amount += element['amount']
        spends.append(amount)
        total_spent += amount
        category_names.append(category.category_name)

    for spend in spends:
        percentages.append(floor(spend * 10 / total_spent))

    for i in range(10, -1, -1):
        bars = ''
        side_percent = str(i * 10).rjust(3, ' ')

        for l, percent in enumerate(percentages):
            if percent < i:
                bars += '   '
            else:
                bars += ' o '

        rows.append('%s|'%side_percent + bars + ' ')
    
    rows.append(' ' * 4 + '-' * 10)

    for i in range(max([len(name)]for name in category_names)[0]):
        row = ' ' * 4
        for name in category_names:
            if len(name) > i:
                row += ' %s '%name[i]
            else:
                row += '   '
        rows.append(row + ' ')

    return '\n'.join(rows)