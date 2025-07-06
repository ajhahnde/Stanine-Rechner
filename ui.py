import tkinter as tk
from tkinter import ttk, messagebox, Toplevel
from logic import StanineTool

# Konfigurationen und Daten
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
    "ASKS": "daten/asks.json",
    #    "ADHSV": "daten/adhsv.json"  # Neu hinzugefügt
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
    "ASKS": [],
    #    "ADHSV": ["UA-V", "HY-IM-V", "GES-ADHS-V"]
}

kennwert_widgets = {}
verlauf = []


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

        ergebnis_formatiert = "\n".join(
            f"{key}: {value}" for key, value in stanines.items()
        )
        ergebnis_text.set(ergebnis_formatiert)

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
    for idx, kennwert in enumerate(aktuelle_kennwerte):
        lbl = ttk.Label(kennwerte_frame, text=f"Rohwert {kennwert}:")
        lbl.grid(row=idx, column=0, sticky="w", pady=2, padx=5)
        entry = ttk.Entry(kennwerte_frame)
        entry.grid(row=idx, column=1, sticky="ew", pady=2, padx=5)
        kennwert_widgets[kennwert] = (lbl, entry)


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
root.resizable(False, False)

main_frame = ttk.Frame(root, padding=5)
main_frame.grid(row=0, column=0, sticky="nsew")

# Fragebogen & Form
fragebogen_form_frame = ttk.LabelFrame(
    main_frame, text="", padding=10)
fragebogen_form_frame.grid(row=0, column=0, sticky="ew", pady=5)

fragebogen_var = tk.StringVar(value="ADHS")
form_var = tk.StringVar(value="FBB")
geschlecht_var = tk.StringVar(value="Mädchen")
alter_var = tk.IntVar(value=4)

ttk.Label(fragebogen_form_frame, text="Fragebogen:").grid(
    row=0, column=0, sticky="w", padx=5, pady=2)
fragebogen_dropdown = ttk.Combobox(fragebogen_form_frame, textvariable=fragebogen_var, values=list(
    kennwert_namen.keys()), state="readonly")
fragebogen_dropdown.grid(row=0, column=1, sticky="ew", padx=5, pady=2)

form_frame = ttk.Frame(fragebogen_form_frame)
form_frame.grid(row=1, column=1, sticky="w")
ttk.Label(fragebogen_form_frame, text="Form:").grid(
    row=1, column=0, sticky="w", padx=5, pady=2)
ttk.Radiobutton(form_frame, text="FBB", variable=form_var,
                value="FBB").pack(side="left", padx=5)
ttk.Radiobutton(form_frame, text="SBB", variable=form_var,
                value="SBB").pack(side="left", padx=5)

# Persönliche Daten
persoenlich_frame = ttk.LabelFrame(
    main_frame, text="", padding=10)
persoenlich_frame.grid(row=1, column=0, sticky="ew", pady=5)

ttk.Label(persoenlich_frame, text="Geschlecht:").grid(
    row=0, column=0, sticky="w", padx=5, pady=2)
geschlecht_frame = ttk.Frame(persoenlich_frame)
geschlecht_frame.grid(row=0, column=1, sticky="w")
ttk.Radiobutton(geschlecht_frame, text="Mädchen",
                variable=geschlecht_var, value="Mädchen").pack(side="left", padx=5)
ttk.Radiobutton(geschlecht_frame, text="Jungen",
                variable=geschlecht_var, value="Jungen").pack(side="left", padx=5)

ttk.Label(persoenlich_frame, text="Alter:").grid(
    row=1, column=0, sticky="w", padx=5, pady=2)
alter_spinbox = ttk.Spinbox(
    persoenlich_frame, from_=4, to=17, textvariable=alter_var, width=5)
alter_spinbox.grid(row=1, column=1, sticky="w", padx=5, pady=2)

# Kennwerte
kennwerte_frame = ttk.LabelFrame(main_frame, text="", padding=10)
kennwerte_frame.grid(row=2, column=0, sticky="ew", pady=5)

# Buttons
button_frame = ttk.Frame(main_frame)
button_frame.grid(row=3, column=0, pady=2)
ttk.Button(button_frame, text="Berechnen",
           command=berechnen).pack(side="left", padx=10)
ttk.Button(button_frame, text="Verlauf",
           command=zeige_verlauf).pack(side="left", padx=10)

# Ergebnis als LabelFrame
ergebnis_frame = ttk.LabelFrame(main_frame, text="Ergebnis", padding=10)
ergebnis_frame.grid(row=4, column=0, sticky="ew", pady=5)

ergebnis_text = tk.StringVar()
label_ergebnis = ttk.Label(
    ergebnis_frame, textvariable=ergebnis_text, justify="left")
label_ergebnis.grid(row=0, column=0, sticky="w")

fragebogen_var.trace_add("write", fragebogen_gewechselt)
fragebogen_gewechselt()

root.mainloop()
