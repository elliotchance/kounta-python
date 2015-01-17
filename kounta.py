class Object:
    def __init__(self, obj):
        self.obj = obj

    def __getattr__(self, item):
        return self.obj[item]

class Address(Object):
    @property
    def id(self):
        """
        Address ID.
        :return: integer
        """
        return self.obj['id']

    @property
    def city(self):
        """
        City/suburb.
        :return: string
        """
        return self.obj['city']

    @property
    def lines(self):
        """
        Address lines.
        :return: string[]
        """
        return self.obj['lines']
