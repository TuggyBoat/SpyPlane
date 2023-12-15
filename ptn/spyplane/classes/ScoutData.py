class ScoutData:
    def __init__(self, info_dict=None):
        """
        Class represents a scout object as returned from the database

        entry_id, system_name, username, user_id, timestamp

        :param info_dict:
        """
        if info_dict:
            # Convert the sqlite3.Row object to a dictionary
            info_dict = dict(info_dict)

        else:
            info_dict = dict()

        self.entry_id = info_dict.get('entry_id', None)
        self.system_name = info_dict.get('system_name', None)
        self.username = info_dict.get('username', None)
        self.user_id = info_dict.get('user_id', None)
        self.timestamp = info_dict.get('timestamp', None)

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
        return 'TickData: entry_id:{0.entry_id} system_name:{0.system_name} username:{0.username} user_id:{0.user_id}' \
               'timestamp"{0.timestamp}'.format(self)

    def __bool__(self):
        """
        Override boolean to check if any values are set, if yes then return True, else False, where false is an empty
        class.

        :rtype: bool
        """
        return any([value for key, value in vars(self).items() if value])
