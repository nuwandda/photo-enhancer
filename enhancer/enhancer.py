import os
import torch 
from gfpgan import GFPGANer
from tqdm import tqdm
import cv2


class Enhancer:
    def __init__(self, method='gfpgan', background_enhancement=True, upscale=2):
        # Set up RealESRGAN for background enhancement
        if background_enhancement:
            if upscale == 2:
                if not torch.cuda.is_available(): # CPU
                    import warnings
                    warnings.warn('The unoptimized RealESRGAN is slow on CPU. We do not use it. '
                                'If you really want to use it, please modify the corresponding codes.')
                    self.bg_upsampler = None
                else:
                    from basicsr.archs.rrdbnet_arch import RRDBNet
                    from realesrgan import RealESRGANer
                    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=2)
                    self.bg_upsampler = RealESRGANer(
                        scale=2,
                        model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.2.1/RealESRGAN_x2plus.pth',
                        model=model,
                        tile=400,
                        tile_pad=10,
                        pre_pad=0,
                        half=True)  # need to set False in CPU mode
            elif upscale == 4:
                if not torch.cuda.is_available(): # CPU
                    import warnings
                    warnings.warn('The unoptimized RealESRGAN is slow on CPU. We do not use it. '
                                'If you really want to use it, please modify the corresponding codes.')
                    self.bg_upsampler = None
                else:
                    from basicsr.archs.rrdbnet_arch import RRDBNet
                    from realesrgan import RealESRGANer
                    model = RRDBNet(num_in_ch=3, num_out_ch=3, num_feat=64, num_block=23, num_grow_ch=32, scale=4)
                    self.bg_upsampler = RealESRGANer(
                        scale=4,
                        model_path='https://github.com/xinntao/Real-ESRGAN/releases/download/v0.1.0/RealESRGAN_x4plus.pth',
                        model=model,
                        tile=400,
                        tile_pad=10,
                        pre_pad=0,
                        half=True)  # need to set False in CPU mode
            else:
                raise ValueError(f'Wrong upscale constant {upscale}.')
        else:
            self.bg_upsampler = None

        # Set up GPFGAN for face enhancement
        if  method == 'gfpgan':
            self.arch = 'clean'
            self.channel_multiplier = 2
            self.model_name = 'GFPGANv1.4'
            self.url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.0/GFPGANv1.4.pth'
        elif method == 'RestoreFormer':
            self.arch = 'RestoreFormer'
            self.channel_multiplier = 2
            self.model_name = 'RestoreFormer'
            self.url = 'https://github.com/TencentARC/GFPGAN/releases/download/v1.3.4/RestoreFormer.pth'
        elif method == 'codeformer': # TODO:
            self.arch = 'CodeFormer'
            self.channel_multiplier = 2
            self.model_name = 'CodeFormer'
            self.url = 'https://github.com/sczhou/CodeFormer/releases/download/v0.1.0/codeformer.pth'
        else:
            raise ValueError(f'Wrong model version {method}.')
        
        # Determine the model path and if the model is not available, download it
        model_path = os.path.join('gfpgan/weights', self.model_name + '.pth')
        
        if not os.path.isfile(model_path):
            model_path = os.path.join('checkpoints', self.model_name + '.pth')
        
        if not os.path.isfile(model_path):
            # Download pre-trained models from url
            model_path = self.url

        self.restorer = GFPGANer(
            model_path=model_path,
            upscale=upscale,
            arch=self.arch,
            channel_multiplier=self.channel_multiplier,
            bg_upsampler=self.bg_upsampler)
        

    def check_image_dimensions(self, image):
        # Get the dimensions of the image
        height, width, _ = image.shape

        # Check if either dimension exceeds 2048 pixels
        if width > 2048 or height > 2048:
            print("Image dimensions exceed 2048 pixels.")
            return False

        else:
            print("Image dimensions are within the limit.")
            return True
        

    def enhance(self, image):
        img = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if self.check_image_dimensions(img):
            cropped_faces, restored_faces, r_img = self.restorer.enhance(
                img,
                has_aligned=False,
                only_center_face=False,
                paste_back=True)
        else:
            r_img = img
        
        r_img = cv2.cvtColor(r_img, cv2.COLOR_BGR2RGB)

        return r_img
