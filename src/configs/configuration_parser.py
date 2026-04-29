from configparser import ConfigParser


# TODO: in ENVIRONMENTS !!!
SECRETS_PATH = "configs/secrets.ini"
CERT_PATH = "configs/http_ca.crt"


def get_config_parser():
    configs = ConfigParser()
    configs.read(SECRETS_PATH)
    return configs