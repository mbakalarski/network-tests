import pytest
from snappi import Config


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_before_configured_otg(otg01_api):
    config = otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) == 0


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_configured_otg(configured_otg01_api):
    config = configured_otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) != 0


@pytest.mark.filterwarnings("ignore:.*Unverified HTTPS request.*:")
def test_after_configured_otg(otg01_api):
    config = otg01_api.get_config().serialize(encoding=Config.DICT)
    assert len(config) == 0
