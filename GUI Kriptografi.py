import tkinter
import tkinter.messagebox
import customtkinter
import numpy as np
from Kriptografi import enkripsi, deskripsi, corelation_value, encryption_quality

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("A Criptography Algorithm Using Quantum Wavelet S-Transform")
        self.geometry(f"{1100}x{610}")

        # configure grid layout
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((1, 2), weight=1)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=10)
        self.sidebar_frame.grid(row=0, column=0, rowspan=5, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(5, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Menu", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, text="Input Data", command=self.sidebar_button_1_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, text="Enkripsi", command=self.sidebar_button_2_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, text="Deskripsi", command=self.sidebar_button_3_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.sidebar_button_4 = customtkinter.CTkButton(self.sidebar_frame, text="Reset", command=self.sidebar_button_4_event)
        self.sidebar_button_4.grid(row=4, column=0, padx=20, pady=10)
        self.sidebar_button_5 = customtkinter.CTkButton(self.sidebar_frame, text="Save", command=self.sidebar_button_5_event)
        self.sidebar_button_5.grid(row=5, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=6, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=7, column=0, padx=20, pady=(10, 10))

        # create mid frame
        self.mid_frame = customtkinter.CTkFrame(self, width=340, corner_radius=10)
        self.mid_frame.grid(row=0, column=1, rowspan=13, padx=(10,5), sticky="nsew")
        self.mid_frame.grid_rowconfigure(0, weight=0)
        self.mid_frame.grid_columnconfigure(1, weight=1)
        self.label_plain = customtkinter.CTkLabel(self.mid_frame, text="Plain Text", font=customtkinter.CTkFont(size=13, weight="bold"), justify="left")
        self.label_plain.grid(row=0, column=1, padx=20, pady=(10, 10))
        self.textbox_plain = customtkinter.CTkTextbox(self.mid_frame)
        self.textbox_plain.grid(row=1, column=1, padx=(10, 10), pady=(0, 0), sticky="nsew")
        self.textbox_plain.insert("0.0", "")
        self.label_char1 = customtkinter.CTkLabel(self.mid_frame, text="Panjang Karakter", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char1.grid(row=2, column=1, padx=20, pady=(10, 0))
        self.entry1 = customtkinter.CTkEntry(self.mid_frame)
        self.entry1.grid(row=3, column=1, padx=10, sticky="nsew")
        self.label_char2 = customtkinter.CTkLabel(self.mid_frame, text="Kunci Enkripsi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char2.grid(row=4, column=1, padx=20)
        self.entry2 = customtkinter.CTkEntry(self.mid_frame)
        self.entry2.grid(row=5, column=1, padx=10, sticky="nsew")
        self.label_char3 = customtkinter.CTkLabel(self.mid_frame, text="Waktu Enkripsi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char3.grid(row=6, column=1, padx=20)
        self.entry3 = customtkinter.CTkEntry(self.mid_frame)
        self.entry3.grid(row=7, column=1, padx=10, sticky="nsew")
        self.label_char4 = customtkinter.CTkLabel(self.mid_frame, text="Nilai Korelasi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char4.grid(row=8, column=1, padx=20)
        self.entry4 = customtkinter.CTkEntry(self.mid_frame)
        self.entry4.grid(row=9, column=1, padx=10, sticky="nsew")
        self.label_char5 = customtkinter.CTkLabel(self.mid_frame, text="Kualitas Enkripsi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char5.grid(row=10, column=1, padx=20)
        self.entry5 = customtkinter.CTkEntry(self.mid_frame)
        self.entry5.grid(row=11, column=1, padx=10, sticky="nsew")
        self.label_char6 = customtkinter.CTkLabel(self.mid_frame, text="Persentase Kualitas Enkripsi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char6.grid(row=12, column=1, padx=20)
        self.entry6 = customtkinter.CTkEntry(self.mid_frame)
        self.entry6.grid(row=13, column=1, padx=10, sticky="nsew")

        # create end frame
        self.end_frame = customtkinter.CTkFrame(self, width=340, corner_radius=10)
        self.end_frame.grid(row=0, column=2, rowspan=5, padx=(5,10), sticky="nsew")
        self.end_frame.grid_rowconfigure(0, weight=0)
        self.end_frame.grid_columnconfigure(2, weight=1)
        self.label_chip = customtkinter.CTkLabel(self.end_frame, text="Chiper Text", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_chip.grid(row=0, column=2, padx=20, pady=(10, 10))
        self.textbox_chip = customtkinter.CTkTextbox(self.end_frame)
        self.textbox_chip.grid(row=1, column=2, padx=(10, 10), pady=(0, 0), sticky="nsew")
        self.textbox_chip.insert("0.0", "")
        self.label_char_1 = customtkinter.CTkLabel(self.end_frame, text="Panjang Karakter", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_1.grid(row=2, column=2, padx=20, pady=(10, 0))
        self.entry_1 = customtkinter.CTkEntry(self.end_frame)
        self.entry_1.grid(row=3, column=2, padx=10, sticky="nsew")
        self.label_char_2 = customtkinter.CTkLabel(self.end_frame, text="Kunci Deskripsi 1", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_2.grid(row=4, column=2, padx=20)
        self.entry_2 = customtkinter.CTkEntry(self.end_frame)
        self.entry_2.grid(row=5, column=2, padx=10, sticky="nsew")
        self.label_char_3 = customtkinter.CTkLabel(self.end_frame, text="Kunci Deskripsi 2", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_3.grid(row=6, column=2, padx=20)
        self.entry_3 = customtkinter.CTkEntry(self.end_frame)
        self.entry_3.grid(row=7, column=2, padx=10, sticky="nsew")
        self.label_char_6 = customtkinter.CTkLabel(self.end_frame, text="Kunci Deskripsi 3", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_6.grid(row=8, column=2, padx=20)
        self.entry_6 = customtkinter.CTkEntry(self.end_frame)
        self.entry_6.grid(row=9, column=2, padx=10, sticky="nsew")
        self.label_char_4 = customtkinter.CTkLabel(self.end_frame, text="Waktu Deskripsi", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_4.grid(row=10, column=2, padx=20)
        self.entry_4 = customtkinter.CTkEntry(self.end_frame)
        self.entry_4.grid(row=11, column=2, padx=10, sticky="nsew")
        self.label_char_5 = customtkinter.CTkLabel(self.end_frame, text="Similarity", font=customtkinter.CTkFont(size=11, weight="bold"))
        self.label_char_5.grid(row=12, column=2, padx=20)
        self.entry_5 = customtkinter.CTkEntry(self.end_frame)
        self.entry_5.grid(row=13, column=2, padx=10, sticky="nsew")

         # create end frame
        self.ended_frame = customtkinter.CTkFrame(self, width=340, corner_radius=10)
        self.ended_frame.grid(row=0, column=3, rowspan=5, padx=(5,10), sticky="nsew")
        self.ended_frame.grid_rowconfigure(0, weight=0)
        self.ended_frame.grid_columnconfigure(2, weight=1)
        self.label_invchip = customtkinter.CTkLabel(self.ended_frame, text="Plain Text", font=customtkinter.CTkFont(size=13, weight="bold"))
        self.label_invchip.grid(row=0, column=3, padx=20, pady=(10, 10))
        self.textbox_invchip = customtkinter.CTkTextbox(self.ended_frame)
        self.textbox_invchip.grid(row=1, column=3, padx=(10, 10), pady=(0, 0), sticky="nsew")
        self.textbox_invchip.insert("0.0", "")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def sidebar_button_1_event(self):
        file_path = tkinter.filedialog.askopenfilename()
        if file_path:
            with open(file_path, 'r') as file:
                data = file.read()
                self.textbox_plain.delete("1.0", "end")
                self.textbox_plain.insert("1.0", data)
                self.entry1.delete(0, "end")
                self.entry1.insert(0, str(len(data)))

    def sidebar_button_2_event(self):
        if not self.textbox_plain.get("1.0", "end-1c").strip() or not self.entry2.get().strip():
            tkinter.messagebox.showwarning("Peringatan", "Plain Text dan Kunci Enkripsi tidak boleh kosong")
            return
        bit_precision = 4 
        bit_precision += 2
        PlainText = self.textbox_plain.get("1.0", "end-1c")
        key_input = self.entry2.get()
        Key = [int(k) for k in key_input.split(',')]
        ChiperText, Key3, Key2, te = enkripsi(PlainText, Key, bit_precision)
        self.textbox_chip.delete("1.0", "end")
        self.textbox_chip.insert("1.0", ChiperText)
        self.entry3.delete(0, "end")
        self.entry3.insert(0, te)
        self.entry_1.delete(0, "end")
        self.entry_1.insert(0, str(len(ChiperText)))
        self.entry_2.delete(0, "end")
        self.entry_2.insert(0, ', '.join(map(str, Key)))
        self.entry_3.delete(0, "end")
        self.entry_3.insert(0, ', '.join(map(str, Key2)))
        self.entry_6.delete(0, "end")
        self.entry_6.insert(0, ', '.join(map(str, Key3)))
        correlation_value = corelation_value(PlainText, ChiperText)
        self.entry4.delete(0, "end")
        self.entry4.insert(0, correlation_value)
        max_quality_enk, persent_quality_enk = encryption_quality(PlainText, ChiperText)
        self.entry5.delete(0, "end")
        self.entry5.insert(0, max_quality_enk)
        self.entry6.delete(0, "end")
        self.entry6.insert(0, persent_quality_enk)

    def sidebar_button_3_event(self):
        bit_precision = 4
        bit_precision += 2
        SignalOri = np.array([ord(char) for char in self.textbox_plain.get("1.0", "end-1c")]) 
        ChiperText = self.textbox_chip.get("1.0", "end-1c")
        Key2 = [int(k) for k in self.entry_3.get().split(',')]
        Key = [int(k) for k in self.entry_2.get().split(',')]
        invChipperText, td = deskripsi(ChiperText, Key2, Key, bit_precision, SignalOri)
        self.textbox_invchip.insert("1.0",  invChipperText)
        self.entry_4.insert(0, td)

    def sidebar_button_4_event(self):
        self.textbox_plain.delete("1.0", "end")
        self.textbox_chip.delete("1.0", "end")
        self.entry1.delete(0, "end")
        self.entry2.delete(0, "end")
        self.entry3.delete(0, "end")
        self.entry4.delete(0, "end")
        self.entry5.delete(0, "end")
        self.entry6.delete(0, "end")
        self.entry_1.delete(0, "end")
        self.entry_2.delete(0, "end")
        self.entry_3.delete(0, "end")
        self.entry_4.delete(0, "end")
        self.entry_5.delete(0, "end")

    def sidebar_button_5_event(self):
        file_path = tkinter.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, 'w') as file:
                file.write("Plain Text:\n" + self.textbox_plain.get("1.0", "end-1c") + "\n")
                file.write("Chiper Text:\n" + self.textbox_chip.get("1.0", "end-1c") + "\n")
                file.write("Kunci Enkripsi:\n" + self.entry2.get() + "\n")
                file.write("Kunci Deskripsi 1:\n" + self.entry_2.get() + "\n")
                file.write("Kunci Deskripsi 2:\n" + self.entry_3.get() + "\n")


if __name__ == "__main__":
    app = App()
    app.mainloop()
