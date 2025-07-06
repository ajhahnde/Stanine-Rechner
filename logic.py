import json


class StanineTool:
    def __init__(self, json_path):
        with open(json_path, encoding="utf-8") as f:
            self.daten = json.load(f)
        # Definition der Altersgruppen je nach Formular
        self.altersgruppen = {
            "FBB": {
                "Mädchen": [(4, 6, "4-6"), (7, 10, "7-10"), (11, 13, "11-13"), (14, 17, "14-17")],
                "Jungen":  [(4, 6, "4-6"), (7, 10, "7-10"), (11, 13, "11-13"), (14, 17, "14-17")]
            },
            "SBB": {
                "Mädchen": [(11, 13, "11-13"), (14, 17, "14-17")],
                "Jungen":  [(11, 13, "11-13"), (14, 17, "14-17")]
            }
        }

    def finde_altersgruppe(self, form, geschlecht, alter):
        for grenze_min, grenze_max, bezeichnung in self.altersgruppen[form][geschlecht]:
            if grenze_min <= alter <= grenze_max:
                return bezeichnung
        return None

    def finde_stanine(self, rohwert, grenzen):
        for i, (low, high) in enumerate(grenzen, 1):
            # Punktintervall: low == high
            if high is not None and low == high and rohwert == low:
                return i
        # Normales Intervall: [low, high)
            if (high is None and low <= rohwert) or (low <= rohwert < high):
                return i
        return None

    def berechne_stanine(self, fragebogen, form, geschlecht, alter, rohwerte):
        gruppe = self.finde_altersgruppe(form, geschlecht, alter)
        if gruppe is None:
            raise ValueError("Keine passende Altersgruppe gefunden.")
        norm_tab = self.daten[fragebogen][form][geschlecht][gruppe]
        return {kw: self.finde_stanine(wert, norm_tab[kw]) for kw, wert in rohwerte.items()}
