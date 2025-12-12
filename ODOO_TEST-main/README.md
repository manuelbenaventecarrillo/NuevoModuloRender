# OdooTests
# **Implementación de Odoo en Render**
# Texto modificacion verificacion

## **1. Requisitos Previos**
### **1.1 GitHub**
Antes de comenzar, debemos tener preparado nuestro repositorio en GitHub con la siguiente estructura de directorios:
```bash
Dockerfile
extra-addons/
├── .gitkeep
└── dummy_module/
    ├── __init__.py
    └── __manifest__.py
README.md
```

> 🔴 **Nota:** 🔴 
> Los unicos archivos con contenido son: "Dockerfile" y "__manifest__.py", el resto no tienen contenido.
> El contenido de estos archivos se encuentra al final de esta documentación.

---
### **1.2 Render**

Para poder implementar Odoo en Render, será necesario:
- Crear una cuenta en [Render](https://render.com/).
- Iniciar sesión en la plataforma con tu cuenta de **GitHub** o **GitLab** para vincular directamente tu repositorio, o bien introducir manualmente el enlace HTTPS del repositorio si se trata de uno externo.
Render detectará automáticamente el repositorio y permitirá desplegar el proyecto desde él. antes de proceder con la configuración del servicio.

---
## **2. Pasos en Render para Crear el Servicio de Odoo**

### **2.1 Crear Web Service en Render**

En la parte superior derecha de la página de Render, haremos clic en **"New"** y seleccionaremos la opción **"Web Service"**.

A continuación:

1. Enlazaremos el servicio con el repositorio de **GitHub** que el usuario haya creado previamente, el cual contiene el árbol de directorios mostrado en el apartado anterior.  
2. Configuraremos el servicio según las preferencias del usuario, en nuestro caso (nombre el que deseemos, language/lenguaje = "docker", región "Frankfurt", "Instance Type" = "Free", etc.).  
3. Es **muy importante** seleccionar el tipo de lenguaje (**Language**) como **Docker**.  
4. Finalmente, haremos clic en **"Deploy Web Service"**.

Render comenzará el proceso de implementación, analizando el contenido del repositorio y preparando el entorno.  
Este proceso puede tardar unos minutos.  
Si todo es correcto, Render mostrará un mensaje informando del **estado del despliegue**.  
En caso contrario, se mostrarán mensajes de error indicando el motivo del fallo.

---
### **2.2 Crear la Base de Datos Postgres**

De nuevo, en la parte superior derecha de Render, haremos clic en **"New"** y esta vez seleccionaremos la opción **"Postgres"**.

Después:

1. Configuraremos la base de datos según las preferencias del usuario, en nuestro caso, como anteriormente (nombre el que deseemos, language/lenguaje = "docker", región "Frankfurt", "Instance Type" = "Free", etc.).    
2. Cuando todo esté listo, pulsaremos el botón **"Create Database"**.

Esto creará nuestra base de datos **PostgreSQL**, que será la que Odoo utilizará para almacenar toda la información del sistema.

---
## **3. Conexión entre Odoo y la Base de Datos Postgres en Render**
Una vez creados ambos servicios (el **Web Service** y la **Base de Datos Postgres**), debemos establecer la conexión entre ellos para que Odoo pueda acceder correctamente a la base de datos.
---

### **3.1 Obtener las credenciales de la Base de Datos**

1. Accede a tu servicio de **Postgres** en Render.  
2. Dirígete a la pestaña **"Connections"**.  
3. Copia los siguientes datos que Render proporciona automáticamente:
   - **Host**
   - **Database**
   - **User**
   - **Password**
   - **Internal Database URL** (opcional, solo de referencia)

Render mostrará también información adicional como:
- **Internal Database URL**
- **External Database URL**

> 🔴 **Importante:** 🔴 
> La **Internal Database URL** es la que deberás usar preferentemente al configurar Odoo, ya que ofrece una conexión interna más rápida y segura entre servicios dentro de Render.

Guarda estos valores, ya que los necesitaremos para configurar las variables de entorno del servicio Odoo.

---
### **3.2 Configurar las Variables de Entorno en Odoo**

1. Ve al servicio **Web Service (Odoo)** que creaste en Render.  
2. En el panel lateral, selecciona la opción **"Environment"**.  
3. Añade las siguientes variables con los valores obtenidos del servicio Postgres:

| Nombre de la variable | Valor (ejemplo)                 | Descripción                                  |
|------------------------|----------------------------------|----------------------------------------------|
| `PGHOST`              | `oregon-postgres.render.com`     | Dirección del host de la base de datos       |
| `PGPORT`              | `5432`                           | Puerto de conexión PostgreSQL (por defecto)  |
| `PGUSER`              | `nombre_de_usuario`              | Usuario de la base de datos                  |
| `PGPASSWORD`          | `contraseña_asignada`            | Contraseña de la base de datos               |
| `PGDATABASE`          | `nombre_de_tu_bd`                | Nombre de la base de datos                   |
> 🔴 **Nota:** 🔴
> Asegúrate de que los nombres de las variables coinciden exactamente con los utilizados en el archivo `Dockerfile`.  
> Por ejemplo, si en el Dockerfile aparece `$PGHOST`, la variable deberá llamarse **PGHOST** en Render.


4. Guarda los cambios y Render reiniciará el servicio automáticamente.

---
### **3.3 Verificar la Conexión**
Cuando el servicio Odoo se reinicie:
- Si todo está configurado correctamente, en los **logs** (pestaña “Logs”) verás los mensajes:
==> Checking/initializing DB <nombre_de_tu_bd>
==> Starting Odoo server

> 🔴 **Consejos:** 🔴
> Asegúrate de que tanto Odoo como Postgres estén en la misma región dentro de Render para evitar problemas de conexión o latencia.
> Si hay algún error (por ejemplo, credenciales incorrectas o base de datos inaccesible), Render mostrará mensajes indicando el problema.

---

## **4. Contenido de los Archivos del Proyecto**
A continuación se muestra el contenido de los archivos principales utilizados en la implementación del proyecto.

### **4.1 Archivo `Dockerfile`**
```
# Imagen base Odoo 17
FROM odoo:17

# (Opcional) módulos propios
COPY ./extra-addons /mnt/extra-addons

# Puerto HTTP de Odoo
EXPOSE 8069

# Puerto por defecto de PostgreSQL
ENV PGPORT=5432

# 1) Inicializa la BD indicada en $PGDATABASE si está vacía (stop-after-init)
# 2) Después arranca el servidor normalmente
#
# NOTA: usamos $PGDATABASE para que la inicialización vaya contra esa BD
# y --db-filter la fije para evitar que Odoo “coja” otra por error.
CMD ["bash","-lc", "\
  echo '==> Checking/initializing DB $PGDATABASE' && \
  odoo -d $PGDATABASE -i base --without-demo=all \
       --db_host=$PGHOST --db_port=$PGPORT \
       --db_user=$PGUSER --db_password=$PGPASSWORD \
       --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
       --stop-after-init || true; \
  echo '==> Starting Odoo server' && \
  odoo --db_host=$PGHOST --db_port=$PGPORT \
       --db_user=$PGUSER --db_password=$PGPASSWORD \
       --addons-path=/usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons \
       --db-filter=$PGDATABASE \
       --dev=all"]
```
### **4.1 Archivo `__manifest__.py`**
```
{
    "name": "Dummy Module",
    "version": "1.0",
    "summary": "Módulo vacío de prueba",
    "installable": True,
}
```







#