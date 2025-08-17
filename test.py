class ContextManager:
    def __init__(self, filename, method):
        self.filename = filename
        self.method = method
        self.file = None

    def __enter__(self):
        self.file = open(self.filename, self.method)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
    

with ContextManager('filename.txt', 'w') as f:
    f.write('Hello, world!')