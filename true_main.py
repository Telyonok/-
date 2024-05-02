from asyncio import sleep
from io import StringIO
import re
import os
import sys
import tkinter as tk
from tkinter import filedialog
from collections import Counter
from tkinter import scrolledtext
import xml.etree.ElementTree as ET
import pymorphy2
from natasha import (
    Segmenter,
    NewsEmbedding,
    NewsSyntaxParser,
    Doc
)
import xml
import requests
import spacy
from NLP_AI import J2ChatAI


from ruslingua import RusLingua

russian_tags = {
        'NOUN': 'Существительное',
        'ADJF': 'Прилагательное (полное)',
        'ADJS': 'Прилагательное (краткое)',
        'VERB': 'Глагол (личная форма)',
        'COMP': 'Компаратив',
        'INFN': 'Глагол(инфинитив)',
        'PRTF': 'Причастие(полное)',
        'PRTS': 'Причастие(краткое)',
        'GRND': 'Деепричастие',
        'NUMR': 'Числительное',
        'ADVB': 'Наречие',
        'NPRO': 'Местоимение',
        'PRED': 'Предикатив',
        'PREP': 'Предлог',
        'CONJ': 'Союз',
        'PRCL': 'Частица',
        'INTJ': 'Междометие',
        'Anph': 'Анафорическое местоимение',
        'Subx': 'Часть композита - первая часть слова',
        'Name': 'Имя(персональное имя или название)',
        'Surn': 'Фамилия',
        'Patr': 'Отчество',
        'Geox': 'Топоним(географическое название)',
        'Orgn': 'Организация(название)',
        'Trad': 'Зарегистрированная торговая марка, проприетарное название',
        'Apro': 'Местоимение - прилагательное(полное)',
        'Prdx': 'Предикатив или однородное именное сказуемое',
        'Coun': 'Счетная форма существительного',
        'Coll': 'Собирательное числительное',
        'Supr': 'Превосходная степень',
        'Qual': 'Качественное прилагательное',
        'Anum': 'Порядковое числительное',
        'Poss': 'Притяжательное прилагательное',
        'V - ey': 'Форма глагола на - ей(-еет, -уют)',
        'V - oy': 'Форма глагола на - ой(-оет, -уют)',
        'V - uy': 'Форма глагола на - уй(-ует, -уют)',
        'V - iy': 'Форма глагола на - ий(-ит, -ят)',
        'Sgtm': 'Одушевленное существительное(мужской род, единственное число)',
        'Pltm': 'Одушевленное существительное(мужской род, множественное число)',
        'Sgtf': 'Одушевленное существительное(женский род, единственное число)',
        'Pltf': 'Одушевленное существительное(женский род, множественное число)',
        'Sgtn': 'Одушевленное существительное(средний род, единственное число)',
        'Pltn': 'Одушевленное существительное(средний род, множественное число)',
        'Ms - f': 'мужской род(женская форма)',
        'Ms - pl': 'мужской род(множественное число)',
        'Fs - m' : 'женский род(мужская форма)',
        'Fs - pl': 'женский род(множественное число)',
        'Ns - f' : 'средний род(женская форма)',
        'Ns - pl': 'средний род(множественное число)',
        'nomn': 'именительный',
        'gent': 'родительный',
        'datv':	'дательный',
        'accs': 'винительный',
        'ablt': 'творительный',
        'loct': 'предложный',
        'voct': 'звательный',
        'gen2': 'второй родительный(частичный)',
        'acc2': 'второй винительный',
        'loc2': 'второй предложный(местный)',
        'sing': 'единственное число',
        'plur': 'множественное число',
        'masc': 'мужской род',
        'femn': 'женский род',
        'neut': 'средний род',
        'intg': 'целое число',
        'real': 'вещественное число',
        'ROMN': 'Римское число',
        'UNKN': 'Токен не удалось разобрать',
        'LATN': 'Токен состоит из латинских букв',
        'PNCT': 'Пунктуация',
        "acl:relcl": "Относительная придаточная прилагательная",
        "det": "Определитель",
        "iobj": "Косвенное дополнение",
        "discourse": "Дискурс",
        "amod": "Прилагательное-определение",
        "obl": "Обстоятельство",
        "punct": "Знак препинания",
        "nsubj:pass": "Пассивный субъект",
        "nsubj": "Субъект",
        "fixed": "Фиксированное выражение",
        "obj": "Объект",
        "nmod": "Существительное-модификатор",
        "cc": "Координационный союз",
        "case": "Падежная маркировка",
        "acl": "Пассивное прилагательное-модификатор",
        "acl": "Прилагательное-модификатор",
        "advmod": "Наречие-модификатор",
        "obl:agent": "Агент пассивной конструкции",
        "conj": "Соединительный элемент",
        "aux:pass": "Вспомогательный глагол пассива",
        "xcomp": "Открытое предложное дополнение",
        "parataxis": "Паратаксис",
        "mark": "Маркер"
    }

