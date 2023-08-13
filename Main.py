import Query as q
import ConnectionDB as db
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkinter import messagebox


def destroy_windows():
    """
    Funzione che distrugge le nuove finestre
    """
    for window in master.winfo_children():
        if isinstance(window, Toplevel):
            window.destroy()


def create_button_query(frame, first_text, second_text, command, second_command):
    """
    Funzione che crea due bottoni affiancati
    :param frame: frame per i bottoni
    :param first_text: nome del primo bottone
    :param second_text: nome del secondo bottone
    :param command: comando per il primo bottone
    :param second_command: comando per il secondo bottone
    """
    submit = Button(frame, text=first_text, command=command)
    submit.pack(side=LEFT, padx=5)
    reset = Button(frame, text=second_text, command=second_command)
    reset.pack(side=LEFT, padx=5)


def create_table_games(table_frame, height):
    """
    Funzione che crea la tabella per inserire i giochi
    :param table_frame: frame della tabella
    :param height: altezza della tabella
    :return: la tabella costruita
    """
    table = ttk.Treeview(table_frame, height=height)

    table['columns'] = ["Nome", "Piattaforma", "Data Rilascio", "Score", "Score Utenti", "Developer", "Genere",
                        "Critiche", "Utenti"]

    table.column("#0", width=0, stretch=NO)
    table.column("Nome", width=100, anchor=CENTER)
    table.column("Piattaforma", width=100, anchor=CENTER)
    table.column("Data Rilascio", width=100, anchor=CENTER)
    table.column("Score", width=100, anchor=CENTER)
    table.column("Score Utenti", width=100, anchor=CENTER)
    table.column("Developer", width=100, anchor=CENTER)
    table.column("Genere", width=100, anchor=CENTER)
    table.column("Critiche", width=100, anchor=CENTER)
    table.column("Utenti", width=100, anchor=CENTER)

    table.heading("#0", text="", anchor=CENTER)
    table.heading("Nome", text="Nome", anchor=CENTER)
    table.heading("Piattaforma", text="Piattaforma", anchor=CENTER)
    table.heading("Data Rilascio", text="Data Rilascio", anchor=CENTER)
    table.heading("Score", text="Score", anchor=CENTER)
    table.heading("Score Utenti", text="Score Utenti", anchor=CENTER)
    table.heading("Developer", text="Developer", anchor=CENTER)
    table.heading("Genere", text="Genere", anchor=CENTER)
    table.heading("Critiche", text="Critiche", anchor=CENTER)
    table.heading("Utenti", text="Utenti", anchor=CENTER)

    return table


