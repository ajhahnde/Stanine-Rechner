import json
from logic import StanineTool

with open("adhs.json", encoding="utf-8") as f:
    daten = json.load(f)

print(daten.keys())

# Nutzung/Test
tool = StanineTool("adhs.json")
stanines = tool.berechne_stanine(
    fragebogen="ADHS",
    form="FBB",
    geschlecht="Mädchen",
    alter=9,
    rohwerte={"UA": 0.45, "HY-IM": 0.2}
)
print(stanines)

with open("adhs.json", encoding="utf-8") as f:
    daten = json.load(f)

for fragebogen in daten:
    for form in daten[fragebogen]:
        for geschlecht in daten[fragebogen][form]:
            for altersgruppe in daten[fragebogen][form][geschlecht]:
                print(f"{fragebogen} / {form} / {geschlecht} / {altersgruppe}")
