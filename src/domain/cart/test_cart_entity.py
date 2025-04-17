from uuid import UUID, uuid4

import pytest

from domain.__seedwork.test_utils import run_async
from domain.cart.cart_entity import Cart


@pytest.mark.asyncio
async def test_cart_creation():
    cart_id = uuid4()
    user_id = uuid4()
    total_price = 100.0

    cart = Cart(id=cart_id, user_id=user_id, total_price=total_price)

    assert cart.id == cart_id
    assert cart.user_id == user_id
    assert cart.total_price == total_price

@pytest.mark.asyncio
async def test_cart_invalid_id():
    user_id = uuid4()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Cart(id="invalid_uuid", user_id=user_id, total_price=total_price)
    assert str(excinfo.value) == "id must be an UUID"

@pytest.mark.asyncio
async def test_cart_invalid_user_id():
    cart_id = uuid4()
    total_price = 100.0

    with pytest.raises(Exception) as excinfo:
        Cart(id=cart_id, user_id="invalid_uuid", total_price=total_price)
    assert str(excinfo.value) == "user_id must be an UUID"

@pytest.mark.asyncio
async def test_cart_invalid_total_price():
    cart_id = uuid4()
    user_id = uuid4()

    with pytest.raises(Exception) as excinfo:
        Cart(id=cart_id, user_id=user_id, total_price=-10.0)
    assert str(excinfo.value) == "total_price must be a positive float"

    with pytest.raises(Exception) as excinfo:
        Cart(id=cart_id, user_id=user_id, total_price="invalid_price")
    assert str(excinfo.value) == "total_price must be a positive float"
