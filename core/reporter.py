import os
from datetime import datetime

def generate_markdown_report(nodes, filename="reports/rapport_infrastructure.md"):
    "Génère un rapport d'audit au format Markdown"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    total = len(nodes)
    online = sum(1 for n in nodes if n[4] == "En ligne")
    offline = total - online
    
    content = f"""# 📊 Rapport d'Audit Infrastructure Réseau
Généré automatiquement le : {datetime.now().strftime('%Y-%m-%d à %H:%M:%S')}

## 📈 Statistiques Globales
- **Total équipements référencés** : {total}
- **Équipements opérationnels (En ligne)** : {online}
- **Équipements en panne (Hors ligne)** : {offline}

## 🖥️ État détaillé du parc informatique

| Nom d'hôte | Adresse IP | Rôle Système | Statut Actuel | Dernier Scan Réussi |
| :--- | :--- | :--- | :--- | :--- |
"""
    for n in nodes:
        content += f"| {n[1]} | {n[2]} | {n[3]} | {n[4]} | {n[5]} |\n"
        
    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(filename)
