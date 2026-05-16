import customtkinter as ctk
from PIL import Image, ImageDraw
import backend
from tkinter import messagebox
import csv

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

def crear_imagen_placeholder(size=(100, 100), color="gray"):
    """Crea una imagen de placeholder para canes usando PIL."""
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    d.text((size[0]/4, size[1]/2-5), "Sin Imagen", fill="white")
    return img

class LoginFrame(ctk.CTkFrame):
    def __init__(self, master, login_callback):
        super().__init__(master)
        self.login_callback = login_callback
        
        lbl_title = ctk.CTkLabel(self, text="Sistema de Adopción", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=30)
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="ID Usuario")
        self.entry_user.pack(pady=10, padx=50, fill="x")
        
        self.entry_pwd = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pwd.pack(pady=10, padx=50, fill="x")
        
        btn_login = ctk.CTkButton(self, text="Entrar", command=self.validar_login)
        btn_login.pack(pady=20)
        
    def validar_login(self):
        usr = self.entry_user.get()
        pwd = self.entry_pwd.get()
        usuario_obj = backend.USUARIO.INICIO_SESION(usr, pwd)
        if usuario_obj:
            self.login_callback(usuario_obj)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

class TrabajadorDashboardFrame(ctk.CTkFrame):
    def __init__(self, master, usuario, logout_callback):
        super().__init__(master)
        self.usuario = usuario # Instancia de TRABAJADOR
        self.logout_callback = logout_callback
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=10, padx=10)
        lbl_title = ctk.CTkLabel(header, text=f"Dashboard Veterinario - {usuario.nombre}", font=("Arial", 18, "bold"))
        lbl_title.pack(side="left")
        btn_logout = ctk.CTkButton(header, text="Cerrar Sesión", command=logout_callback, width=100)
        btn_logout.pack(side="right")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.tabview.add("Gestión de Canes")
        self.tabview.add("Validar Adopción")
        self.tabview.add("Estadísticas")
        
        self._setup_gestion_canes()
        self._setup_validar_adopcion()
        self._setup_estadisticas()
        
    def _setup_gestion_canes(self):
        tab = self.tabview.tab("Gestión de Canes")
        
        form_frame = ctk.CTkFrame(tab)
        form_frame.pack(fill="x", pady=5)
        
        self.e_id = ctk.CTkEntry(form_frame, placeholder_text="ID Canino")
        self.e_id.grid(row=0, column=0, padx=5, pady=5)
        self.e_nom = ctk.CTkEntry(form_frame, placeholder_text="Nombre")
        self.e_nom.grid(row=0, column=1, padx=5, pady=5)
        self.e_ubi = ctk.CTkEntry(form_frame, placeholder_text="Ubicación Rescate")
        self.e_ubi.grid(row=0, column=2, padx=5, pady=5)
        self.e_raza = ctk.CTkEntry(form_frame, placeholder_text="Raza")
        self.e_raza.grid(row=1, column=0, padx=5, pady=5)
        self.e_edad = ctk.CTkEntry(form_frame, placeholder_text="Edad")
        self.e_edad.grid(row=1, column=1, padx=5, pady=5)
        
        self.c_estatus = ctk.CTkOptionMenu(form_frame, values=["EN TRATAMIENTO", "OBSERVACIÓN", "LISTO PARA ADOPCIÓN"])
        self.c_estatus.grid(row=1, column=2, padx=5, pady=5)
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=2, column=0, columnspan=3, pady=10)
        
        btn_add = ctk.CTkButton(btn_frame, text="Agregar/Modificar", command=self.guardar_can)
        btn_add.pack(side="left", padx=5)
        
        btn_del = ctk.CTkButton(btn_frame, text="Eliminar (Lógico)", fg_color="red", hover_color="darkred", command=self.eliminar_can)
        btn_del.pack(side="left", padx=5)
        
    def guardar_can(self):
        id_c = self.e_id.get()
        if not id_c:
            return
        can = backend.CANINO(id_c, self.e_nom.get(), self.e_ubi.get(), raza=self.e_raza.get(), edade=self.e_edad.get(), estatus=self.c_estatus.get())
        try:
            exists = False
            with open(backend.CANES_CSV, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for r in reader:
                    if r['ID_CANINO'] == id_c:
                        exists = True
                        break
            if exists:
                self.usuario.GESTIONAR_REGISTRO("MODIFICAR", can)
                messagebox.showinfo("Éxito", "Perfil modificado")
            else:
                self.usuario.GESTIONAR_REGISTRO("AGREGAR", can)
                messagebox.showinfo("Éxito", "Perfil agregado")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar_can(self):
        id_c = self.e_id.get()
        if not id_c:
            return
        can = backend.CANINO(id_c, self.e_nom.get(), self.e_ubi.get(), raza=self.e_raza.get(), edade=self.e_edad.get(), estatus=self.c_estatus.get())
        try:
            self.usuario.GESTIONAR_REGISTRO("ELIMINAR", can)
            messagebox.showinfo("Éxito", "Perfil eliminado (Borrado lógico)")
        except Exception as e:
            messagebox.showerror("Error", str(e))
            
    def _setup_validar_adopcion(self):
        tab = self.tabview.tab("Validar Adopción")
        lbl = ctk.CTkLabel(tab, text="ID de Usuario Destino:")
        lbl.pack(pady=5)
        self.e_dest = ctk.CTkEntry(tab, placeholder_text="Ej. U01")
        self.e_dest.pack(pady=5)
        
        btn_frame = ctk.CTkFrame(tab, fg_color="transparent")
        btn_frame.pack(pady=10)
        btn_apto = ctk.CTkButton(btn_frame, text="Aprobar Adopción", fg_color="green", hover_color="darkgreen", command=lambda: self.validar(True))
        btn_apto.pack(side="left", padx=5)
        btn_noapto = ctk.CTkButton(btn_frame, text="Rechazar Adopción", fg_color="red", hover_color="darkred", command=lambda: self.validar(False))
        btn_noapto.pack(side="left", padx=5)
        
    def validar(self, apto):
        id_d = self.e_dest.get()
        if not id_d:
            return
        self.usuario.VALID_ADOPCION(id_d, apto)
        messagebox.showinfo("Éxito", "Notificación enviada al usuario.")
        
    def _setup_estadisticas(self):
        tab = self.tabview.tab("Estadísticas")
        self.lbl_stats = ctk.CTkLabel(tab, text="", font=("Arial", 14), justify="left")
        self.lbl_stats.pack(pady=20, padx=20)
        
        btn_refresh = ctk.CTkButton(tab, text="Actualizar Datos", command=self.actualizar_estadisticas)
        btn_refresh.pack(pady=10)
        self.actualizar_estadisticas()
        
    def actualizar_estadisticas(self):
        stats = backend.ESTADISTICA()
        txt = stats.IMPACTO_SOCIAL() + "\n\n" + stats.REPORTE_ANALISIS()
        self.lbl_stats.configure(text=txt)

class UsuarioDashboardFrame(ctk.CTkFrame):
    def __init__(self, master, usuario, logout_callback):
        super().__init__(master)
        self.usuario = usuario # Instancia de USUARIO
        self.logout_callback = logout_callback
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", pady=10, padx=10)
        lbl_title = ctk.CTkLabel(header, text=f"Dashboard Adoptante - {usuario.nombre}", font=("Arial", 18, "bold"))
        lbl_title.pack(side="left")
        btn_logout = ctk.CTkButton(header, text="Cerrar Sesión", command=logout_callback, width=100)
        btn_logout.pack(side="right")
        
        self.tabview = ctk.CTkTabview(self)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)
        self.tabview.add("Canes Disponibles")
        self.tabview.add("Mis Reportes")
        
        self.scroll_canes = ctk.CTkScrollableFrame(self.tabview.tab("Canes Disponibles"))
        self.scroll_canes.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.frame_reportes = ctk.CTkScrollableFrame(self.tabview.tab("Mis Reportes"))
        self.frame_reportes.pack(fill="both", expand=True, padx=5, pady=5)
        
        self.cargar_canes()
        self.cargar_reportes()
        
    def cargar_canes(self):
        for widget in self.scroll_canes.winfo_children():
            widget.destroy()
        canes = self.usuario.CONSULTA_CAN()
        if not canes:
            lbl = ctk.CTkLabel(self.scroll_canes, text="No hay canes disponibles para adopción en este momento.")
            lbl.pack(pady=20)
            return
            
        for can in canes:
            card = ctk.CTkFrame(self.scroll_canes)
            card.pack(fill="x", pady=10, padx=10)
            
            pil_img = crear_imagen_placeholder((100, 100), color="#3A7EBF")
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
            lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
            lbl_img.pack(side="left", padx=10, pady=10)
            
            info = f"Nombre: {can.nombre} | Raza: {can.raza} | Edad: {can.edade}\nUbicación Rescate: {can.ubicacionr}"
            lbl_info = ctk.CTkLabel(card, text=info, justify="left", font=("Arial", 14))
            lbl_info.pack(side="left", padx=10)
            
    def cargar_reportes(self):
        for widget in self.frame_reportes.winfo_children():
            widget.destroy()
        reportes = backend.REPORTE_ADOPCION.AVANCE_SOLI(self.usuario.id_usuario)
        if not reportes:
            lbl = ctk.CTkLabel(self.frame_reportes, text="No tienes notificaciones.")
            lbl.pack(pady=20)
            return
            
        for rep in reportes:
            color = "#a3e4d7" if rep.apto_adopcion else "#f5b7b1"
            txt_color = "black"
            lbl = ctk.CTkLabel(self.frame_reportes, text=rep.mensaje, text_color=txt_color, fg_color=color, corner_radius=8, padx=10, pady=10)
            lbl.pack(fill="x", pady=5, padx=10)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Sistema de Adopción de Mascotas")
        self.geometry("800x600")
        
        # Inicializa los archivos CSV y datos semilla
        backend.inicializar_archivos()
        
        self.current_frame = None
        self.mostrar_login()
        
    def mostrar_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, self.iniciar_dashboard)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
        
    def iniciar_dashboard(self, usuario_obj):
        if self.current_frame:
            self.current_frame.destroy()
            
        if isinstance(usuario_obj, backend.TRABAJADOR):
            self.current_frame = TrabajadorDashboardFrame(self, usuario_obj, self.mostrar_login)
            self.current_frame.pack(fill="both", expand=True)
        else:
            self.current_frame = UsuarioDashboardFrame(self, usuario_obj, self.mostrar_login)
            self.current_frame.pack(fill="both", expand=True)

if __name__ == "__main__":
    app = App()
    app.mainloop()
