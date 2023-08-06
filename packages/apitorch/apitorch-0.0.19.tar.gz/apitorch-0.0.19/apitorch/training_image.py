from apitorch.api_client import Client
from apitorch.routes import delete_image_route


def delete_image(image_id):
    client = Client()
    url = delete_image_route(image_id)
    response = client.delete(url)
    return response.json()
