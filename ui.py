import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from logic import StanineTool

DATEIEN = {
    "ADHS": "daten/adhs.json",
    "ANG": "daten/ang.json",
    "DES": "daten/des.json",
    "SCREEN": "daten/screen.json",
    "TIC": "daten/tic.json",
    "SSV": "daten/ssv.json",
    "ZWA": "daten/zwa.json",
    "TBS": "daten/tbs.json",
    "BIST": "daten/bist.json",
    "ASKS": "daten/asks.json"
}

kennwert_namen = {
    "ADHS": ["UA", "HY-IM", "GES-ADHS", "K-AAR"],
    "ANG": ["TREN", "PA", "AP", "GEN", "SOZ", "SPEZ", "GES-ANG", "FL-ANG", "K-KZ"],
    "DES": ["GES-DES", "K-SG"],
    "SCREEN": ["ADHS-SCREEN", "SSV-SCREEN", "ANG-SCREEN", "DEP-SCREEN", "ENTW-SCREEN", "AUT-SCREEN", "ZWATIC-SCREEN", "EXT-SCREEN", "INT-SCREEN", "KON-SCREEN", "GES-SCREEN"],
    "TIC": [],
    "SSV": ["OPP", "AG-DISS", "BPE", "DAF-RE", "GES-SSV", "FL-SSV", "K_PSV"],
    "ZWA": ["ZH", "ZG", "ZPS", "KD-S", "GES-ZWA", "FL-ZWA"],
    "TBS": [],
    "BIST": [],
    "ASKS": []
}

kennwert_widgets = {}  # Kennwertname → (Label, Entry)
verlauf = []  # Neue Liste für den Verlauf


def berechnen():
    try:
        fragebogen = fragebogen_var.get()
        form = form_var.get()
        geschlecht = geschlecht_var.get()
        alter = alter_var.get()

        rohwerte = {}
        for kennwert, (_, entry) in kennwert_widgets.items():
            rohwerte[kennwert] = float(entry.get())

        tool = StanineTool(DATEIEN[fragebogen])

        stanines = tool.berechne_stanine(
            fragebogen=fragebogen,
            form=form,
            geschlecht=geschlecht,
            alter=alter,
            rohwerte=rohwerte
        )

        ergebnis_text.set("Stanine-Ergebnisse:\n" + "\n".join(
            f"{key}: {value}" for key, value in stanines.items()
        ))

        # Verlauf speichern
        verlauf.append({
            "fragebogen": fragebogen,
            "form": form,
            "geschlecht": geschlecht,
            "alter": alter,
            "rohwerte": rohwerte,
            "stanines": stanines
        })
        if len(verlauf) > 10:
            verlauf.pop(0)

    except Exception as e:
        messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")


def fragebogen_gewechselt(*args):
    for widget in kennwert_widgets.values():
        widget[0].destroy()
        widget[1].destroy()
    kennwert_widgets.clear()

    aktuelle_kennwerte = kennwert_namen.get(fragebogen_var.get(), [])
    start_row = 4
    for idx, kennwert in enumerate(aktuelle_kennwerte):
        row = start_row + idx
        lbl = ttk.Label(frame, text=f"Rohwert {kennwert}:")
        lbl.grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, sticky="ew", pady=2)
        kennwert_widgets[kennwert] = (lbl, entry)

    button_berechnen.grid(
        row=row+1, column=0, columnspan=2, pady=5, sticky="ew")
    button_verlauf.grid(
        row=row+2, column=0, columnspan=2, pady=5, sticky="ew")
    label_ergebnis.grid(
        row=row+3, column=0, columnspan=3, pady=10, sticky="nsew")


def zeige_verlauf():
    if not verlauf:
        messagebox.showinfo("Verlauf", "Noch keine Berechnungen im Verlauf.")
        return

    top = Toplevel(root)
    top.title("Verlauf")
    text = tk.Text(top, width=80, height=25)
    text.pack(padx=10, pady=10)

    for i, eintrag in enumerate(verlauf, 1):
        text.insert(
            tk.END, f"{i}. {eintrag['fragebogen']} - {eintrag['form']} - {eintrag['geschlecht']} - Alter: {eintrag['alter']}\n")
        text.insert(tk.END, "   Rohwerte: " +
                    ", ".join(f"{k}={v}" for k, v in eintrag['rohwerte'].items()) + "\n")
        text.insert(tk.END, "   Stanines: " +
                    ", ".join(f"{k}={v}" for k, v in eintrag['stanines'].items()) + "\n\n")

    text.config(state="disabled")


root = tk.Tk()
root.title("Stanine-Rechner")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
for i in range(20):
    frame.rowconfigure(i, weight=1)
for j in range(3):
    frame.columnconfigure(j, weight=1)

