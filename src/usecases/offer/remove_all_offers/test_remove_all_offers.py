from unittest.mock import AsyncMock, Mock, patch

import pytest

from domain.__seedwork.test_utils import (async_return, async_side_effect,
                                          run_async)
from usecases.offer.remove_all_offers.remove_all_offers_usecase import \
    RemoveAllOffersUsecase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def remove_all_offers_usecase(offer_repository):
    return RemoveAllOffersUsecase(offer_repository)

@pytest.mark.asyncio
async def test_remove_all_offers_success(remove_all_offers_usecase, offer_repository):
    # Act
    offer_repository.remove_all_offers = async_return(None)
    # Substituindo run_async por await
    result = await remove_all_offers_usecase.execute()

    # Assert
    assert offer_repository.remove_all_offers.await_count == 1
    assert result is None
