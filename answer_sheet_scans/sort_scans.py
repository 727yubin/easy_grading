import os
import cv2
import argparse
import shutil
import concurrent.futures

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Detect QR code in the image
    detector = cv2.QRCodeDetector()
    data, bbox, _ = detector.detectAndDecode(gray)
    
    if data:
        print(f"QR code detected: {data}")
        return data
    else:
        print(f"No QR code found in {image_path}")
        return None

def copy_image_to_folder(image_path, destination_folder, new_name=None):
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)
    
    if new_name:
        new_image_path = os.path.join(destination_folder, new_name)
    else:
        new_image_path = os.path.join(destination_folder, os.path.basename(image_path))
    
    shutil.copy2(image_path, new_image_path)
    print(f"Copied {image_path} to {new_image_path}")

def process_image(image_path, parent_folder, manual_sort_folder):
    qr_data = read_qr_code(image_path)
    
    if qr_data:
        try:
            student_id, page_number = qr_data.split('_')
            destination_folder = os.path.join(parent_folder, student_id)
            new_name = f"{page_number}.png"
            copy_image_to_folder(image_path, destination_folder, new_name)
        except ValueError:
            print(f"QR code format is incorrect in {image_path}")
            copy_image_to_folder(image_path, manual_sort_folder)
    else:
        copy_image_to_folder(image_path, manual_sort_folder)

def process_images(folder_path, max_workers):
    parent_folder = os.path.dirname(folder_path)
    manual_sort_folder = os.path.join(parent_folder, 'manual-sort')

    image_paths = [os.path.join(folder_path, filename) for filename in os.listdir(folder_path) 
                   if filename.lower().endswith(('.png', '.jpg', '.jpeg'))]
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(process_image, image_path, parent_folder, manual_sort_folder) 
                   for image_path in image_paths]
        for future in concurrent.futures.as_completed(futures):
            future.result()  # To catch any exceptions raised during processing

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Sort scanned images by QR code data.")
    parser.add_argument('folder_path', type=str, help="Path to the folder containing scanned images.")
    parser.add_argument('--max_workers', type=int, default=4, help="Maximum number of concurrent threads.")
    args = parser.parse_args()
    
    process_images(args.folder_path, args.max_workers)

