class UDelegate:
    def __init__(self):
        self.handlers = []

    def AddHandler(self, handler):
        self.handlers.append(handler)

    def Broadcast(self, *args, **kwargs):
        for handler in self.handlers:
            handler(*args, **kwargs)