from io import BytesIO
from PIL import Image

def image_to_byte_array(image):
    with BytesIO() as byte_array:
        image.save(byte_array, format="BMP")
        return byte_array.getvalue()

def byte_array_to_image(byte_array):
    with BytesIO(byte_array) as byte_stream:
        return Image.open(byte_stream)