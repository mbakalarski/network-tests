import logging

from snappi import Api, Config

logger = logging.getLogger("FROM_TEST")


def test_config_sent(api: Api, b2b_config: Config):
    config_to_sent_dict = b2b_config.serialize(encoding=Config.DICT)

    logger.info(f"to sent: {config_to_sent_dict}")

    api.set_config(b2b_config)

    config: Config = api.get_config()
    config_from_ixia_dict = config.serialize(encoding=Config.DICT)

    logger.info(f"read from ixia: {config_from_ixia_dict}")

    assert config_to_sent_dict == config_from_ixia_dict