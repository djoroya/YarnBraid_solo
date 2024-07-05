class classpath():

    def __init__(self, path):
        self.path = path
        self.classes = []
        self.load()