def insert():
    """
    Comando per l'inserimento di un gioco
    """
    def query_insert():
        """
        Query di inserimento
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list]
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[2].isdigit() is False or values[3].isdigit() is False or values[4].isdigit() is False or values[5].isdigit() is False or values[6].isdigit() is False or values[9].isdigit() is False or values[10].isdigit() is False :
            messagebox.showerror("Errore", "Errore nell'inserimento dei dati")
        elif values[0].isdigit() is True or values[1].isdigit() is True or values[7].isdigit() is True or values[8].isdigit() is True:
            messagebox.showerror("Errore", "Errore nell'inserimento")
        else:
            q.insert_game(collection, values[0], values[1], int(values[2]), int(values[3]), int(values[4]), int(values[5]), int(values[6]), values[7], values[8], int(values[9]), int(values[10]))
            game = q.find_game_by_name_and_platform(collection, values[0], values[1])
            table.insert("", END, values=(game["name"], game["platform"], game["r-date"], game["score"], game["user score"], game["developer"],
                game["genre"], game["critics"], game["users"]))

    def reset():
        for entry in entry_list:
            entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Inserimento")
    insert_table = Canvas(new_master, height=350)
    insert_table.pack(side=TOP)

    labels = ["Nome", "Piattaforma", "Anno Rilascio", "Mese Rilascio", "Giorno Rilascio", "Score", "Score Utenti", "Developer", "Genere",
                "Critiche", "Utenti"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(insert_table, text=label_text, anchor=W, width=20)
        label_window = insert_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_table, width=30)
        entry_window = insert_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Inserisci", "Resetta", query_insert, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame,2)
    table.pack()


def delete_name():
    """
    Comando per la cancellazione per nome
    """
    def query_delete_name():
        """
        Query per la cancellazione per nome
        """
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            result = q.delete_game_by_name(collection, value)
            if result > 0:
                messagebox.showinfo("Successo", "Sono stati cancellati " + result + "giochi con nome " + value)
            elif result == 0:
                messagebox.showinfo("Insuccesso", "Non sono stati trovati giochi con nome " + value)

    def reset():
        for entry in entry_list:
            entry.delete(0, END)

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Cancellazione per nome")
    delete_name = Canvas(new_master, height=100)
    delete_name.pack(side=TOP)

    entry_list = []
    label = Label(delete_name, text="Nome", anchor=W, width=20)
    label_window = delete_name.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(delete_name, width=30)
    entry_window = delete_name.create_window(100, 30 + (1 * 30), anchor=W, window=entry)
    entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Elimina", "Resetta", query_delete_name, reset)


def delete_name_platform():
    """
    Comando per la cancellazione per nome e piattaforma
    """
    def query_delete_name_platform():
        """
        Query per la cancellazione per nome e piattaforma
        """
        values = [entry.get() for entry in entry_list]
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[0].isdigit() is True or values[1].isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            result = q.delete_game_by_name_and_platform(collection, values[0], values[1])
            if result == 1:
                messagebox.showinfo("Successo", "è stato cancellato il gioco " + values[0] + " per la piattaforma " + values[1])
            elif result == 0:
                messagebox.showinfo("Insuccesso", "Non è stato trovato il gioco " + values[0] + " per la piattaforma " + values[1])

    def reset():
        for entry in entry_list:
            entry.delete(0, END)

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Cancellazione per nome e piattaforma")
    delete_name_platform = Canvas(new_master, height=100)
    delete_name_platform.pack(side=TOP)

    labels = ["Nome", "Piattaforma"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(delete_name_platform, text=label_text, anchor=W, width=20)
        label_window = delete_name_platform.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(delete_name_platform, width=30)
        entry_window = delete_name_platform.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Elimina", "Resetta", query_delete_name_platform, reset)


def delete_score():
    """
    Comando per la cancellazione di giochi minori di un dato score
    """
    def query_delete_score():
        """
        Query per la cancellazione per score
        """
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is False:
            messagebox.showerror("Errore", "Devi inserire un numero.")
        else:
            result = q.delete_by_score(collection, int(value))
            if result > 0:
                messagebox.showinfo("Successo", "Sono stati cancellati " + result + "giochi con score minore di " + value)
            elif result == 0:
                messagebox.showinfo("Insuccesso", "Non sono stati trovati giochi con score minore di " + value)

    def reset():
        for entry in entry_list:
            entry.delete(0, END)

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Cancellazione per score")
    delete_score = Canvas(new_master, height=100)
    delete_score.pack(side=TOP)

    entry_list = []
    label = Label(delete_score, text="Score minori di", anchor=W, width=20)
    label_window = delete_score.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(delete_score, width=30)
    entry_window = delete_score.create_window(100, 30 + (1 * 30), anchor=W, window=entry)
    entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Elimina", "Resetta", query_delete_score, reset)


def find_name():
    """
    Comando per la ricerca di giochi per nome
    """
    def query_find_name():
        """
        Query di ricerca per nome
        """
        table.delete(*table.get_children())
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            games = q.find_game_by_name(collection, value)
            if len(games) == 0:
                messagebox.showinfo("Info", "Non sono stati trovati giochi con nome " + value)
            else:
                for x in games:
                    table.insert("", END, values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                                                  x["genre"], x["critics"], x["users"]))

    def reset():
        entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per nome")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    label = Label(insert_table, text="Nome", anchor=W, width=20)
    label_window = insert_table.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(insert_table, width=30)
    entry_window = insert_table.create_window(100, 30 + (1 * 30), anchor=W, window=entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_name, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame,10)
    table.pack()


def find_name_platform():
    """
    Comando per la ricerca di un gioco per nome e piattaforma
    """
    def query_find_name_platform():
        """
        Query di ricerca per nome e piattaforma
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list]
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[0].isdigit() is True or values[1].isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            game = q.find_game_by_name_and_platform(collection, values[0], values[1])
            if game == None:
                messagebox.showinfo("Info", "Non è stato trovato un gioco con nome " + values[0] + " per la piattaforma " + values[1])
            else:
                table.insert("", END, values=(game["name"], game["platform"], game["r-date"], game["score"], game["user score"], game["developer"],
                    game["genre"], game["critics"], game["users"]))

    def reset():
        for entry in entry_list:
            entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per nome e piattaforma")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    labels = ["Nome", "Piattaforma"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(insert_table, text=label_text, anchor=W, width=20)
        label_window = insert_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_table, width=30)
        entry_window = insert_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_name_platform, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame,2)
    table.pack()


