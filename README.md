# TFG - Aplicación Visual de Análisis de ECG en Python

Aplicación web que permite visualizar y analizar señales de electrocardiograma desarrollada en Dash (Plotly) 
e integrando el módulo WTdelineator.

Permite visualizar y analizar señales de electrocardiograma (ECG) desde el navegador web, facilitando ver 
ciertos parámetros de la señal, detectar sus distintas ondas y posibles patrones que pueden poner en riesgo la vida 
de un paciente.</br>

<h2>Instalación y despliegue</h2>
Para desplegar el proyecto, se seguirán los siguientes pasos (realizados en MacOS).</br>

</br>Instalamos Anaconda:</br>
<code>https://www.anaconda.com/products/individual</br></code>

Desde una terminal (Linux o MacOS) se clonará el repositorio:</br>
<code>git clone https://github.com/crismartin/TFG</br></code>

Nos ubicaremos dentro del directorio "TFG" e instalaremos el entorno de Conda, creando el entorno "EcgEnv":</br>
<code>conda env create -f environment.yml</code></br>

Activaremos el entorno para la configuración de <b>MongoDB</b>:</br>
<code>conda activate EcgEnv</code></br>

Crearemos el directorio /data/db:</br>
<code>mkdir /data/db</code></br>

Damos permisos de sólo lectura al directorio:</br>
<code>sudo chown -R $USER /data/db </code></br>

Iniciamos el servidor de mongo sin control de acceso:</br>
<code>mongod --port 27017 --dbpath /data/db</code>

Desde una <b>nueva</b> terminal, activamos el entorno y conectamos un cliente de mongo al servidor de mongo antes lanzado:</br>
<code>conda activate EcgEnv</code></br>
<code>mongo --port 27017</code></br>

Creamos el usuario administrador:</br>
<code>db.createUser({user:"hexxa", pwd:"1708bilens",roles:[{role: "userAdminAnyDatabase",db: "admin" }], mechanisms: [ "SCRAM-SHA-1","SCRAM-SHA-256"]})</code></br>

Creamos la BBDD para la aplicación:</br>
<code>use EcgDB</code>

Creamos el usuario con roles de escritura/lectura para <b>EcgDb</b>: </br>
<code>db.createUser({user:"hexxa", pwd:"1708bilens",roles:[{role:"dbAdmin",db: "EcgDB"}, {role:"readWrite",db: "EcgDB"}], mechanisms: [ "SCRAM-SHA-1","SCRAM-SHA-256"]})</code></br>

Creamos las colecciones y cerramos el cliente de mongo: </br>
<code>db.createCollection("Anotaciones_Temp")</code></br>
<code>db.createCollection("Ficheros")</code></br>
<code>db.createCollection("SesionesUsuario")</code></br>
<code>db.createCollection("Usuarios")</code></br>

Ahora, con el entorno y con el servidor de mongo activos, iremos al directorio del código de la aplicación: </br>
<code>cd TFG/ecp_app</code></br>

Lanzamos el ejecutable de la aplicación: </br>
<code>python3 server.py</code>

Por útimo, desde un navegador iremos a la siguiente url:</br> 
<code>http://localhost:8050/</code></br>

<h2>Manual de usuario</h2>
Lo puedes encontrar en el directorio raíz del repositorio como <code>manualUser.pdf</code>, en él se explica las 
principales funciones en un uso típico que se puede realizar en la aplicación.</br>

<h2>Comentarios y feedback</h2>
Todo proyecto de software no termina. Si tienes algún comentario, sugerencia o dudas al momento de querer agregar nuevas 
funcionalidades, agradecería un <i>pull-request</i>.

Para lo demás, escríbeme a <mail>c.martinezros@alumnos.urjc.es</mail>

<h2>Licencia</h2>
Proyecto desarrollado como Trabajo de Fin de Grado (TFG) para la Universidad Rey Juan Carlos 
por parte de Cristian Fabián Martínez Rosero (2019-2020).
