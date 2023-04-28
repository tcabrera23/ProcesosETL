Este programa tiene como objetivo obtener una lista de canciones reproducidas en el último día de un usuario de Spotify y guardar la información en una base de datos relacional.
Al ingresar a la web (https://developer.spotify.com/console/get-recently-played/?limit=&after=&before=) obtendrás el token de la API de tu cuenta de Spotify. Yo dejo los campos vacíos por seguridad. 
Pasos: 
- Creamos funciones para verificar que los datos que estamos tomando son válidos junto a la autenticación de la cuenta.
- Extraemos los datos en nuestro programa mediante la API 
- Del archivo JSON nos quedamos con las claves que queremos utilizar.
- Agregamos los datos obtenidos a unas listas y referenciamos hacia un diccionario para posteriormente cargar los datos en un dataframe.
- Creamos una base de datos donde quedará almacenado el dataframe. Hacemos la conexión a la base de datos mediante el método engine y definiendo las variables que tendremos en las tablas.  Mediante el software Dbeaver podrías visualizar los resultados. 

Por último, automatizamos el proceso con Airflow creando nuestros dags. Conectándonos al servidor y ejecutando las tareas tendremos a este programa funcionando por sí solo.
