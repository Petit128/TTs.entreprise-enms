import customtkinter as ctk
import threading
from core.monitor import audit_node
from core.reporter import generate_markdown_report

class DevicesView(ctk.CTkFrame):
    def __init__(self, master, db, update_dash_callback):
        super().__init__(master, fg_color="transparent")
        self.db = db
        self.update_dash = update_dash_callback

        # Formulaire
        self.form = ctk.CTkFrame(self)
        self.form.pack(pady=10, fill="x", padx=10)

        self.ent_name = ctk.CTkEntry(self.form, placeholder_text="Hostname")
        self.ent_name.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.ent_ip = ctk.CTkEntry(self.form, placeholder_text="IP Address")
        self.ent_ip.pack(side="left", padx=5, pady=5, expand=True, fill="x")

        self.cmb_role = ctk.CTkOptionMenu(self.form, values=["Routeur Core", "Switch Distribution", "Serveur Web", "Firewall"])
        self.cmb_role.pack(side="left", padx=5, pady=5)

        self.btn_add = ctk.CTkButton(self.form, text="Ajouter", width=70, command=self.add_device)
        self.btn_add.pack(side="left", padx=5, pady=5)

        # Tableau Défilant
        self.scroll = ctk.CTkScrollableFrame(self, label_text="Inventaire Centralisé")
        self.scroll.pack(pady=10, fill="both", expand=True, padx=10)

        # Actions
        self.actions = ctk.CTkFrame(self, fg_color="transparent")
        self.actions.pack(pady=10, fill="x", padx=10)

        self.btn_scan = ctk.CTkButton(self.actions, text=" Scanner l'infrastructure (Asynchrone)", fg_color="#27ae60", command=self.trigger_scan)
        self.btn_scan.pack(side="left", expand=True, fill="x", padx=5)

        self.btn_report = ctk.CTkButton(self.actions, text=" Générer Rapport MD", fg_color="#2980b9", command=self.export_report)
        self.btn_report.pack(side="right", padx=5)

        self.populate_list()

    def add_device(self):
        name, ip, role = self.ent_name.get(), self.ent_ip.get(), self.cmb_role.get()
        if name and ip:
            if self.db.add_node(name, ip, role):
                self.populate_list()
                self.update_dash()

    def populate_list(self):
        for w in self.scroll.winfo_children(): 
            w.destroy()
        for n in self.db.fetch_nodes():
            row = ctk.CTkFrame(self.scroll, fg_color="transparent")
            row.pack(fill="x", pady=2)
            ctk.CTkLabel(row, text=f"{n[1]} ({n[2]}) - {n[3]}", anchor="w").pack(side="left", padx=10)
            
            color = "#2ecc71" if n[4] == "En ligne" else ("#e74c3c" if n[4] == "Hors ligne" else "orange")
            ctk.CTkLabel(row, text=n[4], text_color=color, font=ctk.CTkFont(weight="bold"), width=80).pack(side="right", padx=20)
            
            btn_del = ctk.CTkButton(row, text="X", width=25, fg_color="#c0392b", command=lambda nid=n[0]: self.delete_device(nid))
            btn_del.pack(side="right", padx=5)

    def delete_device(self, nid):
        self.db.delete_node(nid)
        self.populate_list()
        self.update_dash()

    def trigger_scan(self):
        self.btn_scan.configure(state="disabled", text="Scan global en cours...")
        threading.Thread(target=self.run_background_scan, daemon=True).start()

    def run_background_scan(self):
        nodes = self.db.fetch_nodes()
        for n in nodes:
            status, ts = audit_node(n[2])
            self.db.update_node_status(n[2], status, ts)
        self.after(0, self.finish_scan)

    def finish_scan(self):
        self.populate_list()
        self.update_dash()
        self.btn_scan.configure(state="normal", text=" Scanner l'infrastructure (Asynchrone)")

    def export_report(self):
        nodes = self.db.fetch_nodes()
        path = generate_markdown_report(nodes)
        print(f"Rapport exporté à : {path}")
