import csv
import os
from datetime import datetime
import uuid

# Archivos CSV
USUARIOS_CSV = 'usuarios.csv'
CANES_CSV = 'canes.csv'
REPORTES_CSV = 'reportes.csv'

def inicializar_archivos():
    """
    Crea los archivos CSV requeridos si no existen y añade datos base.
    """
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_USUARIO', 'NOMBRE', 'CONTACTO', 'CONTRASENA', 'ROL', 'PUESTO'])
            writer.writerow(['T01', 'Dr. Pepe Vet', '2225556677|pepe@clinic.com', '123', 'TRABAJADOR', 'Veterinario'])
            writer.writerow(['U01', 'Kino', '2221113344|kino@mail.com', '456', 'USUARIO', 'N/A'])
            
    if not os.path.exists(CANES_CSV):
        with open(CANES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_CANINO', 'NOMBRE', 'UBICACIONR', 'FECHAI', 'RAZA', 'EDADE', 'ESTATUS', 'HISTORIAL', 'DIAGNOSTICO', 'TRATAMIENTO', 'VACUNAS'])
            
    if not os.path.exists(REPORTES_CSV):
        with open(REPORTES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_REPORTE', 'ID_DESTINO', 'MENSAJE', 'APTO_ADOPCION'])


class CANINO:
    def __init__(self, id_canino, nombre, ubicacionr, fechai=None, raza="Mestizo", edade="", estatus="EN TRATAMIENTO"):
        self.id_canino = id_canino
        self.nombre = nombre
        self.ubicacionr = ubicacionr
        self.fechai = fechai if fechai else datetime.now().strftime("%Y-%m-%d %H:%M")
        self.raza = raza
        self.edade = edade
        self.estatus = estatus

    def REG_CANINO(self):
        """Guarda un nuevo registro en canes.csv."""
        with open(CANES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_canino, self.nombre, self.ubicacionr, self.fechai, self.raza, self.edade, self.estatus, "N/A", "N/A", "N/A", "N/A"])

    def ACTU_PERFIL(self):
        """Modifica los datos del can en canes.csv."""
        filas = []
        with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            filas = list(reader)
        
        with open(CANES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for fila in filas:
                if fila and fila[0] == self.id_canino:
                    fila[1] = self.nombre
                    fila[2] = self.ubicacionr
                    fila[3] = self.fechai
                    fila[4] = self.raza
                    fila[5] = self.edade
                    fila[6] = self.estatus
                writer.writerow(fila)

    def DEL_PERFIL(self):
        """Elimina de forma lógica el registro en canes.csv (cambia estatus a ELIMINADO)."""
        self.estatus = "ELIMINADO"
        self.ACTU_PERFIL()


class EXPEDIENTE_MEDICO(CANINO):
    def __init__(self, id_canino, nombre, ubicacionr, fechai=None, raza="Mestizo", edade="", estatus="EN TRATAMIENTO", historial="", diagnostico="", tratamiento="", vacunas=""):
        super().__init__(id_canino, nombre, ubicacionr, fechai, raza, edade, estatus)
        self.historial = historial
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.vacunas = vacunas

    def NUEVA_CONSULTA(self, notas):
        """Agrega un bloque de texto con fecha actual al historial médico y actualiza el CSV."""
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        if self.historial == "N/A" or self.historial.strip() == "":
            self.historial = f"[{fecha_actual}] {notas}"
        else:
            self.historial += f" | [{fecha_actual}] {notas}"
        self._actualizar_csv()

    def EDITAR_CONSULTA(self, diagnostico, tratamiento, vacunas):
        """Permite modificar el diagnóstico, tratamiento y vacunas vigentes."""
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.vacunas = vacunas
        self._actualizar_csv()

    def _actualizar_csv(self):
        """Método interno para sobreescribir el archivo completo de canes actualizando los campos médicos."""
        filas = []
        with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            filas = list(reader)
        
        with open(CANES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for fila in filas:
                if fila and fila[0] == self.id_canino:
                    fila[1] = self.nombre
                    fila[2] = self.ubicacionr
                    fila[3] = self.fechai
                    fila[4] = self.raza
                    fila[5] = self.edade
                    fila[6] = self.estatus
                    # Campos de expediente
                    fila[7] = self.historial
                    fila[8] = self.diagnostico
                    fila[9] = self.tratamiento
                    fila[10] = self.vacunas
                writer.writerow(fila)
        
    def REG_CANINO(self):
        """Override para guardar todos los campos incluyendo los del expediente."""
        with open(CANES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_canino, self.nombre, self.ubicacionr, self.fechai, self.raza, self.edade, self.estatus, self.historial, self.diagnostico, self.tratamiento, self.vacunas])


class USUARIO:
    def __init__(self, id_usuario, nombre, contacto, contrasena):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contacto = contacto
        self.contrasena = contrasena

    def REG_USUARIO(self):
        """Registra un nuevo perfil de adoptante en usuarios.csv."""
        with open(USUARIOS_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_usuario, self.nombre, self.contacto, self.contrasena, 'USUARIO', 'N/A'])

    @staticmethod
    def INICIO_SESION(id_usuario, contrasena):
        """Valida credenciales en usuarios.csv y retorna la instancia correcta según su Rol."""
        with open(USUARIOS_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_USUARIO'] == id_usuario and row['CONTRASENA'] == contrasena:
                    if row['ROL'] == 'TRABAJADOR':
                        return TRABAJADOR(row['ID_USUARIO'], row['NOMBRE'], row['CONTACTO'], row['CONTRASENA'], row['PUESTO'])
                    else:
                        return USUARIO(row['ID_USUARIO'], row['NOMBRE'], row['CONTACTO'], row['CONTRASENA'])
        return None

    def CONSULTA_CAN(self):
        """Retorna únicamente los canes cuyo ESTATUS sea 'LISTO PARA ADOPCIÓN'."""
        canes_listos = []
        with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ESTATUS'] == "LISTO PARA ADOPCIÓN":
                    can = EXPEDIENTE_MEDICO(
                        row['ID_CANINO'], row['NOMBRE'], row['UBICACIONR'], row['FECHAI'], 
                        row['RAZA'], row['EDADE'], row['ESTATUS'], 
                        row['HISTORIAL'], row['DIAGNOSTICO'], row['TRATAMIENTO'], row['VACUNAS']
                    )
                    canes_listos.append(can)
        return canes_listos


class TRABAJADOR(USUARIO):
    def __init__(self, id_usuario, nombre, contacto, contrasena, puesto):
        super().__init__(id_usuario, nombre, contacto, contrasena)
        self.puesto = puesto

    def GESTIONAR_REGISTRO(self, operacion, can_obj):
        """Permite agregar, modificar o eliminar registros de canes."""
        if operacion == "AGREGAR":
            can_obj.REG_CANINO()
        elif operacion == "MODIFICAR":
            if isinstance(can_obj, EXPEDIENTE_MEDICO):
                can_obj._actualizar_csv()
            else:
                can_obj.ACTU_PERFIL()
        elif operacion == "ELIMINAR":
            can_obj.DEL_PERFIL()

    def VALID_ADOPCION(self, id_destino, apto):
        """Genera una resolución (Apto / No Apto) para una solicitud de adopción."""
        id_reporte = "REP-" + str(uuid.uuid4())[:8]
        msg = "Su solicitud de adopción ha sido APROBADA." if apto else "Su solicitud de adopción ha sido RECHAZADA."
        reporte = REPORTE_ADOPCION(id_reporte, id_destino, msg, apto)
        reporte.ENVIAR_NOTI()

    def ACT_ESTATUSC(self, can_obj, nuevo_estatus):
        """Cambia rápidamente el estatus médico/adopción de un can."""
        can_obj.estatus = nuevo_estatus
        if isinstance(can_obj, EXPEDIENTE_MEDICO):
            can_obj._actualizar_csv()
        else:
            can_obj.ACTU_PERFIL()


class REPORTE_ADOPCION:
    def __init__(self, id_reporte, id_destino, mensaje, apto_adopcion):
        self.id_reporte = id_reporte
        self.id_destino = id_destino
        self.mensaje = mensaje
        self.apto_adopcion = apto_adopcion

    def ENVIAR_NOTI(self):
        """Guarda la notificación en reportes.csv."""
        with open(REPORTES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_reporte, self.id_destino, self.mensaje, str(self.apto_adopcion)])

    @staticmethod
    def AVANCE_SOLI(id_usuario):
        """Filtra y devuelve los reportes pertenecientes a un ID_USUARIO específico."""
        reportes_usuario = []
        if os.path.exists(REPORTES_CSV):
            with open(REPORTES_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['ID_DESTINO'] == id_usuario:
                        apto = row['APTO_ADOPCION'] == 'True'
                        r = REPORTE_ADOPCION(row['ID_REPORTE'], row['ID_DESTINO'], row['MENSAJE'], apto)
                        reportes_usuario.append(r)
        return reportes_usuario


class ESTADISTICA:
    def __init__(self):
        self.usuariost = 0
        self.canest = 0
        self.canes_rescatados = 0
        self._cargar_datos()

    def _cargar_datos(self):
        if os.path.exists(USUARIOS_CSV):
            with open(USUARIOS_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader = list(csv.DictReader(f))
                self.usuariost = sum(1 for r in reader if r['ROL'] == 'USUARIO')
                
        if os.path.exists(CANES_CSV):
            with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader = list(csv.DictReader(f))
                self.canes_rescatados = len([r for r in reader if r['ESTATUS'] != 'ELIMINADO'])
                self.canest = len([r for r in reader if r['ESTATUS'] == 'LISTO PARA ADOPCIÓN'])

    def IMPACTO_SOCIAL(self):
        """Retorna una cadena resumiendo el impacto del refugio."""
        return f"Usuarios: {self.usuariost} | Rescatados Históricamente: {self.canes_rescatados} | Listos para adopción: {self.canest}"

    def REPORTE_ANALISIS(self):
        """Procesa los datos y calcula el porcentaje de canes rehabilitados frente al total de rescatados."""
        if self.canes_rescatados == 0:
            return "No hay canes registrados para calcular el impacto."
        
        porcentaje = (self.canest / self.canes_rescatados) * 100
        return f"Porcentaje de canes rehabilitados (listos para adopción) frente al total rescatado activo: {porcentaje:.2f}%"
