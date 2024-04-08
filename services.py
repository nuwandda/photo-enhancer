import schemas as _schemas
import os
from PIL import Image
from io import BytesIO
import uuid
import numpy as np
import base64
from enhancer.enhancer import Enhancer


TEMP_PATH = 'temp'
ENHANCE_METHOD = os.getenv('METHOD')
BACKGROUND_ENHANCEMENT = os.getenv('BACKGROUND_ENHANCEMENT')
if ENHANCE_METHOD is None:
    ENHANCE_METHOD = 'gfpgan'

if BACKGROUND_ENHANCEMENT is None:
    BACKGROUND_ENHANCEMENT = True
else:
    BACKGROUND_ENHANCEMENT = True if BACKGROUND_ENHANCEMENT == 'True' else False

enhancer = Enhancer(method=ENHANCE_METHOD, background_enhancement=BACKGROUND_ENHANCEMENT, upscale=2)


async def enhance(enhanceBase: _schemas._EnhanceBase) -> Image:
    init_image = np.array(Image.open(BytesIO(base64.b64decode(enhanceBase.encoded_base_img[0]))))
    restored_image = enhancer.enhance(init_image)

    final_image = Image.fromarray(restored_image)
    buffered = BytesIO()
    final_image.save(buffered, format="JPEG")
    encoded_img = base64.b64encode(buffered.getvalue())
    
    return encoded_img
        