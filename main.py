from core.downloader import descargar_imagenes
from datetime import datetime

def convertir_fecha(fecha_str):
    try:
        fecha = datetime.strptime(fecha_str, "%d-%m-%Y")
        return fecha.strftime("%Y-%m-%d")
    except:
        print("❌ Formato inválido. Usar DD-MM-YYYY")
        return None


if __name__ == "__main__":

    print("=== AGRO SATELITAL ===")

    lat = float(input("Latitud: "))
    lon = float(input("Longitud: "))

    fecha_inicio_input = input("Fecha inicio (DD-MM-YYYY): ")
    fecha_fin_input = input("Fecha fin (DD-MM-YYYY): ")

    start_date = convertir_fecha(fecha_inicio_input)
    end_date = convertir_fecha(fecha_fin_input)

    if not start_date or not end_date:
        exit()

    max_images = int(input("Cantidad de imágenes (0 = máximo disponible): "))

    if max_images == 0:
        max_images = None

    # 👉 NUEVO
    radio_km = float(input("Radio (km): "))
    buffer_meters = radio_km * 1000

    coords = (lat, lon)

    print("📡 Descargando imágenes...")

    descargar_imagenes(
        coords,
        start_date=start_date,
        end_date=end_date,
        max_images=max_images,
        buffer_meters=buffer_meters
    )

    print("✅ Descarga finalizada")