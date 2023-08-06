def classify_image_route():
    return 'classify'


def list_classifiers_route():
    return 'classifiers'


def ping_route():
    return 'ping'


def training_set_images_route(training_set_id):
    return f'training-set/{training_set_id}/images'


def training_set_list_route():
    return f'training-sets'


def upload_image_route(training_set_id, label_slug):
    return f'training-set/{training_set_id}/{label_slug}/image'


def delete_image_route(image_id):
    return f'training-image/{image_id}'
