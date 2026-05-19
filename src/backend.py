# Importacion de modulos necesarios para el manejo de archivos fechas y generacion de identificadores unicos
import csv
import os
from datetime import datetime
import uuid

# Definicion de las rutas absolutas para los archivos de texto que almacenan la informacion
BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')
USUARIOS_CSV = os.path.join(BASE_DIR, 'usuarios.csv')
CANES_CSV = os.path.join(BASE_DIR, 'canes.csv')
REPORTES_CSV = os.path.join(BASE_DIR, 'reportes.csv')
SOLICITUDES_CSV = os.path.join(BASE_DIR, 'solicitudes.csv')

# Funcion encargada de crear los archivos base y sus encabezados si estos no existen en el sistema
def inicializar_archivos():
    if not os.path.exists(USUARIOS_CSV):
        with open(USUARIOS_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_USUARIO', 'NOMBRE', 'CONTACTO', 'CONTRASENA', 'ROL', 'PUESTO'])
            writer.writerow(['T01', 'Dr. Pepe Vet', '2225556677|pepe@clinic.com', '123', 'TRABAJADOR', 'Veterinario'])
            writer.writerow(['U01', 'Kino', '2221113344|kino@mail.com', '456', 'USUARIO', 'N/A'])
    if not os.path.exists(CANES_CSV):
        with open(CANES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_CANINO', 'NOMBRE', 'UBICACIONR', 'FECHAI', 'RAZA', 'EDADE', 'ESTATUS', 'HISTORIAL', 'DIAGNOSTICO', 'TRATAMIENTO', 'VACUNAS', 'RUTA_IMAGEN'])
    if not os.path.exists(REPORTES_CSV):
        with open(REPORTES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_REPORTE', 'ID_DESTINO', 'MENSAJE', 'APTO_ADOPCION'])
    if not os.path.exists(SOLICITUDES_CSV):
        with open(SOLICITUDES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['ID_SOLICITUD', 'ID_USUARIO', 'ID_CANINO', 'ESTADO'])

# Clase principal que representa el perfil basico de un perro rescatado
class CANINO:
    # Metodo constructor para inicializar los atributos de identificacion y estado del perro
    def __init__(self, id_canino, nombre, ubicacionr, fechai=None, raza="Mestizo", edade="", estatus="EN TRATAMIENTO", ruta_imagen=""):
        self.id_canino = id_canino
        self.nombre = nombre
        self.ubicacionr = ubicacionr
        self.fechai = fechai if fechai else datetime.now().strftime("%Y-%m-%d %H:%M")
        self.raza = raza
        self.edade = edade
        self.estatus = estatus
        self.ruta_imagen = ruta_imagen

    # Metodo para guardar un nuevo registro del perro en el archivo correspondiente
    def REG_CANINO(self):
        with open(CANES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_canino, self.nombre, self.ubicacionr, self.fechai, self.raza, self.edade, self.estatus, "N/A", "N/A", "N/A", "N/A", self.ruta_imagen])

    # Metodo para buscar al perro por su identificador y sobrescribir sus datos actualizados
    def ACTU_PERFIL(self):
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
                    if len(fila) > 11:
                        fila[11] = self.ruta_imagen
                    else:
                        fila.append(self.ruta_imagen)
                writer.writerow(fila)

    # Metodo que cambia el estado del perro a eliminado y actualiza el archivo
    def DEL_PERFIL(self):
        self.estatus = "ELIMINADO"
        self.ACTU_PERFIL()

# Clase derivada de CANINO que incorpora la informacion clinica del animal
class EXPEDIENTE_MEDICO(CANINO):
    # Metodo constructor que hereda propiedades basicas y añade datos medicos
    def __init__(self, id_canino, nombre, ubicacionr, fechai=None, raza="Mestizo", edade="", estatus="EN TRATAMIENTO", historial="", diagnostico="", tratamiento="", vacunas="", ruta_imagen=""):
        super().__init__(id_canino, nombre, ubicacionr, fechai, raza, edade, estatus, ruta_imagen)
        self.historial = historial
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.vacunas = vacunas

    # Metodo para registrar una nueva entrada en el historial del animal con fecha actual
    def NUEVA_CONSULTA(self, notas):
        fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M")
        if self.historial == "N/A" or self.historial.strip() == "":
            self.historial = f"[{fecha_actual}] {notas}"
        else:
            self.historial += f" | [{fecha_actual}] {notas}"
        self._actualizar_csv()

    # Metodo para modificar los campos especificos de salud del expediente
    def EDITAR_CONSULTA(self, diagnostico, tratamiento, vacunas):
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento
        self.vacunas = vacunas
        self._actualizar_csv()

    # Metodo interno auxiliar que reescribe el archivo con los datos medicos mas recientes
    def _actualizar_csv(self):
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
                    fila[7] = self.historial
                    fila[8] = self.diagnostico
                    fila[9] = self.tratamiento
                    fila[10] = self.vacunas
                    if len(fila) > 11:
                        fila[11] = self.ruta_imagen
                    else:
                        fila.append(self.ruta_imagen)
                writer.writerow(fila)

    # Metodo que sobrescribe el registro basico para incluir todos los campos del expediente clinico
    def REG_CANINO(self):
        with open(CANES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_canino, self.nombre, self.ubicacionr, self.fechai, self.raza, self.edade, self.estatus, self.historial, self.diagnostico, self.tratamiento, self.vacunas, self.ruta_imagen])

# Clase base para definir a los usuarios de la plataforma
class USUARIO:
    # Metodo constructor que define las credenciales y datos de contacto de una persona
    def __init__(self, id_usuario, nombre, contacto, contrasena):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self.contacto = contacto
        self.contrasena = contrasena

    # Metodo para inscribir un nuevo usuario normal en el sistema
    def REG_USUARIO(self):
        with open(USUARIOS_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_usuario, self.nombre, self.contacto, self.contrasena, 'USUARIO', 'N/A'])

    # Metodo estatico que valida credenciales y retorna un objeto de tipo usuario o trabajador segun el rol
    @staticmethod
    def INICIO_SESION(id_usuario, contrasena):
        with open(USUARIOS_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ID_USUARIO'] == id_usuario and row['CONTRASENA'] == contrasena:
                    if row['ROL'] == 'TRABAJADOR':
                        return TRABAJADOR(row['ID_USUARIO'], row['NOMBRE'], row['CONTACTO'], row['CONTRASENA'], row['PUESTO'])
                    else:
                        return USUARIO(row['ID_USUARIO'], row['NOMBRE'], row['CONTACTO'], row['CONTRASENA'])
        return None

    # Metodo que lee el archivo de animales y devuelve una lista unicamente con los que estan habilitados para adoptar
    def CONSULTA_CAN(self):
        canes_listos = []
        with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row['ESTATUS'] == "LISTO PARA ADOPCIÓN":
                    ruta = row.get('RUTA_IMAGEN', '')
                    can = EXPEDIENTE_MEDICO(
                        row['ID_CANINO'], row['NOMBRE'], row['UBICACIONR'], row['FECHAI'],
                        row['RAZA'], row['EDADE'], row['ESTATUS'],
                        row['HISTORIAL'], row['DIAGNOSTICO'], row['TRATAMIENTO'], row['VACUNAS'], ruta
                    )
                    canes_listos.append(can)
        return canes_listos

    # Metodo para generar una nueva peticion de adopcion asignando un identificador aleatorio
    def SOLICITAR_ADOPCION(self, id_canino):
        id_sol = "SOL-" + str(uuid.uuid4())[:8]
        with open(SOLICITUDES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([id_sol, self.id_usuario, id_canino, 'Pendiente'])

# Clase para el personal interno que hereda de usuario y posee permisos especiales de administracion
class TRABAJADOR(USUARIO):
    # Metodo constructor que añade el rol especifico laboral
    def __init__(self, id_usuario, nombre, contacto, contrasena, puesto):
        super().__init__(id_usuario, nombre, contacto, contrasena)
        self.puesto = puesto

    # Metodo que centraliza la insercion modificacion o borrado logico de los registros de perros
    def GESTIONAR_REGISTRO(self, operacion, can_obj):
        if operacion == "AGREGAR":
            can_obj.REG_CANINO()
        elif operacion == "MODIFICAR":
            if isinstance(can_obj, EXPEDIENTE_MEDICO):
                can_obj._actualizar_csv()
            else:
                can_obj.ACTU_PERFIL()
        elif operacion == "ELIMINAR":
            can_obj.DEL_PERFIL()

    # Metodo para revisar que peticiones de adopcion se encuentran en espera de aprobacion
    def OBTENER_SOLICITUDES(self):
        sols = []
        if os.path.exists(SOLICITUDES_CSV):
            with open(SOLICITUDES_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['ESTADO'] == 'Pendiente':
                        sols.append(row)
        return sols

    # Metodo que permite aceptar o denegar una peticion actualizando los archivos y enviando una resolucion
    def VALID_ADOPCION(self, id_solicitud, id_destino, id_canino, apto):
        filas = []
        with open(SOLICITUDES_CSV, mode='r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            filas = list(reader)
        with open(SOLICITUDES_CSV, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            for fila in filas:
                if fila and fila[0] == id_solicitud:
                    fila[3] = 'Aprobada' if apto else 'Rechazada'
                writer.writerow(fila)
        if apto:
            filas_c = []
            with open(CANES_CSV, mode='r', newline='', encoding='utf-8') as f:
                reader_c = csv.reader(f)
                filas_c = list(reader_c)
            with open(CANES_CSV, mode='w', newline='', encoding='utf-8') as f:
                writer_c = csv.writer(f)
                for fila in filas_c:
                    if fila and fila[0] == id_canino:
                        fila[6] = "ADOPTADO"
                    writer_c.writerow(fila)
        id_reporte = "REP-" + str(uuid.uuid4())[:8]
        msg = f"Su solicitud para el can {id_canino} ha sido APROBADA." if apto else f"Su solicitud para el can {id_canino} ha sido RECHAZADA."
        reporte = REPORTE_ADOPCION(id_reporte, id_destino, msg, apto)
        reporte.ENVIAR_NOTI()

    # Metodo rapido para modificar directamente la situacion de un perro especifico
    def ACT_ESTATUSC(self, can_obj, nuevo_estatus):
        can_obj.estatus = nuevo_estatus
        if isinstance(can_obj, EXPEDIENTE_MEDICO):
            can_obj._actualizar_csv()
        else:
            can_obj.ACTU_PERFIL()

# Clase que maneja las notificaciones enviadas a los usuarios sobre sus tramites
class REPORTE_ADOPCION:
    # Metodo constructor con los detalles del aviso resultante de una evaluacion
    def __init__(self, id_reporte, id_destino, mensaje, apto_adopcion):
        self.id_reporte = id_reporte
        self.id_destino = id_destino
        self.mensaje = mensaje
        self.apto_adopcion = apto_adopcion

    # Metodo que almacena el veredicto para que el interesado lo pueda revisar despues
    def ENVIAR_NOTI(self):
        with open(REPORTES_CSV, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow([self.id_reporte, self.id_destino, self.mensaje, str(self.apto_adopcion)])

    # Metodo estatico para buscar todas las respuestas vinculadas a un usuario en particular
    @staticmethod
    def AVANCE_SOLI(id_usuario):
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

# Clase para recopilar metricas y calcular el exito general de la plataforma
class ESTADISTICA:
    # Metodo constructor que inicia los contadores y llama a la recoleccion inicial
    def __init__(self):
        self.usuariost = 0
        self.canest = 0
        self.canes_rescatados = 0
        self._cargar_datos()

    # Metodo interno que cuenta la poblacion activa leyendo los diferentes archivos
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

    # Metodo que devuelve un resumen en texto de los totales encontrados
    def IMPACTO_SOCIAL(self):
        return f"Usuarios: {self.usuariost} | Rescatados Históricamente: {self.canes_rescatados} | Listos para adopción: {self.canest}"

    # Metodo que calcula y devuelve matematicamente la efectividad de las rehabilitaciones
    def REPORTE_ANALISIS(self):
        if self.canes_rescatados == 0:
            return "No hay canes registrados para calcular el impacto."
        porcentaje = (self.canest / self.canes_rescatados) * 100
        return f"Porcentaje de canes rehabilitados (listos para adopción) frente al total rescatado activo: {porcentaje:.2f}%"