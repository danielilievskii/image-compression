import cv2
import numpy as np

# RLE Compression and Decompression
def rle_compress_and_save(image, filename):
    compressed_data = []
    height, width = image.shape

    for i in range(height):
        run_length = 1
        current_pixel = image[i, 0]

        for j in range(1, width):
            if image[i, j] == current_pixel:
                run_length += 1
            else:
                compressed_data.append((run_length, current_pixel))
                current_pixel = image[i, j]
                run_length = 1

        compressed_data.append((run_length, current_pixel))

    try:
        with open(filename, 'w') as f:
            f.write(f"{height} {width}\n")
            for run_length, pixel_value in compressed_data:
                f.write(f"{run_length} {pixel_value}\n")
        print(f"Compressed data saved to '{filename}'")
    except Exception as e:
        print(f"Error saving compressed data: {e}")

def load_and_rle_decompress(filename):
    compressed_data = []
    try:
        with open(filename, 'r') as f:
            height, width = map(int, f.readline().strip().split())
            for line in f:
                run_length, pixel_value = map(int, line.strip().split())
                compressed_data.append((run_length, pixel_value))
    except Exception as e:
        print(f"Error loading compressed data: {e}")
        return None

    decompressed_image = np.zeros((height, width), dtype=np.uint8)
    current_row = 0
    current_col = 0

    for run_length, pixel_value in compressed_data:
        for _ in range(run_length):
            decompressed_image[current_row, current_col] = pixel_value
            current_col += 1
            if current_col == width:
                current_col = 0
                current_row += 1
                if current_row == height:
                    break

    return decompressed_image

# JPEG Compression

def jpeg_compress(image_path, output_path, jpeg_quality):
    if not (0 <= jpeg_quality <= 100):
        raise ValueError("JPEG quality must be between 0 and 100")

    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"The image at {image_path} could not be found or read.")

    success = cv2.imwrite(output_path, image, [cv2.IMWRITE_JPEG_QUALITY, jpeg_quality-5])
    if not success:
        raise IOError(f"Failed to save the compressed image to {output_path}")

    print(f"Image saved as {output_path} with JPEG quality {jpeg_quality}")