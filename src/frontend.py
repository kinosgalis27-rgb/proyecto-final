import customtkinter as ctk
from PIL import Image, ImageDraw
import backend
from tkinter import messagebox, filedialog
import csv
import os


ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# Funcion que genera una imagen por defecto en caso de que un canino no tenga fotografia asignada
def crear_imagen_placeholder(size=(100, 100), color="gray"):
    img = Image.new('RGB', size, color=color)
    d = ImageDraw.Draw(img)
    d.text((size[0]/4, size[1]/2-5), "Sin Imagen", fill="white")
    return img

# Clase que construye y maneja la ventana inicial de inicio de sesion
class LoginFrame(ctk.CTkFrame):
    # Metodo constructor que inicia los elementos graficos para capturar credenciales
    def __init__(self, master, login_callback, registro_callback): 
        super().__init__(master)
        self.login_callback = login_callback
        self.registro_callback = registro_callback 
        
        lbl_title = ctk.CTkLabel(self, text="Sistema de Adopción", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=30)
        
        self.entry_user = ctk.CTkEntry(self, placeholder_text="ID Usuario")
        self.entry_user.pack(pady=10, padx=50, fill="x")
        
        self.entry_pwd = ctk.CTkEntry(self, placeholder_text="Contraseña", show="*")
        self.entry_pwd.pack(pady=10, padx=50, fill="x")
        
        btn_login = ctk.CTkButton(self, text="Entrar", command=self.validar_login)
        btn_login.pack(pady=(20, 10))
        btn_registro = ctk.CTkButton(self, text="Crear Cuenta (Adoptante)", fg_color="gray", command=self.registro_callback)
        btn_registro.pack(pady=10)
        
    # Metodo que verifica el identificador y la contrasea contra el backend para que pueda ingresar
    def validar_login(self):
        usr = self.entry_user.get()
        pwd = self.entry_pwd.get()
        usuario_obj = backend.USUARIO.INICIO_SESION(usr, pwd)
        if usuario_obj:
            self.login_callback(usuario_obj)
        else:
            messagebox.showerror("Error", "Credenciales incorrectas")

