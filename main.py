from scraper import Backend
from gui import Frontend

class App:
    def __init__(self):
        self.frontend = Frontend()

if __name__ == '__main__':
    app = App()
    app.mainloop()