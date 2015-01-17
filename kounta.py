class Address:
    def __init__(self, obj):
        self.obj = obj

    @property
    def id(self):
        """
        Address ID.
        :rtype : integer
        """
        return self.obj['id']