# Clase que define la interfaz principal y herramientas para los usuarios veterinarios o trabajadores
class TrabajadorDashboardFrame(ctk.CTkFrame):
    # Metodo constructor que divide la pantalla en diferentes pestañas de gestion
    def __init__(self, master, usuario, logout_callback):
        super().__init__(master)
        self.usuario = usuario 
        self.logout_callback = logout_callback
        self.ruta_imagen_seleccionada = ""
        
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
        
    # Metodo interno que crea el formulario para dar de alta modificar o dar de baja perros
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

        btn_foto = ctk.CTkButton(form_frame, text="Subir Foto", command=self.seleccionar_foto, fg_color="#17a2b8", hover_color="#138496")
        btn_foto.grid(row=2, column=1, pady=10)
        self.lbl_foto_ruta = ctk.CTkLabel(form_frame, text="Sin foto seleccionada", text_color="gray", font=("Arial", 10))
        self.lbl_foto_ruta.grid(row=3, column=1)
        
        btn_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        btn_frame.grid(row=4, column=0, columnspan=3, pady=10)
        
        btn_add = ctk.CTkButton(btn_frame, text="Agregar/Modificar", command=self.guardar_can)
        btn_add.pack(side="left", padx=5)
        
        btn_del = ctk.CTkButton(btn_frame, text="Eliminar (Lógico)", fg_color="red", hover_color="darkred", command=self.eliminar_can)
        btn_del.pack(side="left", padx=5)

    # Metodo que abre un explorador de archivos para elegir y guardar la ruta de una foto
    def seleccionar_foto(self):
        ruta = filedialog.askopenfilename(title="Seleccionar foto del canino", filetypes=[("Imágenes", "*.png *.jpg *.jpeg")])
        if ruta:
            self.ruta_imagen_seleccionada = ruta
            nombre_archivo = os.path.basename(ruta)
            self.lbl_foto_ruta.configure(text=f"Foto: {nombre_archivo}", text_color="green")
        
    # Metodo que lee el formulario y determina si debe agregar un perro nuevo o actualizar uno existente
    def guardar_can(self):
        id_c = self.e_id.get()
        if not id_c:
            return
        can = backend.CANINO(id_c, self.e_nom.get(), self.e_ubi.get(), raza=self.e_raza.get(), edade=self.e_edad.get(), estatus=self.c_estatus.get(), ruta_imagen=self.ruta_imagen_seleccionada)
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
            self.ruta_imagen_seleccionada = ""
            self.lbl_foto_ruta.configure(text="Sin foto seleccionada", text_color="gray")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # Metodo que toma el id del formulario y marca al perro como eliminado 
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

    # Metodo interno que empiez el espacio donde se listaran las peticiones de adopcion
    def _setup_validar_adopcion(self):
        tab = self.tabview.tab("Validar Adopción")
        self.scroll_solicitudes = ctk.CTkScrollableFrame(tab)
        self.scroll_solicitudes.pack(fill="both", expand=True, padx=5, pady=5)
        self.cargar_solicitudes()

    # Metodo que extrae las solicitudes pendientes del backend y genera las tarjetas con opciones de aprobacion
    def cargar_solicitudes(self):
        for widget in self.scroll_solicitudes.winfo_children():
            widget.destroy()
        solicitudes = self.usuario.OBTENER_SOLICITUDES()
        if not solicitudes:
            lbl = ctk.CTkLabel(self.scroll_solicitudes, text="No hay solicitudes pendientes.")
            lbl.pack(pady=20)
            return
        for sol in solicitudes:
            card = ctk.CTkFrame(self.scroll_solicitudes)
            card.pack(fill="x", pady=5, padx=5)
            txt = f"Usuario: {sol['ID_USUARIO']} | Canino: {sol['ID_CANINO']}"
            lbl = ctk.CTkLabel(card, text=txt, font=("Arial", 14))
            lbl.pack(side="left", padx=10, pady=10)
            btn_rechazar = ctk.CTkButton(card, text="Rechazar", fg_color="red", hover_color="darkred", width=80, command=lambda s=sol: self.procesar_solicitud(s, False))
            btn_rechazar.pack(side="right", padx=5, pady=10)
            btn_aceptar = ctk.CTkButton(card, text="Aceptar", fg_color="green", hover_color="darkgreen", width=80, command=lambda s=sol: self.procesar_solicitud(s, True))
            btn_aceptar.pack(side="right", padx=5, pady=10)

    # Metodo que envia la decision tomada sobre una solicitud al backend para notificar al usuario que adopta
    def procesar_solicitud(self, sol, apto):
        self.usuario.VALID_ADOPCION(sol['ID_SOLICITUD'], sol['ID_USUARIO'], sol['ID_CANINO'], apto)
        messagebox.showinfo("Éxito", "Solicitud procesada.")
        self.cargar_solicitudes()
        
    # Metodo interno que crea la seccion para ver las metricas de la organizacion
    def _setup_estadisticas(self):
        tab = self.tabview.tab("Estadísticas")
        self.lbl_stats = ctk.CTkLabel(tab, text="", font=("Arial", 14), justify="left")
        self.lbl_stats.pack(pady=20, padx=20)
        
        btn_refresh = ctk.CTkButton(tab, text="Actualizar Datos", command=self.actualizar_estadisticas)
        btn_refresh.pack(pady=10)
        self.actualizar_estadisticas()
        
    # Metodo que pide al backend los ultimos calculos estadisticos y los muestra en la pantalla
    def actualizar_estadisticas(self):
        stats = backend.ESTADISTICA()
        txt = stats.IMPACTO_SOCIAL() + "\n\n" + stats.REPORTE_ANALISIS()
        self.lbl_stats.configure(text=txt)

# Clase que define la vista principal para que los usuarios normales interactuen con el catalogo
class UsuarioDashboardFrame(ctk.CTkFrame):
    # Metodo constructor que organiza la vista en catalogo de animales e historial de reportes
    def __init__(self, master, usuario, logout_callback):
        super().__init__(master)
        self.usuario = usuario 
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
        
    # Metodo que lee el catalogo de perros aptos y mete graficamente sus fotos y datos
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
            
            try:
                if can.ruta_imagen and os.path.exists(can.ruta_imagen):
                    pil_img = Image.open(can.ruta_imagen).resize((100, 100))
                else:
                    pil_img = crear_imagen_placeholder((100, 100), color="#3A7EBF")
            except Exception:
                pil_img = crear_imagen_placeholder((100, 100), color="#3A7EBF")

            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(100, 100))
            lbl_img = ctk.CTkLabel(card, image=ctk_img, text="")
            lbl_img.pack(side="left", padx=10, pady=10)
            
            info = f"ID Canino: {can.id_canino} | Nombre: {can.nombre} | Raza: {can.raza} | Edad: {can.edade}\nUbicación Rescate: {can.ubicacionr}"
            lbl_info = ctk.CTkLabel(card, text=info, justify="left", font=("Arial", 14))
            lbl_info.pack(side="left", padx=10)
            
            btn_adoptar = ctk.CTkButton(card, text="Solicitar Adopción", fg_color="#28a745", hover_color="#218838", command=lambda c=can: self.solicitar_adopcion(c))
            btn_adoptar.pack(side="right", padx=20)

    # Metodo que manda la creacion de una peticion formal uniendo al usuario actual con el perro elegido
    def solicitar_adopcion(self, can):
        self.usuario.SOLICITAR_ADOPCION(can.id_canino)
        mensaje = f"¡Excelente decisión!\n\nHas iniciado el proceso para adoptar a {can.nombre}.\n\nTu solicitud ha sido enviada al veterinario para su revisión."
        messagebox.showinfo("Proceso de Adopción Iniciado", mensaje)
            
    # Metodo que busca las resoluciones enviadas por los veterinarios y las pinta en la seccion de notificaciones
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

