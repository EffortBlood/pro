==========================
Interfaz Asistente Fiscal
==========================

Genera archivos de de texto de las facturas, compatibles con el Asistente Fiscal ("Super Spooler Fiscal") (AF), para su impresion en impresoras fiscales.

Puede funcionar en servidores locales o remotos ("en la nube"), con Linux o Windows. Tambien con Docker.

*Pruebas realizadas:*
    . Odoo Community versiones 14 y 15. 
    . Servidores locales Windows, Linux (Debian, Ubuntu, Arch Linux (Manjaro))
    . Docker/Linux
    . Docker con host Windows y MV Linux debian (VirtualBox)

Instalacion
============

Instalar por la interfaz de aplicaciones (Aplicaciones) de Odoo.
Nombre tecnico "ca_interfaz_asistente_fiscal"


Configuracion
==============
*Consideraciones*
    . Odoo genera las facturas en el servidor. Si no hay conexion, no se generan. Por lo tanto los respectivos archivos se crean de ese lado, el servidor (backend).
    . El AF funciona "capturando" los archivos de texto de las facturas en una carpeta especificada para ello
    . El AF se ejecuta en PCs Windows, y a estas se conectan las impresoras fiscales.
    . Lo importante es que el AF tenga acceso a la carpeta, sea servidor Windows, Linux, use o no Docker, etc.
    . Los archivos de texto ocupan alrededor 1k de espacio, su transferencia es rapida asi sea lenta la conexion


*Carpeta de facturas por defecto*
    - Windows: c:\facturas_txt
    - Linux: /var/lib/odoo/facturas_txt/facturas_txt (PROGRAMARLO 01/07/2022)
    - Docker: /svr/odoo/web/facturas_txt --> /var/lib/odoo/facturas_txt (en el contenedor Odoo)
    - Docker online


*Nombres de archivos*
    - Facturas:         fa<num_fact>.<num_estacion>. Ejemplo: fa00030.001, fa00250.002
    - Notas de credito: nc<num_fact>.<num_estacion>. Ejemplo: nc00030.001, nc00250.002


*1. Configuracion inicial*
    - Al instalar  el AF (Spooler) debe especificarsele la carpeta de facturas
    - Configurada la carpeta ya puede imprimirse. Valores por defecto: Estacion: 001, carpeta: *facturas_txt


*2. Personalizar carpeta*
    - 

*3. Personalizar estaciones (cajas)*


*4. Compartir carpetas*
    - NOTA: Este es un tema de administracion de redes, sin ambargo aqui explico brevemente algunas soluciones


Uso
====

