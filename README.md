SISTEMA DE ADOPCION DE MASCOTAS

DESCRIPCION GENERAL

Este proyecto fue desarrollado como una solucion de software para la gestion integral de un centro de adopcion de canes. El objetivo principal es conectar a los veterinarios o trabajadores del refugio con las personas interesadas en adoptar una mascota de manera responsable.

El sistema esta construido bajo una arquitectura modular separada en dos capas principales: el Backend, que contiene toda la logica de negocio, las clases de las entidades y el manejo de datos; y el Frontend, que despliega una interfaz grafica de usuario moderna y responsiva.

Para la persistencia de los datos, decidimos utilizar archivos de texto plano en formato CSV. Esto permite almacenar la informacion de manera local sin necesidad de montar un servidor de base de datos relacional complejo, facilitando la portabilidad del proyecto entre diferentes computadoras.
REQUISITOS E INSTALACION

Para ejecutar esta aplicacion, es necesario contar con Python instalado en su equipo, ademas de las siguientes dependencias de interfaz grafica y procesamiento de imagenes:

* customtkinter: Libreria encargada de proveer los componentes graficos modernos.
* pillow: Libreria utilizada para la carga, redimensionamiento y despliegue de las fotografias de los perritos.

Puedes instalar estas librerias ejecutando el siguiente comando en tu consola:
pip install customtkinter pillow

COMO EJECUTAR EL PROYECTO

1. Asegurate de guardar los archivos backend.py y frontend.py dentro del mismo directorio o carpeta de trabajo.
2. Abre la terminal o linea de comandos posicionandote en dicha carpeta.
3. Inicia la aplicacion ejecutando el archivo del frontend con el comando:
python frontend.py
1. El sistema verificara la existencia de las bases de datos en CSV de forma automatica. Si no existen, invocara una rutina de inicializacion que creara los archivos usuarios.csv, canes.csv, reportes.csv y solicitudes.csv junto con algunos registros de prueba preestablecidos.

CREDENCIALES DE PRUEBA INCLUIDAS
Para evaluar las capacidades del sistema de forma inmediata, se han precargado dos perfiles con diferentes niveles de acceso:

* Cuenta de Trabajador (Veterinario):
ID Usuario: T01
Contraseña: 123
* Cuenta de Usuario (Adoptante):
ID Usuario: U01
Contraseña: 456

FUNCIONAMIENTO DE LA ARQUITECTURA
El codigo aprovecha los pilares de la Programacion Orientada a Objetos de la siguiente manera:

* Herencia: La clase EXPEDIENTE_MEDICO extiende de CANINO para especializar sus atributos de salud sin duplicar codigo. De igual forma, TRABAJADOR hereda de USUARIO para adquirir la capacidad de iniciar sesion, pero sumando privilegios administrativos avanzados.
* Encapsulamiento y Metodos Estatiticos: Clases como USUARIO contienen metodos estaticos para validar accesos globales, centralizando las operaciones de lectura en la coleccion de datos.
* Borrado Logico: Cuando un trabajador elimina un perro, el registro no desaparece del archivo CSV fisicamente, sino que su atributo ESTATUS cambia a ELIMINADO. Esto evita la perdida de historial medico y mantiene la integridad referencial de las solicitudes.