def convert_tags_to_russian(tags):
    current_tag = russian_tags.get(tags, tags)
    return current_tag

def translate_text(text):
    translated_text = text

    for word, translation in russian_tags.items():
        translated_text = translated_text.replace(word, translation)

    return translated_text

class WordFrequencyApp:
    def __init__(self):
        self.chat_bot = J2ChatAI()
        self.model_description = "-*- coding: utf-8 -*-Вы помощник по фильмам по имени Кенни. Вы общаетесь с пользователем на русском языке. Вы можете проконсультировать пользователя о фильмах, ответить на его вопросы, порекомендовать жанры и названия фильмов. Вы кратки, говорите по делу. При вопросе о ваших умениях - кратко расскажите о том, что вы можете советовать фильмы, угадывать фильмы и обсуждать фильмы."
        self.root = tk.Tk()
        self.root.title("Word Frequency Analyzer")
        self.text_frame = tk.Frame(self.root)
        self.text_frame.pack(fill=tk.BOTH, expand=True)

        self.text_box = tk.Text(self.text_frame, height=20, width=100)
        self.text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.text_box.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.text_box.yview)
        self.word_freq = None
        self.word_desc = {}
        self.file_paths = []
        self.search_entry = tk.Entry(self.root)
        self.morph = pymorphy2.MorphAnalyzer(lang='ru')
        self.help_windows = []
        self.file_name_dict = {}
        self.help_button_state = False

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(side=tk.RIGHT, padx=10, pady=10)

        self.chat_button = tk.Button(self.button_frame, text="Чат с помощником", command=self.chat_with_helper)
        self.chat_button.pack(side=tk.RIGHT)

        self.select_file_button = tk.Button(self.button_frame, text="Выбрать файл", command=self.select_files)
        self.select_file_button.pack(side=tk.RIGHT)

        self.export_button = tk.Button(self.button_frame, text="Сохранить", command=self.export_text)
        self.export_button.pack(side=tk.RIGHT)

        self.view_concordance_button = tk.Button(self.button_frame, text="Просмотр конкорданса", command=self.view_concordance)
        self.view_concordance_button.pack(side=tk.RIGHT)

        self.help_button = tk.Button(self.button_frame, text="Помощь", command=self.display_help_windows)
        self.help_button.pack(side=tk.RIGHT)

        self.export_xml_button = tk.Button(self.button_frame, text="Экспорт XML", command=self.export_xml)
        self.export_xml_button.pack(side=tk.RIGHT)

        self.search_label = tk.Label(self.root, text="Поиск:")
        self.search_label.pack(side=tk.TOP)

        self.search_frame = tk.Frame(self.root)
        self.search_frame.pack(side=tk.TOP, padx=10, pady=10)

        self.search_label = tk.Label(self.search_frame, text="n>=")
        self.search_label.pack(side=tk.LEFT)

        self.search_by_count_spinbox = tk.Spinbox(self.search_frame, from_=0, to=100, width=5)
        self.search_by_count_spinbox.pack(side=tk.LEFT)

        self.search_entry = tk.Entry(self.search_frame)
        self.search_entry.pack(side=tk.LEFT)

        self.search_button = tk.Button(self.search_frame, text="Найти", command=self.update_text_box)
        self.search_button.pack(side=tk.LEFT)
        
        self.close_button = tk.Button(self.root, text="Закрыть", command=self.root.quit)
        self.close_button.pack(side=tk.BOTTOM)

        self.syntax_analysis_button = tk.Button(self.button_frame, text="Синтаксический анализ", command=self.syntax_analysis)
        self.syntax_analysis_button.pack(side=tk.RIGHT)

        self.semantic_analysis_button = tk.Button(self.button_frame, text="Семантический анализ", command=self.semantic_analysis)
        self.semantic_analysis_button.pack(side=tk.RIGHT)

        self.file_listbox = tk.Listbox(self.root, height=3)
        self.file_listbox.pack(padx=10, pady=10)

    def chat_with_helper(self):
        # stuff
        self.create_chat_window()

    def syntax_analysis(self):
        segmenter = Segmenter()
        emb = NewsEmbedding()
        syntax_parser = NewsSyntaxParser(emb)

        selected_file = self.file_name_dict[self.file_listbox.get(tk.ACTIVE)]
        text = ''

        with open(selected_file, 'r', encoding='utf-8') as file:
            text = file.read()
        
        doc = Doc(text)
        doc.segment(segmenter)
        doc.parse_syntax(syntax_parser)

        self.create_syntax_window(doc)

    def semantic_analysis(self):
        selected_file = self.file_name_dict[self.file_listbox.get(tk.ACTIVE)]
        text = ''

        with open(selected_file, 'r', encoding='utf-8') as file:
            text = file.read()

        self.create_semantic_window(text)

    def get_word_definition(self, word: str):
        word = word.title()
        url = f"https://ru.wikipedia.org/api/rest_v1/page/summary/{word}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if "extract" in data:
                return data["extract"]
        return None
    
    def get_semantic_data(self, word):
        ruslingua = RusLingua()
        synonyms = ruslingua.get_synonyms(word)
        antonyms = ruslingua.get_antonyms(word)
        associations = ruslingua.get_associations(word)
        cognates = ruslingua.get_cognate_words(word)
        definitions = self.get_word_definition(word)

        return synonyms, antonyms, associations, cognates, definitions
    
    def lemmatize_sentence(self, text, word):
        nlp = spacy.load('ru_core_news_sm')
        doc = nlp(text)
        lemmas = []
        for token in doc:
            if str.lower(word) == token.lower_:
                if not token.lemma_ in lemmas:
                    lemmas.append(token.lemma_)

        return lemmas

    def create_semantic_window(self, text):
        semantic_window = tk.Toplevel()
        semantic_window.geometry("900x600")
        semantic_window.title("Семантический анализ")

        search_frame = tk.Frame(semantic_window)
        search_frame.pack(pady=10)

        search_label = tk.Label(search_frame, text="Поиск:")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT)

        text_area = scrolledtext.ScrolledText(semantic_window, width=100, height=60)
        text_area.pack(padx=10, pady=10)

        def search_sentences():
            search_text = search_entry.get().strip().lower()
            text_area.delete('1.0', tk.END)
            if (search_text != ''):
                words = self.lemmatize_sentence(text, search_text)
                for word in words:
                    synonyms, antonyms, associations, cognates, definitions = self.get_semantic_data(word)
                    text_area.insert(tk.END, f'Слово:\n {word}\n')
                    text_area.insert(tk.END, f'Синонимы:\n {synonyms}\n')
                    text_area.insert(tk.END, f'Антонимы:\n {antonyms}\n')
                    text_area.insert(tk.END, f'Когнаты:\n {cognates}\n')
                    text_area.insert(tk.END, f'Определение:\n {definitions}\n')
                    text_area.insert(tk.END, f'Ассоциации:\n {associations}\n')
                    text_area.insert(tk.END, '\n')
            else:
                text_area.insert(tk.END, text)

        search_button = tk.Button(search_frame, text="Найти", command=search_sentences)
        search_button.pack(side=tk.LEFT)

        def export_syntax():
            default_filename = "Семантический анализ.txt"
            save_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                        initialfile=default_filename)
            if save_filename:
                with open(save_filename, "w", encoding="utf-8") as file:
                    file.write(text_area.get(1.0, tk.END))
                tk.messagebox.showinfo("Экспорт успешен", "Текст экспортирован успешно.")

        export_button = tk.Button(search_frame, text="Экспорт", command=export_syntax)
        export_button.pack(side=tk.LEFT)

        search_sentences()

    def create_syntax_window(self, doc):
        syntax_window = tk.Toplevel()
        syntax_window.geometry("900x600")
        syntax_window.title("Синтаксический анализ")

        search_frame = tk.Frame(syntax_window)
        search_frame.pack(pady=10)

        search_label = tk.Label(search_frame, text="Поиск:")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT)

        text_area = scrolledtext.ScrolledText(syntax_window, width=100, height=60)
        text_area.pack(padx=10, pady=10)

        def search_sentences():
            output = StringIO()
            sys.stdout = output
            search_text = search_entry.get().strip().lower()
            text_area.delete('1.0', tk.END)

            for sentence in doc.sents:
                if search_text in sentence.text.lower():
                    sentence.syntax.print()
                    text_area.insert(tk.END, f'Предложение:\n {sentence.text}\n')
                    text_area.insert(tk.END, 'Синтаксическое дерево:\n')
                    text_area.insert(tk.END, f'{translate_text(output.getvalue())}\n')
                    text_area.insert(tk.END, '\n')
                    output.truncate(0)
                    output.seek(0) 
            sys.stdout = sys.__stdout__

        search_button = tk.Button(search_frame, text="Найти", command=search_sentences)
        search_button.pack(side=tk.LEFT)

        def export_syntax():
            default_filename = "Синтаксическое дерево.txt"
            save_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                        initialfile=default_filename)
            if save_filename:
                with open(save_filename, "w", encoding="utf-8") as file:
                    file.write(text_area.get(1.0, tk.END))
                tk.messagebox.showinfo("Экспорт успешен", "Текст экспортирован успешно.")

        export_button = tk.Button(search_frame, text="Экспорт", command=export_syntax)
        export_button.pack(side=tk.LEFT)

        search_sentences()

    def create_chat_window(self):
        self.chat_history = [{"text": "Привет, я Кенни, ваш помощник в мире фильмов. Чем могу помочь?", "role": "assistant"}]
        chat_window = tk.Toplevel()
        chat_window.geometry("900x600")
        chat_window.title("Чат с помощником")

        search_frame = tk.Frame(chat_window, padx=10, pady=10)
        search_frame.pack(fill=tk.X)

        search_label = tk.Label(search_frame, text="Поиск:")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_frame)
        search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)

        conversation_text = tk.Text(chat_window, padx=10, pady=10)
        conversation_text.pack(fill=tk.BOTH, expand=True)

        conversation_text.insert(tk.END, "AI: " + self.chat_history[0]["text"] + "\n")

        def send_message():
            conversation = conversation_text.get(1.0, tk.END)
            message = message_entry.get()
            message_entry.delete(0, tk.END)
            self.chat_history.append({"text": message, "role": "user"})
            conversation += "Вы: " + message + "\n\n"
            conversation_text.insert(tk.END, conversation)
            conversation_text.see(tk.END)

            response = self.chat_bot.make_request_to_chat(self.chat_history, self.model_description)['outputs'][0]['text']

            self.chat_history.append({"text": response, "role": "assistant"})
            conversation += "AI: " + response + "\n"
            conversation_text.delete('1.0', tk.END)
            conversation_text.insert(tk.END, conversation)
            conversation_text.see(tk.END)
            wait_label.pack_forget()

        def search_sentences():
            conversation_text.tag_remove("highlight", "1.0", tk.END)
            search_text = search_entry.get()
            if search_text:
                index = conversation_text.search(search_text, "1.0", stopindex=tk.END)
                if index:
                    conversation_text.tag_add("highlight", index, f"{index}+{len(search_text)}c")
                    conversation_text.tag_config("highlight", background="yellow")
                    conversation_text.see(index)
                else:
                    tk.messagebox.showinfo("Поиск", "Фраза не найдена.")

        search_button = tk.Button(search_frame, text="Найти", command=search_sentences)
        search_button.pack(side=tk.LEFT)

        message_entry = tk.Entry(chat_window, width=80)
        message_entry.pack(pady=10)

        send_button = tk.Button(chat_window, text="Отправить", width=20, command=send_message)
        send_button.pack(pady=10)

        wait_label = tk.Label(chat_window, text="Пожалуйста, подождите...")

        def export_syntax():
            default_filename = "Чат_лог.txt"
            save_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                        initialfile=default_filename)
            if save_filename:
                with open(save_filename, "w", encoding="utf-8") as file:
                    file.write(conversation_text.get(1.0, tk.END))
                tk.messagebox.showinfo("Экспорт успешен", "Текст экспортирован успешно.")

        export_button = tk.Button(search_frame, text="Экспорт", command=export_syntax)
        export_button.pack(side=tk.LEFT)

    def view_concordance(self):
        word = self.search_entry.get().lower()
        if word:
            file_paths = self.selected_file_paths
            concordance = {}

            for file_path in file_paths:
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    words = re.findall(r"\w+", content.lower())

                    for i in range(len(words)):
                        if words[i] == word:
                            context = " ".join(words[max(0, i - 5):i + 6])
                            if file_path in concordance:
                                concordance[file_path].append(context)
                            else:
                                concordance[file_path] = [context]

            self.update_text_box()

            for file_path, contexts in concordance.items():
                file_name = os.path.basename(file_path)
                self.text_box.insert(tk.END, f"Файл: {file_name}\n")
                self.text_box.insert(tk.END, f"Количество: {len(contexts)}\n")
                self.text_box.insert(tk.END, f"Конкордансы:\n")
                for context in contexts:
                    self.text_box.insert(tk.END, f"- {context}\n")
                self.text_box.insert(tk.END, "\n")

    def count_word_in_file(self, word, file_path):
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            content_words = re.findall(r"\w+", content.lower())
            word_count = content_words.count(word)

        self.update_text_box()

        if word in self.word_desc:
            text = f"{word}: {word_count}\n"
            text += f"Lexeme: {self.word_desc[word]['lexeme']}\n"
            text += f"Morphological Properties: {self.word_desc[word]['morphological_properties']}\n"
            self.text_box.insert(tk.END, text)

    def parse_text(self, file_paths):
        words = []
        for file_path in file_paths:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
                file_words = re.findall(r"\w+", content.lower())
                words.extend(file_words)
            self.file_listbox.insert(tk.END, os.path.basename(file_path))

        self.word_freq = Counter(words)

        for word in self.word_freq:
            parsed_word = self.morph.parse(word)[0]
            word_desc = {
                "wordform": word,
                "lexeme": parsed_word.normal_form,
                "pos": convert_tags_to_russian(parsed_word.tag.POS),
                "morphological_properties": parsed_word.tag.cyr_repr,
            }
            self.word_desc[word] = word_desc

        self.word_freq = dict(sorted(self.word_freq.items(), key=lambda item: item[1], reverse=True))
        self.update_text_box()

    def select_files(self):
        file_paths = filedialog.askopenfilenames(filetypes=[("Text Files", "*")])
        if file_paths:
            self.selected_file_paths = file_paths
            self.file_paths = file_paths
            self.parse_text(file_paths)
        for path in self.file_paths:
            self.file_name_dict[os.path.basename(path)] = path

    def update_text_box(self):
        self.text_box.delete(1.0, tk.END)
        search_text = self.search_entry.get().lower() if self.search_entry.get() else None
        search_count = int(self.search_by_count_spinbox.get())

        for word, freq in self.word_freq.items():
            word_desc = self.word_desc[word]
            if (not search_text or search_text in word or search_text in word_desc["lexeme"]) and self.word_freq[word] >= search_count:
                text = f"{word}: {freq}\n"
                text += f"  Лексема: {word_desc['lexeme']}\n"
                text += f"  Часть речи: {word_desc['pos']}\n"
                text += f"  Морфологические характеристики: {word_desc['morphological_properties']}\n"
                self.text_box.insert(tk.END, text)

    def export_text(self):
        default_filename = "Словарь.txt"
        save_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                     initialfile=default_filename)
        if save_filename:
            with open(save_filename, "w", encoding="utf-8") as file:
                file.write(self.text_box.get(1.0, tk.END))
            tk.messagebox.showinfo("Экспорт успешен", "Текст экспортирован успешно.")

    def export_xml(self):
        xml_root = ET.Element("text")

        for word, desc in self.word_desc.items():
            word_element = ET.SubElement(xml_root, "w")
            word_element.text = word
            ana_element = ET.SubElement(word_element, "ana")
            ana_element.set("lemma", desc.get("lexeme", ""))
            ana_element.set("pos", desc.get("pos", ""))
            gram = desc.get("morphological_properties")
            if gram is not None:
                gram = xml.sax.saxutils.escape(str(gram))
                ana_element.set("gram", gram)
            else:
                ana_element.set("gram", "")

        xml_tree = ET.ElementTree(xml_root)
        xml_string = ET.tostring(xml_root, encoding="windows-1251").decode("windows-1251")
        xml_string_with_newlines = xml_string.replace("><", ">\n<")
        default_filename = "Словарь.xml"
        save_filename = filedialog.asksaveasfilename(defaultextension=".xml",
                                                     initialfile=default_filename)
        if save_filename:
            with open(save_filename, "w", encoding="windows-1251") as xml_file:
                xml_file.write(xml_string_with_newlines)
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
            self.create_help_window("Программа отображает список всех словоформ, встречающихся в тексте, их количество, лексемы и их морфологические характеристики. Внизу расположены поля для фильтрации по количеству вхождений и поиска слов.", 0, 0)
            self.create_help_window("После ввода слова в поле поиска и нажатия кнопки 'Просмотр конкорданса' на экране появляется информация в виде названия файла, количесвтва слов и некоторых контекстов.", 700, 0)
            self.create_help_window("Кнопка 'Сохранить' позволяет сохранить текст из основного списка на локальный диск в формате '.txt'. Кнопка 'Экспорт в xml' позволяет сохранить текст из основного списка на локальный диск в формате '.xml' в виде морфологической разметки.", 700, 300)
            self.create_help_window("Выберите текст в списке в левом нижнем углу и нажмите на кнопку 'Синтаксический анализ', чтобы построить и просмотреть синтаксические деревья для предложений выбранного текста. В новом окне также доступна функция поиска и экспорта файла.", 0, 300)
            self.create_help_window("Выберите текст в списке в левом нижнем углу и нажмите на кнопку 'Семантический анализ', чтобы перейти в режим семантического анализа выбранного текста. В новом окне также доступна функция поиска и экспорта файла.", 0, 600)
            self.create_help_window("Также для любителей кино был добавлен интеллектуальный помощник. Нажмите на кнопку 'Чат с помощником', чтобы перейти в режим общения с помощником. В новом окне также доступна функция поиска и экспорта файла.", 700, 600)
        else:
            for help_window in self.help_windows:
                help_window.destroy()

            self.help_windows = []


    def launch_app(self):
        self.root.mainloop()

    def start(self):
        self.select_files()
        self.launch_app()

app = WordFrequencyApp()
app.start()