def find_genre():
    """
    Comando per la ricerca di giochi per genere
    """
    def query_find_genre():
        """
        Query di ricerca per genere
        """
        table.delete(*table.get_children())
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            games = q.find_game_by_genre(collection, value)
            if len(games) == 0:
                messagebox.showinfo("Info", "Non sono stati trovati giochi con genere " + value)
            else:
                for x in games:
                    table.insert("", END, values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                                                x["genre"], x["critics"], x["users"]))

    def reset():
        entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per genere")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    label = Label(insert_table, text="Genere", anchor=W, width=20)
    label_window = insert_table.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(insert_table, width=30)
    entry_window = insert_table.create_window(100, 30 + (1 * 30), anchor=W, window=entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_genre, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame,10)
    table.pack()


def find_score():
    """
    Comando per la ricerca di giochi per score scelti dall'utente
    """
    def query_find_score():
        """
        Query di ricerca per score scelti dall'utente
        """
        table.delete(*table.get_children())
        selection = selection_combo.get()
        value = entry.get()
        checkbox_mag = checkbox1_var.get()
        checkbox_min = checkbox2_var.get()
        if value == "" or selection == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is False:
            messagebox.showerror("Errore", "Devi inserire un numero.")
        elif checkbox_mag == 1 and checkbox_min == 1:
            messagebox.showerror("Errore", "Puoi scegliere maggiore o minore.")
        elif checkbox_mag == 0 and checkbox_min == 0:
            messagebox.showerror("Errore", "Devi scegliere maggiore o minore.")
        else:
            if checkbox_mag == 1:
                games = q.find_games_by_score(collection, int(value), "maggiore", selection)
                for x in games:
                    table.insert("", END,values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                            x["genre"], x["critics"], x["users"]))
            if checkbox_min == 1:
                games = q.find_games_by_score(collection, int(value), "minore", selection)
                for x in games:
                    table.insert("", END, values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                            x["genre"], x["critics"], x["users"]))

    def reset():
        entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per tipi di score")

    insert_score = Canvas(new_master, height=75)
    insert_score.pack(side=TOP)

    selection_var = StringVar()
    selection_frame = ttk.Frame(insert_score, padding="10")
    selection_frame.pack()
    selection_label = ttk.Label(selection_frame, text="Tipo di score:")
    selection_label.grid(row=0, column=0, padx=5)
    selection_combo = ttk.Combobox(selection_frame, textvariable=selection_var, values=["score", "user score", "critics", "users"], state="readonly")
    selection_combo.grid(row=0, column=1, padx=5)

    entry_frame = ttk.Frame(insert_score, padding="10")
    entry_frame.pack()
    entry = ttk.Entry(entry_frame)
    entry.grid(row=0, column=1, padx=5)

    checkbox1_var = IntVar()
    checkbox1 = ttk.Checkbutton(entry_frame, text="maggiore", variable=checkbox1_var)
    checkbox1.grid(row=0, column=2, padx=5)
    checkbox2_var = IntVar()
    checkbox2 = ttk.Checkbutton(entry_frame, text="minore", variable=checkbox2_var)
    checkbox2.grid(row=0, column=3, padx=5)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_score, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame, 10)
    table.pack()


