import os
import tkinter as tk
from tkinter import messagebox
from datetime import date

from deck_analyzer import run_deck_analysis

class DeckAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("MtG Creature Type Counter")
        self.root.geometry("650x550")
        self.root.iconbitmap("assets\\creature_counter_logo.ico")

        self.download_var = tk.BooleanVar()
        self.deck_choice = tk.StringVar()

        # --- Download Section ---
        download_frame = tk.LabelFrame(root, text="Download Settings", padx=10, pady=10)
        download_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(download_frame, text="If checked, this will download the latest Scryfall data.").pack(anchor="w")
        tk.Label(download_frame, text="This may take some time and only needs to be done if your data/ folder is out of date.").pack(anchor="w")
        tk.Checkbutton(download_frame, text="Download latest Scryfall data", variable=self.download_var).pack(anchor="w", pady=5)

        # --- Deck Selection Section ---
        deck_frame = tk.LabelFrame(root, text="Deck Selection", padx=10, pady=10)
        deck_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(deck_frame, text="Choose a decklist file from the decklist/ folder:").pack(anchor="w")
        self.deck_menu = tk.OptionMenu(deck_frame, self.deck_choice, *self.get_decklist_files())
        self.deck_menu.pack(pady=5)

        tk.Button(deck_frame, text="Refresh Deck List", command=self.refresh_deck_list).pack()

        # --- Run Button ---
        run_frame = tk.Frame(root)
        run_frame.pack(pady=10)

        tk.Button(run_frame, text="Run Analysis", command=self.run_analysis, width=20).pack()

        # --- Output Display ---
        output_frame = tk.LabelFrame(root, text="Analysis Output", padx=10, pady=10)
        output_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.output_box = tk.Text(output_frame, height=15, width=75)
        self.output_box.pack(fill="both", expand=True)

    def get_decklist_files(self):
        decklist_dir = "decklist"
        if not os.path.exists(decklist_dir):
            os.makedirs(decklist_dir)
        return [f for f in os.listdir(decklist_dir) if os.path.isfile(os.path.join(decklist_dir, f))]

    def refresh_deck_list(self):
        menu = self.deck_menu["menu"]
        menu.delete(0, "end")

        new_files = self.get_decklist_files()
        if not new_files:
            self.deck_choice.set("")
            menu.add_command(label="No decks found", command=tk._setit(self.deck_choice, ""))
        else:
            self.deck_choice.set(new_files[0])
            for name in new_files:
                menu.add_command(label=name, command=tk._setit(self.deck_choice, name))

    def run_analysis(self):
        deck_name = self.deck_choice.get()
        if not deck_name:
            messagebox.showwarning("Missing Selection", "Please select a deck file.")
            return

        download_latest = self.download_var.get()

        try:
            type_data = run_deck_analysis(deck_name, download_latest)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to analyze deck:\n{str(e)}")
            return

        self.output_box.delete(1.0, tk.END)
        self.output_box.insert(tk.END, f"Deck: {deck_name}\nDate: {date.today()}\n\n")
        for td in type_data:
            self.output_box.insert(tk.END, str(td) + "\n")

if __name__ == '__main__':
    os.makedirs("decklist", exist_ok=True)
    os.makedirs("data", exist_ok=True)
    root = tk.Tk()
    app = DeckAnalyzerApp(root)
    root.mainloop()
