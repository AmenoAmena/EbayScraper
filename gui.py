from scraper import Backend
import customtkinter as ctk

class Frontend(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EbayScraper")
        self.geometry("800x600")

if __name__ == "__main__":
    app = Frontend()
    app.mainloop()