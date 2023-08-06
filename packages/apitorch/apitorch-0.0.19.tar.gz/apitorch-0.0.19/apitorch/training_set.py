from apitorch.api_client import Client
from apitorch.errors import ArgumentError
from apitorch.routes import training_set_images_route, training_set_list_route, upload_image_route
from apitorch.utils import download_file, ReusableSession
from multiprocessing import Pool
from pathlib import Path
from time import perf_counter
from . import logger


def upload_image(training_set_id, label_slug, **kwargs):
    logger.info('Request: Upload training image')
    image_data = kwargs.get('image')
    image_url = kwargs.get('image_url')

    if image_data and image_url:
        raise ArgumentError('Only one of image, image_url must be specified')

    if not image_data and not image_url:
        raise ArgumentError('One of image, image_url must be specified')

    client = Client()
    post_url = upload_image_route(training_set_id, label_slug)
    response = None

    if image_url:
        postdata = kwargs
        response = client.post(post_url, postdata)

    if image_data:
        response = client.post_with_file(post_url, image_data)

    return response.json()


def list_training_sets():
    logger.info('Request: List training sets')
    client = Client()
    url = training_set_list_route()
    response = client.get(url)
    return response.json()


def get_images_by_label(training_set_id):
    if not training_set_id:
        raise ArgumentError('training_set_id is a required argument')
    logger.info('Request: Get training set images')
    client = Client()
    url = training_set_images_route(training_set_id)
    response = client.get(url)
    return response.json()


def download_images(training_set_id, path, overwrite=False):
    logger.info(f'Request: Download images for training_set={training_set_id}')
    parent_path = prepare_download_images(path)
    response = get_images_by_label(training_set_id)
    destination = parent_path / str(response['training_set_slug'])
    destination.mkdir(exist_ok=True)
    log_pre_totals(response, destination)
    session = ReusableSession()

    # loop through labels
    for label_data in response['data']:
        label_name = label_data['label']
        image_dir = destination / str(label_name)
        image_dir.mkdir(exist_ok=True)
        num_saved = num_skipped = 0

        t_0 = perf_counter()
        with Pool(4) as pool:
            images = label_data['images']
            params = [(image, image_dir, overwrite, session)
                      for image in images]
            results = [pool.apply_async(
                download_training_image, param) for param in params]
            for r in results:
                result = r.get()
                if result:
                    num_saved += 1
                else:
                    num_skipped += 1
        t_elapsed = perf_counter() - t_0
        log_post_batch(num_saved, num_skipped, image_dir, t_elapsed)


def download_images_sync(training_set_id, path, overwrite=False):
    parent_path = prepare_download_images(path)
    response = get_images_by_label(training_set_id)
    destination = parent_path / str(response['training_set_slug'])
    destination.mkdir(exist_ok=True)
    log_pre_totals(response, destination)
    session = ReusableSession()

    # loop through labels
    for label_data in response['data']:
        label_name = label_data['label']
        image_dir = destination / str(label_name)
        image_dir.mkdir(exist_ok=True)
        num_saved = num_skipped = 0
        # download individual images
        t_0 = perf_counter()
        for image in label_data['images']:
            if download_training_image(image, image_dir, overwrite, session):
                num_saved += 1
            else:
                num_skipped += 1
        t_elapsed = perf_counter() - t_0
        log_post_batch(num_saved, num_skipped, image_dir, t_elapsed)


def download_training_image(image, image_dir: Path, overwrite: bool, session: ReusableSession):
    filename = str(image['filename'])
    image_dest = image_dir / filename
    return download_file(image['url'], image_dest, overwrite, session)


def prepare_download_images(path):
    if not path:
        raise ArgumentError('path is a required argument')
    parent_path = Path(path)
    if not parent_path.is_dir():
        raise ArgumentError(f'could not find directory at path: {path.name}')
    return parent_path


def log_pre_totals(response, destination) -> None:
    num_labels = total_images = 0
    for label_data in response['data']:
        num_labels += 1
        total_images += len(label_data['images'])
    logger.info(
        f'Downloading {total_images} images from {num_labels} labels to {destination}...')


def log_post_batch(num_saved: int, num_skipped: int, image_dir: Path, time_elapsed: float) -> None:
    log_message = ' - ' + \
        f'Saved {num_saved} ' + \
        (f'(skipped {num_skipped}) ' if num_skipped > 0 else '') + \
        f'images to {image_dir} in {time_elapsed:0.4f} seconds'
    logger.info(log_message)
