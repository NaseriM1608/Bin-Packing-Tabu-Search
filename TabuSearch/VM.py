class VM:
    id = 0
    def __init__(self, Size):
        self.id = VM.id
        self.Size = Size
        self.PM = None
        VM.id += 1