# Clase que presenta los campos necesarios para inscribir a una nueva persona en el registro
class RegistroUsuarioFrame(ctk.CTkFrame):
    # Metodo constructor que posiciona cajas de texto y botones 
    def __init__(self, master, volver_callback):
        super().__init__(master)
        self.volver_callback = volver_callback
        
        lbl_title = ctk.CTkLabel(self, text="Registro de Adoptante", font=("Arial", 24, "bold"))
        lbl_title.pack(pady=30)
        
        self.entry_nom = ctk.CTkEntry(self, placeholder_text="Nombre Completo")
        self.entry_nom.pack(pady=10, padx=50, fill="x")
        
        self.entry_cont = ctk.CTkEntry(self, placeholder_text="Contacto (Teléfono o Correo)")
        self.entry_cont.pack(pady=10, padx=50, fill="x")
        
        self.entry_pwd = ctk.CTkEntry(self, placeholder_text="Crea una Contraseña", show="*")
        self.entry_pwd.pack(pady=10, padx=50, fill="x")
        
        btn_guardar = ctk.CTkButton(self, text="Registrarme", command=self.guardar_nuevo_usuario)
        btn_guardar.pack(pady=(20, 10))
        
        btn_volver = ctk.CTkButton(self, text="Volver al Inicio", fg_color="gray", command=self.volver_callback)
        btn_volver.pack(pady=10)

    # Metodo que valida que no existan campos vacios genera una clave unica y contempla la informacion
    def guardar_nuevo_usuario(self):
        import uuid
        nom = self.entry_nom.get()
        cont = self.entry_cont.get()
        pwd = self.entry_pwd.get()

        if not nom or not cont or not pwd:
            messagebox.showwarning("Faltan datos", "Por favor, llena todos los campos.")
            return
        id_usr = "U-" + str(uuid.uuid4().int)[:4]

        nuevo_usuario = backend.USUARIO(id_usr, nom, cont, pwd)
        try:
            nuevo_usuario.REG_USUARIO()
            messagebox.showinfo("Éxito", f"¡Cuenta creada!\nTu ID para iniciar sesión es: {id_usr}")
            self.volver_callback() 
        except Exception as e:
            messagebox.showerror("Error", str(e))

# Clase raiz del programa que hereda de la ventana principal de customtkinter
class App(ctk.CTk):
    # Metodo constructor que configura dimensiones iniciales y arranca 
    def __init__(self):
        super().__init__()
        self.title("Sistema de Adopción de Mascotas")
        self.geometry("800x600")
        
        backend.inicializar_archivos()
        
        self.current_frame = None
        self.mostrar_login()
        
    # Metodo controlador que destruye el contenedor que est activo y dibuja la pantalla de inicio de sesion
    def mostrar_login(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = LoginFrame(self, self.iniciar_dashboard, self.mostrar_registro)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")

    # Metodo controlador que despliega el formulario para crear nuevas cuentas
    def mostrar_registro(self):
        if self.current_frame:
            self.current_frame.destroy()
        self.current_frame = RegistroUsuarioFrame(self, self.mostrar_login)
        self.current_frame.place(relx=0.5, rely=0.5, anchor="center")
        
    # Metodo controlador que verifica el nivel de permisos del usuario y despues lo redirige a su panel
    def iniciar_dashboard(self, usuario_obj):
        if self.current_frame:
            self.current_frame.destroy()
            
        if isinstance(usuario_obj, backend.TRABAJADOR):
            self.current_frame = TrabajadorDashboardFrame(self, usuario_obj, self.mostrar_login)
            self.current_frame.pack(fill="both", expand=True)
        else:
            self.current_frame = UsuarioDashboardFrame(self, usuario_obj, self.mostrar_login)
            self.current_frame.pack(fill="both", expand=True)

# Bloque de ejecucion principal que inicia el bucle de elementos gráficos
if __name__ == "__main__":
    app = App()
    app.mainloop()