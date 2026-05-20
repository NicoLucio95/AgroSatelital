import ee

class EarthEngineService:
    def __init__(self):
        self._initialize()

    def _initialize(self):
        try:
            ee.Initialize(project='agro-satelital')
        except Exception:
            print("Autenticando en Earth Engine...")
            ee.Authenticate()
            ee.Initialize(project='agro-satelital')

    def get_point(self, lat, lon):
        return ee.Geometry.Point([lon, lat])

    def get_collection(self, point, start_date, end_date, cloud_threshold=20):
        collection = (
            ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
            .filterBounds(point)
            .filterDate(start_date, end_date)
            .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', cloud_threshold))
        )
        return collection

    def get_image_list(self, collection):
        size = collection.size().getInfo()
        return collection.toList(size), size

    def get_image_metadata(self, image):
        date = image.date().format("dd-MM-YYYY").getInfo()
        cloud = image.get("CLOUDY_PIXEL_PERCENTAGE").getInfo()
        return {
            "date": date,
            "cloud": cloud
        }

    def get_thumbnail_url(self, image, region, size=512):
        # Seleccionar bandas RGB (Sentinel-2)
        image_rgb = image.select(['B4', 'B3', 'B2'])

        url = image_rgb.getThumbURL({
            'region': region,
            'dimensions': size,
            'format': 'png',
            'min': 0,
            'max': 3000
        })
        return url

    def get_ndvi_image(self, image):
        return image.normalizedDifference(['B8', 'B4'])