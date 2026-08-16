from core.database import Database
from gui.main_window import MainWindow

def main():
    # Initialisation de la couche de persistance de données
    db = Database()
    
    # Lancement du composant IHM Principal
    app = MainWindow(db)
    app.mainloop()

if __name__ == "__main__":
    main()
