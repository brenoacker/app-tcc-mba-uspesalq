from unittest.mock import Mock

import pytest

from src.usecases.offer.remove_all_offers.remove_all_offers_usecase import \
    RemoveAllOffersUsecase


@pytest.fixture
def offer_repository():
    return Mock()

@pytest.fixture
def remove_all_offers_usecase(offer_repository):
    return RemoveAllOffersUsecase(offer_repository)

def test_remove_all_offers_success(remove_all_offers_usecase, offer_repository):
    # Act
    offer_repository.remove_all_offers.return_value = None
    result = remove_all_offers_usecase.execute()

    # Assert
    offer_repository.remove_all_offers.assert_called_once()
    assert result is None
