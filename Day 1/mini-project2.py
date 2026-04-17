# Mini Ecommerce

def calculate_total(*prices, tax=0.1, discount=0):
    sub_total = sum(prices)
    tax_amount = sub_total * tax
    discount_amount = sub_total * discount
    total = sub_total + tax_amount - discount_amount

    print(f"No. of Items: {len(prices)}")
    print(f"Sub Total: Rs.{sub_total:.2f}")
    print(f"Tax ({tax*100}%): Rs.{tax_amount:.2f}")
    print(f"Discount ({discount*100}%): Rs.{discount_amount:.2f}")
    print(f"Total: Rs.{total:.2f}")

    return total


# Function call
calculate_total(19.85, 12.75, 7.35, 22.45, tax=0.08, discount=0.05)