def find_developer():
    """
    Comando per la ricerca di giochi per developer
    """
    def query_find_developer():
        """
        Query di ricerca per developer
        """
        table.delete(*table.get_children())
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            games = q.find_games_by_developer(collection, value)
            if len(games) == 0:
                messagebox.showinfo("Info", "Non sono stati trovati giochi sviluppati da " + value)
            else:
                for x in games:
                    table.insert("", END,values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                                                 x["genre"], x["critics"], x["users"]))

    def reset():
        entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per developer")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    label = Label(insert_table, text="Developer", anchor=W, width=20)
    label_window = insert_table.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(insert_table, width=30)
    entry_window = insert_table.create_window(100, 30 + (1 * 30), anchor=W, window=entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_developer, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame, 10)
    table.pack()


def find_dates():
    """
    Comando per la ricerca di giochi per data
    """
    def query_find_dates():
        """
        Query di ricerca per data
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list]
        check_asc = checkbox1_var.get()
        check_dis = checkbox2_var.get()
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[0].isdigit() is False or values[1].isdigit() is False:
            messagebox.showerror("Errore", "Devi inserire un numero.")
        elif check_dis == 1 and check_asc == 1:
            messagebox.showerror("Errore", "Puoi scegliere ascendente o discendente.")
        elif check_dis == 0 and check_asc == 0:
            messagebox.showerror("Errore", "Devi scegliere ascendente o discendente.")
        else:
            if check_asc == 1:
                games = q.sort_by_dates(collection, int(values[0]), int(values[1]), "ascendente")
            if check_dis == 1:
                games = q.sort_by_dates(collection, int(values[0]), int(values[1]), "discendente")
            if len(games) == 0:
                messagebox.showinfo("Info", "Non sono stati trovati giochi usciti dal " + values[0] + " al " + values[1])
            else:
                for x in games:
                    table.insert("", END, values=(x["name"], x["platform"], x["r-date"], x["score"], x["user score"], x["developer"],
                                                x["genre"], x["critics"], x["users"]))

    def reset():
        for entry in entry_list:
            entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca per date")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    labels = ["Anno di inizio", "Anno di fine"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(insert_table, text=label_text, anchor=W, width=20)
        label_window = insert_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_table, width=30)
        entry_window = insert_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    checkbox_frame = Frame(new_master)
    checkbox_frame.pack(pady=10)
    checkbox1_var = IntVar()
    checkbox1 = ttk.Checkbutton(checkbox_frame, text="ascendente", variable=checkbox1_var)
    checkbox1.grid(row=0, column=2, padx=5)
    checkbox2_var = IntVar()
    checkbox2 = ttk.Checkbutton(checkbox_frame, text="discendente", variable=checkbox2_var)
    checkbox2.grid(row=0, column=3, padx=5)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_dates, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame, 10)
    table.pack()


def modify():
    """
    Comando per la modifica di un gioco
    """
    def query_find():
        """
        Query di ricerca del gioco da modificare
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list]
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[0].isdigit() is True or values[1].isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            game = q.find_game_by_name_and_platform(collection, values[0], values[1])
            if game == None:
                messagebox.showinfo("Info", "Non è stato trovato un gioco con nome " + values[0] + " per la piattaforma " +values[1])
            else:
                list = ["name", "platform", "r-date", "score", "user score", "developer", "genre", "critics", "users"]
                index = 0
                for val in entry_list_modify:
                    val.insert(0, game[list[index]])
                    index+=1


    def query_modify():
        """
        Query di modifica del gioco
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list_modify]
        for entry in entry_list_modify:
            entry.delete(0, END)
        search = [entry.get() for entry in entry_list]
        try:
            datetime_object = datetime.strptime(values[2], '%Y-%m-%d %H:%M:%S')
        except ValueError as ve1:
            messagebox.showerror("Errore", ve1)
            return
        if "" in values:
            messagebox.showerror("Errore", "Devi inserire tutti i valori.")
        elif values[3].isdigit() is False or values[4].isdigit() is False or values[7].isdigit() is False or values[8].isdigit() is False:
            messagebox.showerror("Errore", "Errore nell'inserimento dei dati")
        elif values[0].isdigit() is True or values[1].isdigit() is True or values[5].isdigit() is True or values[6].isdigit() is True:
            messagebox.showerror("Errore", "Errore nell'inserimento")
        else:
            q.update_game(collection, search[0], search[1], values[0], values[1], datetime_object, int(values[3]), int(values[4]), values[5], values[6], int(values[7]), int(values[8]))
            game = q.find_game_by_name_and_platform(collection, values[0], values[1])
            table.insert("", END, values=(game["name"], game["platform"], game["r-date"], game["score"], game["user score"], game["developer"],
                                          game["genre"], game["critics"], game["users"]))

    def reset():
        for entry in entry_list:
            entry.delete(0, END)
        for entry in entry_list_modify:
            entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Modifica di un gioco")
    insert_modify_table = Canvas(new_master, height=75)
    insert_modify_table.pack(side=TOP)

    labels = ["Nome", "Piattaforma"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(insert_modify_table, text=label_text, anchor=W, width=20)
        label_window = insert_modify_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_modify_table, width=30)
        entry_window = insert_modify_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find, reset)

    insert_table = Canvas(new_master, height=300)
    insert_table.pack(side=TOP)

    labels_insert = ["Nome", "Piattaforma", "Anno Rilascio", "Score", "Score Utenti","Developer", "Genere","Critiche", "Utenti"]

    entry_list_modify = []
    for i, label_text in enumerate(labels_insert):
        label = Label(insert_table, text=label_text, anchor=W, width=20)
        label_window = insert_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_table, width=30)
        entry_window = insert_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list_modify.append(entry)

    button_frame_modify = Frame(new_master)
    button_frame_modify.pack(pady=10)
    submit = Button(button_frame_modify, text="Modifica", command=query_modify)
    submit.pack(side=LEFT, padx=5)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame, 2)
    table.pack()


def average_developer():
    """
    Comando per la media di valori in base al developer
    """
    def query_average_developer():
        """
        Query di calcolo delle medie
        """
        label_result.config(text="")
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            result = q.average_by_developer(collection, value)
            if len(result) == 0:
                messagebox.showinfo("Info", "Non è stato trovato un developer con nome " + value)
            else:
                label_result.config(text=result)

    def reset():
        entry.delete(0, END)
        label_result.config(text="Risultati")

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Medie per developer")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    label = Label(insert_table, text="Developer", anchor=W, width=20)
    label_window = insert_table.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(insert_table, width=30)
    entry_window = insert_table.create_window(100, 30 + (1 * 30), anchor=W, window=entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Calcola", "Resetta", query_average_developer, reset)

    label_result = Label(new_master, text="Risultati")
    label_result.pack(pady=10, padx=5)


def average_genre():
    """
    Comando per la media di valori in base al genere
    """
    def query_average_genre():
        """
        Query di calcolo delle medie
        """
        label_result.config(text="")
        value = entry.get()
        if value == "":
            messagebox.showerror("Errore", "Nessun valore inserito.")
        elif value.isdigit() is True:
            messagebox.showerror("Errore", "Devi inserire una stringa.")
        else:
            result = q.average_by_genre(collection, value)
            if len(result) == 0:
                messagebox.showinfo("Info", "Non è stato trovato un genere con nome " + value)
            else:
                label_result.config(text=result)

    def reset():
        entry.delete(0, END)
        label_result.config(text="Risultati")

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Medie per genere")
    insert_table = Canvas(new_master, height=75)
    insert_table.pack(side=TOP)

    label = Label(insert_table, text="Genere", anchor=W, width=20)
    label_window = insert_table.create_window(10, 30 + (1 * 30), anchor=W, window=label)
    entry = Entry(insert_table, width=30)
    entry_window = insert_table.create_window(100, 30 + (1 * 30), anchor=W, window=entry)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Calcola", "Resetta", query_average_genre, reset)

    label_result = Label(new_master, text="Risultati")
    label_result.pack(pady=10, padx=5)


def find_all():
    """
    Comando per la ricerca in base a qualsiasi parametro
    """
    def query_find_all():
        """
        Query di ricerca
        """
        table.delete(*table.get_children())
        values = [entry.get() for entry in entry_list]
        check_score_mag = checkbox1_var.get()
        check_score_min = checkbox2_var.get()
        check_user_score_mag = checkbox3_var.get()
        check_user_score_min = checkbox4_var.get()
        check_critics_mag = checkbox5_var.get()
        check_critics_min = checkbox6_var.get()
        check_users_mag = checkbox7_var.get()
        check_users_min = checkbox8_var.get()

        if all(val == "" for val in values):
            messagebox.showerror("Errore", "Devi inserire almeno un dato")
        elif (values[2].isdigit() is False and values[2] != "") or (values[3].isdigit() is False and values[3] != "") or (values[4].isdigit() is False and values[4] != "") or (values[5].isdigit() is False and values[5] != "") or (values[8].isdigit() is False and values[8] != "") or (values[9].isdigit() is False and values[9] != ""):
            messagebox.showerror("Errore", "Errore nell'inserimento dei dati")
        elif values[0].isdigit() is True or values[1].isdigit() is True or values[6].isdigit() is True or values[7].isdigit() is True:
            messagebox.showerror("Errore", "Errore nell'inserimento")
        elif (check_score_mag == 1 and check_score_min == 1) or (check_user_score_mag == 1 and check_user_score_min == 1) or (check_critics_mag == 1 and check_critics_min == 1) or (check_users_mag == 1 and check_users_min == 1):
            messagebox.showerror("Errore", "Puoi scegliere maggiore, minore o nessuno, non puoi selezionarli entrambi")
        else:
            for index, val in enumerate(values):
                if index in [2, 3, 4, 5, 8, 9]:
                    if val == "":
                        values[index] = None
                    else:
                        values[index] = int(values[index])
                if val == "":
                    values[index] = None

            if check_score_mag == 1 and check_score_min == 0:
                operation_score = "maggiore"
            elif check_score_mag == 0 and check_score_min == 1:
                operation_score = "minore"
            elif check_score_mag == 0 and check_score_min == 0:
                operation_score = None

            if check_user_score_mag == 1 and check_user_score_min == 0:
                operation_user_score = "maggiore"
            elif check_user_score_mag == 0 and check_user_score_min == 1:
                operation_user_score = "minore"
            elif check_user_score_mag == 0 and check_user_score_min == 0:
                operation_user_score = None

            if check_critics_mag == 1 and check_critics_min == 0:
                operation_critics = "maggiore"
            elif check_critics_mag == 0 and check_critics_min == 1:
                operation_critics = "minore"
            elif check_critics_mag == 0 and check_critics_min == 0:
                operation_critics = None

            if check_users_mag == 1 and check_users_min == 0:
                operation_users = "maggiore"
            elif check_users_mag == 0 and check_users_min == 1:
                operation_users = "minore"
            elif check_users_mag == 0 and check_users_min == 0:
                operation_users = None

            games = q.find_by_parameters(collection, values[0], values[1], values[2], values[3], values[4], operation_score, values[5], operation_user_score, values[6], values[7], values[8], operation_critics, values[9], operation_users)
            for game in games:
                table.insert("", END, values=(game["name"], game["platform"], game["r-date"], game["score"], game["user score"], game["developer"],game["genre"], game["critics"], game["users"]))

    def reset():
        for entry in entry_list:
            entry.delete(0, END)
        table.delete(*table.get_children())

    destroy_windows()
    new_master = Toplevel(master)
    new_master.resizable(False, False)
    new_master.title("Ricerca in base ai parametri")
    insert_table = Canvas(new_master, height=350)
    insert_table.pack(side=TOP)

    labels = ["Nome", "Piattaforma", "Anno di inizio", "Anno di fine", "Score", "Score Utenti", "Developer", "Genere", "Critiche", "Utenti"]

    entry_list = []
    for i, label_text in enumerate(labels):
        label = Label(insert_table, text=label_text, anchor=W, width=20)
        label_window = insert_table.create_window(10, 30 + (i * 30), anchor=W, window=label)
        entry = Entry(insert_table, width=30)
        entry_window = insert_table.create_window(100, 30 + (i * 30), anchor=W, window=entry)
        entry_list.append(entry)

    checkbox_frame = Frame(new_master)
    checkbox_frame.pack(pady=10)
    checkbox1_var = IntVar()
    checkbox1 = ttk.Checkbutton(checkbox_frame, text="score maggiore", variable=checkbox1_var)
    checkbox1.grid(row=1, column=2, padx=5)
    checkbox2_var = IntVar()
    checkbox2 = ttk.Checkbutton(checkbox_frame, text="score minore", variable=checkbox2_var)
    checkbox2.grid(row=1, column=3, padx=5)
    checkbox3_var = IntVar()
    checkbox3 = ttk.Checkbutton(checkbox_frame, text="user score maggiore", variable=checkbox3_var)
    checkbox3.grid(row=2, column=2, padx=5)
    checkbox4_var = IntVar()
    checkbox4 = ttk.Checkbutton(checkbox_frame, text="user score minore", variable=checkbox4_var)
    checkbox4.grid(row=2, column=3, padx=5)
    checkbox5_var = IntVar()
    checkbox5 = ttk.Checkbutton(checkbox_frame, text="critics maggiore", variable=checkbox5_var)
    checkbox5.grid(row=3, column=2, padx=5)
    checkbox6_var = IntVar()
    checkbox6 = ttk.Checkbutton(checkbox_frame, text="critics minore", variable=checkbox6_var)
    checkbox6.grid(row=3, column=3, padx=5)
    checkbox7_var = IntVar()
    checkbox7 = ttk.Checkbutton(checkbox_frame, text="users maggiore", variable=checkbox7_var)
    checkbox7.grid(row=4, column=2, padx=5)
    checkbox8_var = IntVar()
    checkbox8 = ttk.Checkbutton(checkbox_frame, text="users minore", variable=checkbox8_var)
    checkbox8.grid(row=4, column=3, padx=5)

    button_frame = Frame(new_master)
    button_frame.pack(pady=10)
    create_button_query(button_frame, "Cerca", "Resetta", query_find_all, reset)

    table_canvas_insert = Canvas(new_master)
    table_canvas_insert.pack(expand=True)
    table_frame = Frame(table_canvas_insert)
    table_frame.pack()
    table = create_table_games(table_frame,10)
    table.pack()


def create_initial_button(button_list,button_frame):
    """
    Funzione per la creazione dei bottoni nel menù iniziale
    """
    list = ["Inserimento", "Cancellazione con nome", "Cancellazione con nome e platform", "Cancellazione per score",
            "Ricerca per nome", "Ricerca per nome e platform", "Ricerca per genere", "Ricerca per score", "Ricerca per developer",
            "Ricerca per data", "Modifica", "Media di score per developer", "Media score per genere", "Ricerca generale"]

    command = [insert, delete_name, delete_name_platform, delete_score, find_name, find_name_platform, find_genre, find_score,
               find_developer, find_dates, modify, average_developer, average_genre, find_all]

    for i in range(14):
        button = Button(button_frame, text=list[i], command=command[i])
        button.grid(row=i, column=0, padx=10, pady=10)
        button_list.append(button)


def start_program():
    """
    Funzione che fa partire il programma e porta l'utente al menù
    """
    canvas.destroy()
    master.geometry("1150x650")
    initial_page(collection)


def initial_page(collection):
    """
    Fuzione che crea la pagina iniziale
    """
    button_list = []
    button_frame = Frame(master)
    button_frame.pack(side=LEFT)
    create_initial_button(button_list, button_frame)

    table_canvas = Canvas(master, width=500)
    table_canvas.pack()
    table_frame = Frame(table_canvas)
    table_frame.pack()
    table = create_table_games(table_frame,70)

    for game in collection.find():
        table.insert("", END, values=(
        game["name"], game["platform"], game["r-date"], game["score"], game["user score"], game["developer"],
        game["genre"], game["critics"], game["users"]))

    table.pack()


# Creazione pagina di avvio
dbname = db.get_database()
collection = dbname["Game"]
master = Tk()
master.title("Metacritic Database")
master.geometry("350x200")
master.resizable(False, False)

# Creazione del Canvas master
canvas = Canvas(master, width=350, height=200)
canvas.pack()

label_top = canvas.create_text(175, 40, text="Progetto di Basi di Dati II", font=("Helvetica", 14))
label_bottom = canvas.create_text(175, 160, text="Sviluppato da Andrea Selice", font=("Helvetica", 10))
button = Button(master, text="Avvio", command=start_program)
button_window = canvas.create_window(175, 100, anchor=CENTER, window=button)

master.mainloop()