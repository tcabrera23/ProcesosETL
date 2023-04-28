import sqlalchemy
import pandas as pd 
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


ubicacionBaseDeDatos = "sqlite:///my_played_tracks.sqlite"
userID = "" # Usuario de Spotify 
TOKEN = "" # API TOKEN Spotify (https://developer.spotify.com/console/get-recently-played/)

def datosValidos(df: pd.DataFrame) -> bool:
    # Verifico si el dataframe está vacío
    if df.empty:
        print("No hay canciones descargadas")
        return False 

    # Verifico Primary Key
    if pd.Series(df['played_at']).is_unique:
        pass
    else:
        raise Exception("Primary Key corrupta")

    # Check for nulls
    if df.isnull().values.any():
        raise Exception("No se han encontrado valores")


if __name__ == "__main__":

    # Extract 
    headers = {
        "Accept" : "application/json",
        "Content-Type" : "application/json",
        "Authorization" : "Bearer {token}".format(token=TOKEN)
    }
     
    # Convirtiendo las unidades del tiempo
    today = datetime.datetime.now()
    yesterday = today - datetime.timedelta(days=30)
    yesterdayUnixTimestamp = int(yesterday.timestamp()) * 1000

    # Obteniendo todas las canciones escuchadas en las últimas 24 horas   
    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?after={time}".format(time=yesterdayUnixTimestamp), headers = headers)

    data = r.json()

    # Inicializando las listas a cargarpip 
    songNames = []
    artistNames = []
    playedAtList = []
    timeStamps = []
   
    # Transform
   
    # Agregando los datos obtenidos a las listas
    for song in data["items"]:
        songNames.append(song["track"]["name"])
        artistNames.append(song["track"]["album"]["artists"][0]["name"])
        playedAtList.append(song["played_at"])
        timeStamps.append(song["played_at"][0:10])
        
    # Asignando un diccionario para luego utilizar la librería pandas    
    song_dict = {
        "song_name" : songNames,
        "artist_name": artistNames,
        "played_at" : playedAtList,
        "timestamp" : timeStamps
    }

    songDf = pd.DataFrame(song_dict, columns = ["song_name", "artist_name", "played_at", "timestamp"])
    print(songDf)
    
    # Validando
    if datosValidos(songDf):
        print("Datos válidos")

    # Load

    engine = sqlalchemy.create_engine(ubicacionBaseDeDatos)
    conexion = sqlite3.connect('my_played_tracks.sqlite')
    cursor = conexion.cursor()

    sqlQuery= """
    Creando la tabla por si no existe my_played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sqlQuery)
    print("La base de datos fue abierta exitosamente")
    
    try:
        songDf.to_sql("my_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Ya existen datos en la base de datos")

    conexion.close()
    print("Base de datos cerrada exitosamente")
    
