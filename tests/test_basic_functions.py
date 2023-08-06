import pytest
from tests.util import compare_file_hash, TEST_INPUT_ORANGE_IMAGE_FILEPATH

from giford.image import Image
from giford.frame_batch import FrameBatch

@pytest.mark.skip('rewrite')
def test_read_write(temp_output_png: str, single_orange_image: Image):
    # simply reads and writes a file
    baseline = TEST_INPUT_ORANGE_IMAGE_FILEPATH
    single_orange_image.write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)

@pytest.mark.skip('rewrite')
def test_batch_chain(temp_output_png: str, single_orange_image: Image):
    # does image chain correctly
    baseline = TEST_INPUT_ORANGE_IMAGE_FILEPATH
    batch = FrameBatch()
    batch.add_image(single_orange_image)

    Image.create_from_frame_batch(batch).write_to_file(temp_output_png)

    assert compare_file_hash(baseline, temp_output_png)
