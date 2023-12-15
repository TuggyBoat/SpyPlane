class ConfigData:
    def __init__(self, info_dict=None):
        """
        Clas represents a config object as returned from the database

        config_setting, config_value

        :param info_dict:
        """
        if info_dict:
            # Convert the sqlite3.Row object to a dictionary
            info_dict = dict(info_dict)

        else:
            info_dict = dict()

        self.config_setting = info_dict.get('config_setting', None)
        self.config_value = info_dict.get('config_value', None)

    def to_dictionary(self):
        """
        Formats the config data into a dictionary for easy access

        :returns: A dictionary representation for the config data
        :rtype: dict
        """
        response = {}
        for key, value in vars(self).items():
            if value is not None:
                response[key] = value
        return response

    def __str__(self):
        """
        Overloads str to return a readable object

        :rtype: str
        """
        return 'ConfigData: config_setting:{0.config_setting} config_value:{0.config_value}'.format(self)

    def __bool__(self):
        """
        Override boolean to check if any values are set, if yes then return True, else False, where false is an empty
        class.

        :rtype: bool
        """
        return any([value for key, value in vars(self).items() if value])
