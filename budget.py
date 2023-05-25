import math
class Category:
    def __init__(self, name):
        if len(name) >= 28:
            return ('Error: category name too long')
        self.name = name
        self.ledger = []

    def __str__(self):
        asterisks_by_side = (30 - len(self.name)) / 2
        if asterisks_by_side % 2 != 0:
            asterisks_by_side = [math.floor(asterisks_by_side), math.ceil(asterisks_by_side)]
        else:
            asterisks_by_side = [asterisks_by_side, asterisks_by_side]
        title = '*' * asterisks_by_side[0] + self.name + '*' * asterisks_by_side[1]
        movements = ''
        for movement in self.ledger:
            if len(movement['description']) > 23:
                movements += movement['description'][0:23] + ' ' + '{0:.2f}'.format(movement['amount']) + '\n'
            else:
                whitespace = (30 - len(movement['description']) - len('{0:.2f}'.format(movement['amount']))) * ' '
                movements += movement['description'] + whitespace + '{0:.2f}'.format(movement['amount']) + '\n'
        total = '{0:.2f}'.format(self.get_balance())
        return(title + '\n' + movements + 'Total: ' + total)

    def deposit(self, amount, description=''):
        if amount <= 0:
            return ('Error: deposited amount must be a positive number')
        if not isinstance(description, str):
            return ('Error: description must be a string')
        self.ledger.append({'amount': float(amount), 'description': description})

    def withdraw(self, amount, description=''):
        if amount <= 0:
            return ('Error: witdhrawn amount must be a positive number')
        if not isinstance(description, str) and description != "":
            raise TypeError('Error: description must be a string')
        if self.check_funds(amount):
            self.ledger.append({'amount': float(-amount), 'description': description})
            return True
        return False

    def get_balance(self):
        return sum(movement['amount'] for movement in self.ledger)

    def transfer(self, amount, dest_budget):
        if amount <= 0:
            return ('Error: transferred amount must be a positive number')
        if self.check_funds(amount):
            self.withdraw(amount, f'Transfer to {dest_budget.name}')
            dest_budget.deposit(amount, f'Transfer from {self.name}')
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

def create_spend_chart(categories):
    categories_len = [len(category.name) for category in categories]
    withdrawn_total = sum(
        movement['amount'] for category in categories for movement in category.ledger if movement['amount'] < 0)
    withdraws_per_cat = [{'name': category.name,
                          'withdrawn': sum(movement['amount'] for movement in category.ledger if
                                           movement['amount'] < 0)} for category in categories]
    for category in withdraws_per_cat:
        category['percentage'] = math.floor(category['withdrawn'] / withdrawn_total * 100 / 10) * 10

    chart = ['Percentage spent by category']
    y = ['100|', ' 90|', ' 80|', ' 70|', ' 60|', ' 50|', ' 40|', ' 30|', ' 20|', ' 10|', '  0|']

    n = 0
    while n < (12 + max(categories_len)):
        row = ''
        if n <= 10:
            row += y[n]
            for category in withdraws_per_cat:
                if category['percentage'] >= int(y[n].strip().replace('|', '')):
                    row += ' o '
                else:
                    row += '   '
        elif n == 11:
            row += '    ' + '---' * len(withdraws_per_cat)
        else:
            row += '    '
            for category in withdraws_per_cat:
                if (len(category['name']) > n - 12):
                    row += ' ' + category['name'][n - 12] + ' '
                else:
                    row += '   '
        chart.append(row)
        n += 1
    n = 1
    while n < len(chart):
        if chart[n].find('-') != -1:
            chart[n] = chart[n] + '-'
            n += 1
        else:
            chart[n] = chart[n] + ' '
            n += 1
    return("\n".join(chart))
