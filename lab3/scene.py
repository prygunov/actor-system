from collections import defaultdict

class Scene:
    """
    Класс сцены
    """
    def __init__(self):
        self.entities = defaultdict(list)