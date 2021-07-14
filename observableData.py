

class ObservableData:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def notify_changes(self, data):
        pass
