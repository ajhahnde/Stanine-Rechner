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

print(f"""----------------------
| Mit 'exit' beenden. |
----------------------""")

while True:
    fragebogen = input("Fragebogen: ").strip().upper()
    if fragebogen == "EXIT":
        print("Programm beendet.")
        break
    if fragebogen not in DATEIEN:
        print(f"Ungültiger Fragebogen.\n")
        continue

    tool = StanineTool(DATEIEN[fragebogen])

    form = input("Form (FBB/SBB): ").strip().upper()
    if form == "EXIT":
        print("Programm beendet.")
        break

    geschlecht_input = input("Geschlecht (Mädchen/Jungen): ").strip().lower()
    if geschlecht_input == "exit":
        print("Programm beendet.")
        break

    if geschlecht_input in ["m", "mädchen"]:
        geschlecht = "Mädchen"
    elif geschlecht_input in ["j", "jungen"]:
        geschlecht = "Jungen"
    else:
        print("Ungültige Eingabe für Geschlecht. ('mädchen', 'jungen' bzw. 'm' oder 'j' eingeben)\n")
        continue

    try:
        alter_input = input("Alter: ")
        if alter_input.lower() == "exit":
            print("Programm beendet.")
            break
        alter = int(alter_input)

        if fragebogen == "ADHS":
            kennwerte = ["UA", "HY-IM", "GES-ADHS", "K-AAR"]
        elif fragebogen == "ANG":
            kennwerte = ["TREN", "PA", "AP", "GEN", "SOZ",
                         "SPEZ", "GES-ANG", "FL-ANG", "K-KZ"]
        elif fragebogen == "DES":
            kennwerte = ["GES-DES", "K-SG"]
        elif fragebogen == "SCREEN":
            kennwerte = []
        elif fragebogen == "TIC":
            kennwerte = []
        elif fragebogen == "SSV":
            kennwerte = []
        elif fragebogen == "ZWA":
            kennwerte = []
        elif fragebogen == "TBS":
            kennwerte = []
        elif fragebogen == "BIST":
            kennwerte = []
        elif fragebogen == "ASKS":
            kennwerte = []

        rohwerte = {}
        for kw in kennwerte:
            rw_input = input(f"Rohwert {kw}: ")
            if rw_input.lower() == "exit":
                print("Programm beendet.")
                break
            rohwerte[kw] = float(rw_input)

        stanines = tool.berechne_stanine(
            fragebogen=fragebogen,
            form=form,
            geschlecht=geschlecht,
            alter=alter,
            rohwerte=rohwerte
        )

        print("Stanine-Ergebnisse:")
        for k, v in stanines.items():
            print(f"  {k}: {v}")
        print("\n--- Neue Eingabe ---\n")
    except ValueError:
        print("Ungültige Eingabe.\n")
