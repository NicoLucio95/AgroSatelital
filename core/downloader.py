import ee
import os
import requests
from datetime import datetime

from services.earth_engine import EarthEngineService


def descargar_imagenes(
    coords,
    start_date="2023-01-01",
    end_date="2023-12-31",
    max_images=10,
    cloud_threshold=20,
    buffer_meters=1000,
    output_dir="data/raw"
):

    os.makedirs(output_dir, exist_ok=True)

    lat, lon = coords

    # 👉 Formateo de coordenadas (PROLIJO)
    lat_str = f"{lat:.4f}"
    lon_str = f"{lon:.4f}"

    ee_service = EarthEngineService()

    print("📍 Creando punto geográfico...")
    point = ee_service.get_point(lat, lon)

    print("🛰️ Consultando colección...")
    collection = ee_service.get_collection(
        point, start_date, end_date, cloud_threshold
    )

    images_list, total = ee_service.get_image_list(collection)

    print(f"📊 Total de imágenes encontradas: {total}")

    if total == 0:
        print("⚠️ No se encontraron imágenes")
        return

    region = point.buffer(buffer_meters).bounds().getInfo()

    descargadas = 0

    # 👉 Si max_images es None, descargar todas
    cantidad_descarga = total if max_images is None else min(total, max_images)

    for i in range(cantidad_descarga):
        print(f"\n⬇️ Descargando imagen {i+1}...")

        image = images_list.get(i)
        image = ee.Image(image)

        metadata = ee_service.get_image_metadata(image)

        fecha = metadata["date"] if metadata["date"] else f"img_{i}"

        # 👉 Sanitizar fecha (clave para Windows)
        fecha_safe = fecha.replace("/", "-").replace(":", "-")

        cloud = metadata["cloud"]

        print(f"📅 Fecha: {fecha_safe} | ☁️ Nubes: {cloud}")

        try:
            url = ee_service.get_thumbnail_url(image, region)

            response = requests.get(url)

            if response.status_code == 200:

                # 👉 NOMBRE FINAL (coordenadas adelante)
                filename = f"lat{lat_str}_lon{lon_str}_{fecha_safe}_{i}.png"
                filepath = os.path.join(output_dir, filename)

                with open(filepath, "wb") as f:
                    f.write(response.content)

                print(f"✅ Guardado en: {filepath}")
                descargadas += 1

            else:
                print(f"❌ Error HTTP: {response.status_code}")

        except Exception as e:
            print(f"❌ Error: {e}")

    print(f"\n🎉 Descarga finalizada: {descargadas} imágenes")