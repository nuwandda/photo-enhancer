from PIL import Image
import numpy as np
from enhancer.enhancer import Enhancer
import argparse


def main(method, image_path, output_path, background_enhancement, upscale):
    # Create enhancer
    enhancer = Enhancer(method=method, background_enhancement=background_enhancement, upscale=upscale)

    image = np.array(Image.open(image_path))
    restored_image = enhancer.enhance(image)

    final_image = Image.fromarray(restored_image)
    final_image.save(output_path)


if __name__ == "__main__":
    # Create argument parser
    parser = argparse.ArgumentParser(description="Process method and image.")
    # Add method argument
    parser.add_argument("--method", type=str, required=True, help="Specify the enhance method. (gfpgan, RestoreFormer, codeformer)")
    # Add image path argument
    parser.add_argument("--image_path", type=str, required=True, help="Specify the image path.")
    # Add output image argument
    parser.add_argument("--output_path", type=str, required=True, help="Specify the output path.")
    # Add background enhancement argument
    parser.add_argument("--background_enhancement", action="store_true", help="Specify the background enhancement option.", default=True)
    # Add enhancement upscale argument
    parser.add_argument("--upscale", type=int, help="Specify the enhancement scale (2, 4).")
    # Parse the arguments
    args = parser.parse_args()
    # Call the main function with parsed arguments
    main(args.method, args.image_path, args.output_path, args.background_enhancement, args.upscale)
