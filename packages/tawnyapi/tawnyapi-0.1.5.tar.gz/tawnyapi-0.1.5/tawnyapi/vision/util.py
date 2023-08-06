
import base64
from typing import List
import imutils
import cv2


def _get_resized_shape(resize=None, original_img_shape=None):
    if resize is None or original_img_shape is None:
        return None, None, 1

    (h, w) = original_img_shape[:2]
    r = 1
    # height
    if h >= w:
        r = resize / float(h)
        dim = (int(w * r), resize)

    # width
    else:
        r = resize / float(w)
        dim = (resize, int(h * r))

    return dim[1], dim[0], r


def _resize_img(img, resize=None):

    (h, w, _) = _get_resized_shape(
        resize=resize, original_img_shape=img.shape)
    if h is None or w is None:
        return img

    resized_img = cv2.resize(img, (w, h))
    return resized_img


def _get_base64_images(images, resize=None, images_already_encoded=False):
    b64_images = []
    for img in images:
        if not images_already_encoded:
            img = _resize_img(img, resize=resize)
            _, buffer = cv2.imencode('.tif', img)
            b64_images.append(base64.b64encode(buffer).decode('ascii'))
        else:
            b64_images.append(base64.b64encode(img).decode('ascii'))
    return b64_images


def _load_images_from_paths(img_paths: List[str], load_as_bytes=False):
    images = []
    for img_path in img_paths:
        if load_as_bytes:
            with open(img_path, "rb") as f_in:
                images.append(f_in.read())
        else:
            img = cv2.imread(img_path, cv2.IMREAD_COLOR)
            images.append(img)
    return images
