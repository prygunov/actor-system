
class BaseEntity:
    """Базовая сущность"""
    def __init__(self, onto_desc, scene=None):
        self.onto_description = onto_desc
        self.name = onto_desc.get('data', {}).get('label', {}).get('value')
        # self.uri = self.onto_description.get('uri')
        self.type = self.onto_description.get('type')
        self.uri = 'UNKNOWN_URI'
        self.scene = scene

    def get_type(self):
        return self.type