from pymavlink import mavutil
import time

# прослушивания UDP-соединения
the_connection = mavutil.mavlink_connection('udpin:127.0.0.1:14500')

# Ждем получения первого пакета от MAVProxy для синхронизации
the_connection.wait_heartbeat()


# Отправка данных о местоположении
def send_gps_data(latitude, longitude, altitude):
    msg = the_connection.mav.gps_raw_int_encode(
        int(time.time() * 1000),  # время в мс с начала эпохи
        3,                        # GPS fix type (3 означает 3D фикс)
        int(latitude * 1e7),      # широта в 1E-7 градусов
        int(longitude * 1e7),     # долгота в 1E-7 градусов
        int(altitude * 1000),     # высота в мм
        0,                        # GPS HDOP (horizontal dilution of precision)
        0,                        # GPS VDOP (vertical dilution of precision)
        0,                        # скорость в см/с
        0,                        # направление в 100th градусах
        0,                        # вертикальная скорость в см/с
        0                         # количество спутников
    )
    # Отправка пакета
    the_connection.mav.send(msg)

# Пример симуляционных данных
latitude = 37.7749
longitude = -122.4194
altitude = 10.0

# Цикл отправки данных каждые 2 секунды
while True:
    send_gps_data(latitude, longitude, altitude)
    time.sleep(2)
    latitude += 0.0001
    longitude += 0.0001

