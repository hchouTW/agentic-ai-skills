def cart_total(items, discount_code=None):
    total = sum(price * qty for price, qty in items)
    if discount_code == "TENOFF":
        total -= 10
    if discount_code and discount_code.endswith("PCT"):
        total = total * (1 - int(discount_code[:-3]) / 100)
    return round(total, 2)
