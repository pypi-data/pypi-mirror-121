
from tawnyapi.vision.face_detector import FaceDetector
from typing import List
import asyncio

import cv2
import aiohttp
from . import apitypes
from .util import _get_base64_images, _load_images_from_paths, _resize_img, _get_resized_shape
from .face_detector import FaceDetector


class TawnyVisionApiClient:

    def __init__(self,
                 api_url: str = 'https://vision.tawnyapis.com/v1/images',
                 api_key: str = None,
                 use_local_face_detection: bool = False,
                 use_local_face_embedding: bool = False,
                 sdk_version=apitypes.SdkVersion.V_1_4):
        self.async_client = TawnyVisionApiAsyncClient(
            api_url=api_url,
            api_key=api_key,
            use_local_face_detection=use_local_face_detection,
            use_local_face_embedding=use_local_face_embedding,
            sdk_version=sdk_version
        )

    def analyze_image_from_path(
            self,
            image_path: str,
            max_results: int = 1,
            resize: int = 720,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):
        return asyncio.run(self.async_client.analyze_image_from_path(
            image_path=image_path,
            max_results=max_results,
            resize=resize,
            input_type=input_type,
            features=features
        ))

    def analyze_images_from_paths(
            self,
            image_paths: List[str] = [],
            max_results: int = 1,
            resize: int = 720,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):
        return asyncio.run(self.async_client.analyze_images_from_paths(
            image_paths=image_paths,
            max_results=max_results,
            resize=resize,
            input_type=input_type,
            features=features
        ))

    def analyze_image(
            self,
            image,
            max_results: int = 1,
            resize: int = 720,
            images_already_encoded=False,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):
        return asyncio.run(self.async_client.analyze_image(
            image=image,
            max_results=max_results,
            resize=resize,
            images_already_encoded=images_already_encoded,
            input_type=input_type,
            features=features
        ))

    def analyze_images(
        self,
            images=[],
            max_results: int = 1,
            resize: int = 720,
            images_already_encoded=False,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):

        return asyncio.run(self.async_client.analyze_images(
            images=images,
            max_results=max_results,
            resize=resize,
            images_already_encoded=images_already_encoded,
            input_type=input_type,
            features=features
        ))