fragebogen_var = tk.StringVar(value="ADHS")
form_var = tk.StringVar(value="FBB")
geschlecht_var = tk.StringVar(value="Mädchen")
alter_var = tk.IntVar(value=4)

button_berechnen = ttk.Button(frame, text="Berechnen", command=berechnen)
button_verlauf = ttk.Button(frame, text="Verlauf", command=zeige_verlauf)

ergebnis_text = tk.StringVar()
label_ergebnis = ttk.Label(
    frame, textvariable=ergebnis_text, wraplength=400, justify="left")

ttk.Label(frame, text="Fragebogen:").grid(row=0, column=0, sticky="w")
fragebogen_dropdown = ttk.Combobox(frame, textvariable=fragebogen_var, values=list(
    kennwert_namen.keys()), state="readonly")
fragebogen_dropdown.grid(row=0, column=1, sticky="ew")

ttk.Label(frame, text="Form:").grid(row=1, column=0, sticky="w")
form_frame = ttk.Frame(frame)
form_frame.grid(row=1, column=1, sticky="ew")
form_frame.columnconfigure(0, weight=1)
form_frame.columnconfigure(1, weight=1)
ttk.Radiobutton(form_frame, text="FBB", variable=form_var,
                value="FBB").grid(row=0, column=0, sticky="e", padx=5)
ttk.Radiobutton(form_frame, text="SBB", variable=form_var,
                value="SBB").grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(frame, text="Geschlecht:").grid(row=2, column=0, sticky="w")
geschlecht_frame = ttk.Frame(frame)
geschlecht_frame.grid(row=2, column=1, sticky="ew")
geschlecht_frame.columnconfigure(0, weight=1)
geschlecht_frame.columnconfigure(1, weight=1)
ttk.Radiobutton(geschlecht_frame, text="Mädchen", variable=geschlecht_var,
                value="Mädchen").grid(row=0, column=0, sticky="e", padx=5)
ttk.Radiobutton(geschlecht_frame, text="Jungen", variable=geschlecht_var,
                value="Jungen").grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(frame, text="Alter:").grid(row=3, column=0, sticky="w")
alter_scale = tk.Scale(frame, from_=4, to=17,
                       orient="horizontal", variable=alter_var)
alter_scale.grid(row=3, column=1, sticky="ew")

fragebogen_var.trace_add("write", fragebogen_gewechselt)
fragebogen_gewechselt()

root.mainloop()


DATEIEN = {
    "ADHS": "daten/adhs.json",
    "ANG": "daten/ang.json",
    "DES": "daten/des.json",
    "SCREEN": "daten/screen.json",
    "TIC": "daten/tic.json",
    "SSV": "daten/ssv.json",
    "ZWA": "daten/zwa.json",
    "TBS": "daten/tbs.json",
    "BIST": "daten/bist.json",
    "ASKS": "daten/asks.json"
}

kennwert_namen = {
    "ADHS": ["UA", "HY-IM", "GES-ADHS", "K-AAR"],
    "ANG": ["TREN", "PA", "AP", "GEN", "SOZ", "SPEZ", "GES-ANG", "FL-ANG", "K-KZ"],
    "DES": ["GES-DES", "K-SG"],
    "SCREEN": ["ADHS-SCREEN", "SSV-SCREEN", "ANG-SCREEN", "DEP-SCREEN", "ENTW-SCREEN", "AUT-SCREEN", "ZWATIC-SCREEN", "EXT-SCREEN", "INT-SCREEN", "KON-SCREEN", "GES-SCREEN"],
    "TIC": [],
    "SSV": [],
    "ZWA": [],
    "TBS": [],
    "BIST": [],
    "ASKS": []
}

kennwert_widgets = {}  # Kennwertname → (Label, Entry)
verlauf = []  # Neue Liste für den Verlauf


def berechnen():
    try:
        fragebogen = fragebogen_var.get()
        form = form_var.get()
        geschlecht = geschlecht_var.get()
        alter = alter_var.get()

        rohwerte = {}
        for kennwert, (_, entry) in kennwert_widgets.items():
            rohwerte[kennwert] = float(entry.get())

        tool = StanineTool(DATEIEN[fragebogen])

        stanines = tool.berechne_stanine(
            fragebogen=fragebogen,
            form=form,
            geschlecht=geschlecht,
            alter=alter,
            rohwerte=rohwerte
        )

        ergebnis_text.set("Stanine-Ergebnisse:\n" + "\n".join(
            f"{key}: {value}" for key, value in stanines.items()
        ))

        # Verlauf speichern
        verlauf.append({
            "fragebogen": fragebogen,
            "form": form,
            "geschlecht": geschlecht,
            "alter": alter,
            "rohwerte": rohwerte,
            "stanines": stanines
        })
        if len(verlauf) > 10:
            verlauf.pop(0)

    except Exception as e:
        messagebox.showerror("Fehler", f"Ungültige Eingabe: {e}")


