from scraper import Backend
import customtkinter as ctk

class Frontend(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("EbayScraper")
        self.geometry("800x600")

        self.create_widgets()

    def create_widgets(self):
        self.product_name = ctk.CTkEntry(self, placeholder_text="Product Name: ")
        self.product_name.pack(pady=20)

        self.file_name = ctk.CTkEntry(self, placeholder_text="File name: ")
        self.file_name.pack(pady=20)

        self.options = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
        self.option_menu = ctk.CTkOptionMenu(self, values=self.options)
        self.option_menu.pack(pady=20)

        self.button = ctk.CTkButton(self, text="Search", command=self.grab_values)
        self.button.pack(pady=20)

    def grab_values(self):
        
        self.product_name = self.product_name.get()
        self.page_number = self.option_menu.get()
        self.file_name = self.file_name.get()

        self.scraping()        

    def scraping(self):
        self.scraper = Backend()
        self.scraper.scrape(self.product_name,self.page_number)
        self.scraper.save_to_csv(self.file_name)
        self.scraper.quit_driver()


app = Frontend()
app.mainloop()