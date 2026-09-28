from app.cart import cart_total


def test_plain_total():
    assert cart_total([(5.0, 2)]) == 10.0