def fragebogen_gewechselt(*args):
    for widget in kennwert_widgets.values():
        widget[0].destroy()
        widget[1].destroy()
    kennwert_widgets.clear()

    aktuelle_kennwerte = kennwert_namen.get(fragebogen_var.get(), [])
    start_row = 4
    for idx, kennwert in enumerate(aktuelle_kennwerte):
        row = start_row + idx
        lbl = ttk.Label(frame, text=f"Rohwert {kennwert}:")
        lbl.grid(row=row, column=0, sticky="w", pady=2)
        entry = ttk.Entry(frame)
        entry.grid(row=row, column=1, sticky="ew", pady=2)
        kennwert_widgets[kennwert] = (lbl, entry)

    button_berechnen.grid(
        row=row+1, column=0, columnspan=2, pady=5, sticky="ew")
    button_verlauf.grid(
        row=row+2, column=0, columnspan=2, pady=5, sticky="ew")
    label_ergebnis.grid(
        row=row+3, column=0, columnspan=3, pady=10, sticky="nsew")


def zeige_verlauf():
    if not verlauf:
        messagebox.showinfo("Verlauf", "Noch keine Berechnungen im Verlauf.")
        return

    top = Toplevel(root)
    top.title("Verlauf")
    text = tk.Text(top, width=80, height=25)
    text.pack(padx=10, pady=10)

    for i, eintrag in enumerate(verlauf, 1):
        text.insert(
            tk.END, f"{i}. {eintrag['fragebogen']} - {eintrag['form']} - {eintrag['geschlecht']} - Alter: {eintrag['alter']}\n")
        text.insert(tk.END, "   Rohwerte: " +
                    ", ".join(f"{k}={v}" for k, v in eintrag['rohwerte'].items()) + "\n")
        text.insert(tk.END, "   Stanines: " +
                    ", ".join(f"{k}={v}" for k, v in eintrag['stanines'].items()) + "\n\n")

    text.config(state="disabled")


root = tk.Tk()
root.title("Stanine-Rechner")

frame = ttk.Frame(root, padding=20)
frame.grid(row=0, column=0, sticky="nsew")

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
for i in range(20):
    frame.rowconfigure(i, weight=1)
for j in range(3):
    frame.columnconfigure(j, weight=1)

fragebogen_var = tk.StringVar(value="ADHS")
form_var = tk.StringVar(value="FBB")
geschlecht_var = tk.StringVar(value="Mädchen")
alter_var = tk.IntVar(value=4)

button_berechnen = ttk.Button(frame, text="Berechnen", command=berechnen)
button_verlauf = ttk.Button(frame, text="Verlauf", command=zeige_verlauf)

ergebnis_text = tk.StringVar()
label_ergebnis = ttk.Label(
    frame, textvariable=ergebnis_text, wraplength=400, justify="left")

ttk.Label(frame, text="Fragebogen:").grid(row=0, column=0, sticky="w")
fragebogen_dropdown = ttk.Combobox(frame, textvariable=fragebogen_var, values=list(
    kennwert_namen.keys()), state="readonly")
fragebogen_dropdown.grid(row=0, column=1, sticky="ew")

ttk.Label(frame, text="Form:").grid(row=1, column=0, sticky="w")
form_frame = ttk.Frame(frame)
form_frame.grid(row=1, column=1, sticky="ew")
form_frame.columnconfigure(0, weight=1)
form_frame.columnconfigure(1, weight=1)
ttk.Radiobutton(form_frame, text="FBB", variable=form_var,
                value="FBB").grid(row=0, column=0, sticky="e", padx=5)
ttk.Radiobutton(form_frame, text="SBB", variable=form_var,
                value="SBB").grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(frame, text="Geschlecht:").grid(row=2, column=0, sticky="w")
geschlecht_frame = ttk.Frame(frame)
geschlecht_frame.grid(row=2, column=1, sticky="ew")
geschlecht_frame.columnconfigure(0, weight=1)
geschlecht_frame.columnconfigure(1, weight=1)
ttk.Radiobutton(geschlecht_frame, text="Mädchen", variable=geschlecht_var,
                value="Mädchen").grid(row=0, column=0, sticky="e", padx=5)
ttk.Radiobutton(geschlecht_frame, text="Jungen", variable=geschlecht_var,
                value="Jungen").grid(row=0, column=1, sticky="w", padx=5)

ttk.Label(frame, text="Alter:").grid(row=3, column=0, sticky="w")
alter_scale = tk.Scale(frame, from_=4, to=17,
                       orient="horizontal", variable=alter_var)
alter_scale.grid(row=3, column=1, sticky="ew")

fragebogen_var.trace_add("write", fragebogen_gewechselt)
fragebogen_gewechselt()

root.mainloop()
