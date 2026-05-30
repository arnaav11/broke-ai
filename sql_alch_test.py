import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import text
import random as rand

from geopy.geocoders import Nominatim

# Initialize the geocoder with a custom user-agent
geolocator = Nominatim(user_agent="my_geo_app")

# Enter the address you want to look up
address = ""
location = geolocator.geocode(address)

if location:
    print(f"Address: {location.address}")
    print(f"Latitude: {location.latitude}")
    print(f"Longitude: {location.longitude}")
else:
    print("Location not found.")

print(sqlalchemy.__version__)

engine = create_engine("sqlite+pysqlite:///test.db", echo=True)


with engine.connect() as conn:
    conn.execute(text('DROP TABLE IF EXISTS multimodal_table'))
    conn.execute(
        text("CREATE TABLE multimodal_table (username varchar(50), email varchar(60), lat decimal(10, 7), lon decimal(10, 7), age int)"))

    nums = [{"x": i, "y": i**2} for i in range(1, 10)]
    query = f"INSERT INTO some_table (x, y) VALUES (:x, :y)"

    nums = [{"username": f"{i}"*i, "email": f"{i}@gmail.com", "lat": rand.random(), "lon": rand.random(), "age": i} for i in range(1, 10)]
    query = f"INSERT INTO multimodal_table (username, email, lat, lon, age) VALUES (:username, :email, :lat, :lon, :age)"

    print(f'Executing query: "{query}"')
    result = conn.execute(text(query), nums)

    result = conn.execute(text("SELECT * from multimodal_table"))
    print(result.all())

    conn.commit()