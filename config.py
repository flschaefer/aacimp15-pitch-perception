import ConfigParser


class Config(object):
    """

    """
    @staticmethod
    def get_config_option(option_name):
        config = ConfigParser.ConfigParser()
        config.read("config.ini")

        config_option = config.get('General', option_name)
        return config_option
