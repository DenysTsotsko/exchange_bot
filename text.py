from parser import parse_currencies

currencies = parse_currencies()

for currency, values in currencies.items():
        print(f"Currency: {currency}")
        print(f"Buy: {values['buy']}")
        print(f"Sale: {values['sale']}")
        print()