class Database:
    def __init__(self, filename):
        self.filename = filename
    
    def read(self):
        with open(self.filename, 'r') as file:
            lines = file.readlines()
            data = {}
            for line in lines:
                name, score = line.strip().split(',')
                data[name] = int(score)
            return data
    
    def write(self, data):
        with open(self.filename, 'w') as file:
            for name, score in data.items():
                file.write(f"{name},{score}\n")