class TawnyVisionApiAsyncClient:

    def __init__(self,
                 api_url: str = 'https://vision.tawnyapis.com/v1/images',
                 api_key: str = None,
                 use_local_face_detection: bool = False,
                 use_local_face_embedding: bool = False,
                 sdk_version: str = apitypes.SdkVersion.V_1_4):
        self._api_url = api_url
        self._api_key = api_key
        self._use_local_face_detection = use_local_face_detection
        self._use_local_face_embedding = use_local_face_embedding
        self._sdk_version = sdk_version

        self._face_detector = None
        if self._use_local_face_detection:
            self._face_detector = FaceDetector()

    async def analyze_image_from_path(
            self,
            image_path: str,
            max_results: int = 1,
            resize: int = 720,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):
        return await self.analyze_images_from_paths(
            image_paths=[image_path],
            max_results=max_results,
            resize=resize,
            input_type=input_type,
            features=features
        )

    async def analyze_images_from_paths(
            self,
            image_paths: List[str] = [],
            max_results: int = 1,
            resize: int = 720,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]

    ):

        images = _load_images_from_paths(image_paths, load_as_bytes=(
            not self._requires_local_processing(resize)))

        return await self.analyze_images(
            images=images,
            max_results=max_results,
            resize=resize,
            input_type=input_type,
            images_already_encoded=not self._requires_local_processing(resize),
            features=features
        )

    async def analyze_image(
            self,
            image,
            max_results: int = 1,
            resize: int = 720,
            images_already_encoded=False,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):
        return await self.analyze_images(
            images=[image],
            max_results=max_results,
            resize=resize,
            images_already_encoded=images_already_encoded,
            input_type=input_type,
            features=features
        )

    async def analyze_images(
            self,
            images=[],
            max_results: int = 1,
            resize: int = 720,
            images_already_encoded=False,
            input_type=apitypes.ImageInputType.RAW,
            features=[
                apitypes.ImageAnnotationFeatures.FACE_DETECTION,
                apitypes.ImageAnnotationFeatures.FACE_EMOTION
            ]
    ):

        images_base64 = []
        info_about_local_images = []

        if self._requires_local_processing(resize) and images_already_encoded:
            for idx, img in enumerate(images):
                images[idx] = cv2.imread(img)
            images_already_encoded = False

        if self._use_local_face_detection:
            faces = []
            for img in images:
                img = _resize_img(img, resize=resize)
                rects = self._face_detector.detect_faces(img)
                rects.sort(key=lambda r: (r[2]-r[0])*(r[3]-r[1]), reverse=True)

                faces_per_img = 0
                img_rects = []
                for idx, (x1, y1, x2, y2) in enumerate(rects):
                    if idx < max_results:
                        sq_x1, sq_y1, sq_x2, sq_y2 = self._face_detector.get_square_from_box(
                            bounding_box=(x1, y1, x2, y2))
                        face = img[sq_y1:sq_y2, sq_x1:sq_x2]

                        faces.append(face)
                        img_rects.append((x1, y1, x2, y2))
                        faces_per_img += 1

                info_about_local_images.append(
                    {'faces_per_img': faces_per_img, 'rects': img_rects})

            # remove feature face_detection from features because of local use of face detection
            features = list(filter(
                lambda f: f != apitypes.ImageAnnotationFeatures.FACE_DETECTION, features))

            images_base64 = _get_base64_images(images=faces, resize=224)

        else:
            images_base64 = _get_base64_images(
                images=images, resize=resize, images_already_encoded=images_already_encoded)

        request_data = {
            'requests': []
        }
        for img in images_base64:
            request_data['requests'].append({
                'image': img,
                'imageInputType': input_type,
                'features': features,
                'sdkVersion': self._sdk_version,
                'maxResults': max_results
            })

        headers = {
            'Authorization': f'Bearer {self._api_key}'
        }

        async with aiohttp.ClientSession() as session:
            resp = await session.post(
                self._api_url,
                headers=headers,
                json=request_data
            )

            result = await resp.json()

            if resp.status != 200:
                if 'detail' not in result:
                    result['detail'] = f"Error occurred - status code {resp.status}."
                return result

            if self._use_local_face_detection:
                restructred_result = {}
                restructred_result['debugInfo'] = result['debugInfo']
                restructred_result['performanceInfo'] = result['performanceInfo']
                restructred_result['images'] = []
                idx = 0
                # iterate over images
                for i, info_about_img in enumerate(info_about_local_images):
                    # iterate over faces in image
                    n = info_about_img['faces_per_img']
                    restructred_result['images'].append({'faces': []})
                    for j in range(0, n):
                        current_face = result['images'][idx]['faces'][0]

                        rect = {
                            'x1': info_about_img['rects'][j][0],
                            'y1': info_about_img['rects'][j][1],
                            'x2': info_about_img['rects'][j][2],
                            'y2': info_about_img['rects'][j][3]
                        }
                        current_face['boundingBox'] = rect
                        restructred_result['images'][i]['faces'].append(
                            current_face)
                        idx += 1

                    restructred_result['images'][i]['debugInfo'] = None
                    restructred_result['images'][i]['performanceInfo'] = None

                result = restructred_result

            result = self._adjust_face_rects_to_original_size(
                result_dict=result, resize=resize, orignal_images=images)
            return result

    def _adjust_face_rects_to_original_size(self, result_dict, resize=None, orignal_images=[]):
        if resize is None:
            return result_dict

        for i, o_img in enumerate(orignal_images):
            (_, __annotations__, r) = _get_resized_shape(
                resize=resize, original_img_shape=o_img.shape)

            for j, face in enumerate(result_dict['images'][i]['faces']):
                result_dict['images'][i]['faces'][j]['boundingBox']['x1'] = int(
                    result_dict['images'][i]['faces'][j]['boundingBox']['x1'] / r)
                result_dict['images'][i]['faces'][j]['boundingBox']['x2'] = int(
                    result_dict['images'][i]['faces'][j]['boundingBox']['x2'] / r)
                result_dict['images'][i]['faces'][j]['boundingBox']['y1'] = int(
                    result_dict['images'][i]['faces'][j]['boundingBox']['y1'] / r)
                result_dict['images'][i]['faces'][j]['boundingBox']['y2'] = int(
                    result_dict['images'][i]['faces'][j]['boundingBox']['y2'] / r)

        return result_dict

    def _requires_local_processing(self, resize):
        return resize is not None or self._use_local_face_detection or self._use_local_face_embedding
