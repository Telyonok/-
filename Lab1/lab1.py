import re
import tkinter as tk
from tkinter import filedialog
from collections import defaultdict
import datetime

class WordFrequencyApp:
    def __init__(self):
        self.word_freq = None
        self.input_frame_page = 1
        self.input_frame_items_per_page = 10
        self.user_texts = {}
        self.word_desc = {}
        self.help_windows = []
        self.help_button_state = False

    def parse_text(self, filename):
        dt = datetime.datetime.now()
        with open(filename, 'r', encoding='utf-8') as file:
            text = file.read()

        words = re.findall(r'\b\w+\b', text)
        word_freq = defaultdict(int)
        for word in words:
            word_freq[word.lower()] += 1
        sorted_word_freq = dict(sorted(word_freq.items(), key=lambda x: x[0]))
        self.word_freq = sorted_word_freq
        
        print(datetime.datetime.now() - dt)

    def select_file(self):
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename()
        return filename

    def clear_input_frame_labels(self):
        for i in range(0, self.input_frame_items_per_page):
            self.input_frame_labels[i].config(text="")

    def display_input_frame_page(self):
        words_to_display = list(self.word_freq.keys())[self.input_frame_items_per_page * (self.input_frame_page - 1):self.input_frame_items_per_page * self.input_frame_page]
        self.clear_input_frame_labels()
        for i in range(len(words_to_display)):
            self.input_frame_labels[i].config(text=words_to_display[i])
            self.input_frame_labels[i].pack(anchor=tk.W)
            self.input_frame_texts[i].delete(0, tk.END)
            self.input_frame_texts[i].configure(state="normal")
            self.input_frame_texts[i].insert(0, self.word_desc.get(words_to_display[i], ""))
            self.input_frame_texts[i].pack(anchor=tk.W)

        i = len(words_to_display)
        while i < self.input_frame_items_per_page:
            self.input_frame_texts[i].configure(state="disabled")
            i += 1

    def prev_page(self):
        if self.input_frame_page > 1:
            self.input_frame_page -= 1
            self.display_input_frame_page()

    def next_page(self):
        max_page = (len(self.word_freq) - 1) // self.input_frame_items_per_page + 1
        if self.input_frame_page < max_page:
            self.input_frame_page += 1
            self.display_input_frame_page()

    def update_text_box(self):
        self.text_box.delete("1.0", tk.END)
        search_text = self.search_entry.get().lower()
        search_count = int(self.search_by_count_spinbox.get())

        for word, freq in self.word_freq.items():
            word_desc = self.word_desc.get(word, "")
            if (search_text in word.lower() or (word in self.word_desc and search_text in self.word_desc[word])) and self.word_freq[word] >= search_count:
                self.text_box.insert(tk.END, f"{word}: {freq} {word_desc}\n")

    def save_user_texts(self):
        for i in range(self.input_frame_items_per_page):
            self.word_desc[self.input_frame_labels[i].cget("text")] = self.input_frame_texts[i].get()
        self.update_text_box()

    def export_text(self):
        text = self.text_box.get("1.0", tk.END)
        for word, freq in self.word_freq.items():
            word_desc = self.word_desc.get(word, "")
            text += f"{word}: {freq} {word_desc}\n"

        default_filename = "Словарь.txt"

        save_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                    initialfile=default_filename)
        if save_filename:
            with open(save_filename, "w", encoding="utf-8") as file:
                file.write(text)
            tk.messagebox.showinfo("Экспорт успешен", "Текст экспортирован успешно.")

    def create_help_window(self, text, x, y):
        help_window = tk.Toplevel()
        help_window.geometry(f"300x200+{x}+{y}")
        help_window.title("Помощь")

        text_widget = tk.Text(help_window, width=30, height=10, wrap=tk.WORD)
        text_widget.pack(padx=10, pady=10)

        text_widget.insert(tk.END, text)
        text_widget.configure(state="disabled")

        self.help_windows.append(help_window)

    def display_help_windows(self):
        self.help_button_state = not self.help_button_state
        if self.help_button_state:
            self.create_help_window("В левой части программы находится список всех словоформ, встречающихся в тексте и их количество. Выше расположены поля для фильтрации по количеству вхождений и поиска слов.", 0, 0)
            self.create_help_window("Справа расположены подписанные поля для ввода, предназначенные для морфологической информации. Вы можете заполнить её для любых словоформ из текста. Нажимайте на '<' и '>' для переключения текущего набора слов.", 700, 0)
            self.create_help_window("Нажмите 'Сохранить', чтобы добавить введённую информацию в основной список словоформ (поле слева). Кнопка 'Экспорт' позволяет сохранить текст из основного списка (окна слева) на локальный диск.", 700, 500)
        else:
            for help_window in self.help_windows:
                help_window.destroy()

            self.help_windows = []

    def launch_app(self):
        app = tk.Tk()
        app.title("Словарь словоформ")

        text_frame = tk.Frame(app)
        text_frame.pack(side=tk.LEFT, padx=10, pady=10)
        
        text_box_frame = tk.Frame(text_frame)
        text_box_frame.pack(side=tk.TOP, padx=10, pady=10)
        
        search_label = tk.Label(text_box_frame, text="Поиск:")
        search_label.pack(side=tk.TOP)

        search_frame = tk.Frame(text_box_frame)
        search_frame.pack(side=tk.TOP, padx=10, pady=10)

        search_label = tk.Label(search_frame, text="n>=")
        search_label.pack(side=tk.LEFT)

        self.text_box = tk.Text(text_box_frame, width=30, height=30)
        self.text_box.pack(side=tk.LEFT, padx=10, pady=10)

        scroll_bar = tk.Scrollbar(text_box_frame)
        scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box.config(yscrollcommand=scroll_bar.set)
        scroll_bar.config(command=self.text_box.yview)

        self.search_by_count_spinbox = tk.Spinbox(search_frame, from_=0, to=100, width=5)
        self.search_by_count_spinbox.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(search_frame)
        self.search_entry.pack(side=tk.LEFT)

        search_button = tk.Button(search_frame, text="Найти", command=self.update_text_box)
        search_button.pack(side=tk.LEFT)

        help_button = tk.Button(app, text="Помощь", command=self.display_help_windows, width=20)
        help_button.pack(anchor=tk.W, side=tk.TOP)

        for word, freq in self.word_freq.items():
            self.text_box.insert(tk.END, f"{word}: {freq}\n")

        input_frame = tk.Frame(app)
        input_frame.pack(side=tk.RIGHT, padx=10)

        self.input_frame_labels = []
        self.input_frame_texts = []
        for _ in range(self.input_frame_items_per_page):
            self.input_frame_labels.append(tk.Label(input_frame))
            self.input_frame_texts.append(tk.Entry(input_frame))

        self.display_input_frame_page()

        save_button = tk.Button(input_frame, text="Сохранить текст", command=self.save_user_texts)
        save_button.pack(anchor=tk.W)

        prev_button = tk.Button(input_frame, text="<", command=self.prev_page)
        prev_button.pack(side=tk.LEFT)

        next_button = tk.Button(input_frame, text=">", command=self.next_page)
        next_button.pack(side=tk.LEFT)

        export_button = tk.Button(input_frame, text="Экспорт", command=self.export_text)
        export_button.pack(anchor=tk.W)

        app.mainloop()

    def start(self):
        filename = self.select_file()
        
        if filename:
            self.parse_text(filename)
            self.launch_app()

if __name__ == "__main__":
    app = WordFrequencyApp()
    app.start()