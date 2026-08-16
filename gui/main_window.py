import customtkinter as ctk
from gui.dashboard_view import DashboardView
from gui.devices_view import DevicesView
from config import settings

class MainWindow(ctk.CTk):
    def __init__(self, db):
        super().__init__()
        self.db = db
        
        self.title(settings.APP_TITLE)
        self.geometry(settings.WINDOW_SIZE)
        ctk.set_appearance_mode(settings.THEME_MODE)
        ctk.set_default_color_theme(settings.THEME_COLOR)

        # Barre Latérale de Navigation
        self.sidebar = ctk.CTkFrame(self, width=160, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        
        self.logo = ctk.CTkLabel(self.sidebar, text="Enterprise ENMS", font=ctk.CTkFont(size=16, weight="bold"))
        self.logo.pack(pady=20, padx=10)
        
        # Boutons Menu
        self.btn_dash = ctk.CTkButton(self.sidebar, text="Dashboard", command=self.show_dashboard)
        self.btn_dash.pack(pady=10, padx=10)
        
        self.btn_dev = ctk.CTkButton(self.sidebar, text="Équipements", command=self.show_devices)
        self.btn_dev.pack(pady=10, padx=10)
        
        # Zone d'affichage de la vue courante
        self.container = ctk.CTkFrame(self, fg_color="transparent")
        self.container.pack(side="right", fill="both", expand=True)
        
        # Initialisation des vues modulaires
        self.view_dash = DashboardView(self.container, self.db)
        self.view_devices = DevicesView(self.container, self.db, self.view_dash.refresh_stats)
        
        # Affichage par défaut
        self.show_dashboard()

    def show_dashboard(self):
        self.view_devices.pack_forget()
        self.view_dash.pack(fill="both", expand=True)
        self.view_dash.refresh_stats()

    def show_devices(self):
        self.view_dash.pack_forget()
        self.view_devices.pack(fill="both", expand=True)
