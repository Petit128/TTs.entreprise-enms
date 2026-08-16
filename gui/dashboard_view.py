import customtkinter as ctk

class DashboardView(ctk.CTkFrame):
    def __init__(self, master, db):
        super().__init__(master, fg_color="transparent")
        self.db = db
        
        self.lbl = ctk.CTkLabel(self, text=" Tableau de bord analytique", font=ctk.CTkFont(size=18, weight="bold"))
        self.lbl.pack(pady=15)

        self.stats_frame = ctk.CTkFrame(self)
        self.stats_frame.pack(pady=20, fill="x", padx=40)

        self.lbl_total = ctk.CTkLabel(self.stats_frame, text="Total équipements : 0", font=ctk.CTkFont(size=15))
        self.lbl_total.pack(pady=10)

        self.lbl_online = ctk.CTkLabel(self.stats_frame, text="En ligne : 0", text_color="#2ecc71", font=ctk.CTkFont(size=15, weight="bold"))
        self.lbl_online.pack(pady=10)

    def refresh_stats(self):
        nodes = self.db.fetch_nodes()
        total = len(nodes)
        online = sum(1 for n in nodes if n[4] == "En ligne")
        
        self.lbl_total.configure(text=f"Total équipements référencés : {total}")
        self.lbl_online.configure(text=f"Équipements opérationnels : {online} / {total}")
