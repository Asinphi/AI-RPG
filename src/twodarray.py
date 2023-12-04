class TwoDArray:
    def __init__(self, width = 320, height = 320):
        self.array = []
        temp = []
        for i in range(height):
            for j in range(width):
                identifier = width * i + j
                temp.append(identifier)
            self.array.append(temp.copy())
            temp.clear()

    def get_array(self):
        return self.array