class hidy:
    def hi(self):
        self.hello()

    def hello(self):
        print("hi")

class hello(hidy):
    def hi(self):
        super().hello()

    def hello(self):
        print("hello")

if __name__ == "__main__":
    i = hidy()
    h = hello()
    i.hi()
    h.hi()