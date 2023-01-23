import os
import tempfile
import ffmpeg
import numpy as np
import uuid
from skimage import transform

from salt_shaker.image import Image
from salt_shaker.image_actions.image_action import ImageAction
from salt_shaker.raw_data import RawDataVideo
from salt_shaker.image_batch import ImageBatch


class Gifify(ImageAction):
    def __init__(self):
        super().__init__()

    def process(self, input_batch: ImageBatch) -> ImageBatch:
        """
        takes list of images and returns a gif
        """
        # validate shape and create raw_video
        if not input_batch.is_all_img_same_shape():
            raise Exception("not all images are same size in input")
        rdv = RawDataVideo()
        for img in input_batch.images:
            rdv.add_frame(img.image_data)

        # python scoping allows me to get away with this
        height = img.image_data.height
        width = img.image_data.width

        vid_ndarr = rdv.as_ndarray()

        # TODO - look at https://github.com/kkroening/ffmpeg-python/blob/master/examples/README.md#tensorflow-streaming
        # and make this buffered

        # working video output
        # out, _ = (
        #     ffmpeg.input(
        #         "pipe:",
        #         video_size='120x120',
        #         format='rawvideo',
        #         pix_fmt='rgba'
        #     )
        #     .output(
        #         # rgb8 is correct, rgba is 4x more data so need to store differently
        #         # rgb8 is not correct, that's monochrome. rgba is 32 bit + alpha
        #         "pipe:", format="rawvideo", pix_fmt="rgba"#pix_fmt="rgba"
        #     ).overwrite_output()  # outputs 25 frames of 120x120x120x4
        #     .run(capture_stdout=True, input=vid_ndarr.astype(np.uint8).tobytes())
        # )

        out, _ = (
            ffmpeg.input(
                "pipe:",
                s=f"{height},{width}",
                format="rawvideo",
                pix_fmt="rgba",
                framerate=5,
            )
            # .filter(
            #
            # )
            .output("pipe:", format="gif").run(
                capture_stdout=True, input=vid_ndarr.astype(np.uint8).tobytes()
            )
        )

        # output_batch = ImageBatch()
        # output_batch.add_image(Image.create_from_bytes(out, height=120, width=120))
        return out  # output_batch
