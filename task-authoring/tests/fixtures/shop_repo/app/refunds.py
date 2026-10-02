def process_payment(order, payment, user, flags):
    # ~300 lines in the real thing; untested
    if payment["method"] == "card":
        status = "charged"
    elif payment["method"] == "voucher":
        status = "redeemed"
    else:
        status = "pending"
    order["status"] = status
    return order
