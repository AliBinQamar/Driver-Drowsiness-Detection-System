"""
Automatic dlib Model Downloader
Downloads and extracts the facial landmark model needed for drowsiness detection.
Run this script once before running code.py
"""

import bz2
import urllib.request
import os
import sys

def download_model():
    """Download and extract the dlib facial landmark model."""
    
    model_url = "http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2"
    compressed_file = "shape_predictor_68_face_landmarks.dat.bz2"
    final_file = "shape_predictor_68_face_landmarks.dat"
    
    # Check if model already exists
    if os.path.exists(final_file):
        print(f"✓ Model file '{final_file}' already exists!")
        return True
    
    try:
        print("Downloading facial landmark model...")
        print(f"URL: {model_url}")
        print("This may take a few minutes (file size: ~99 MB)")
        print("-" * 60)
        
        # Download with progress
        def download_progress(block_num, block_size, total_size):
            downloaded = block_num * block_size
            if total_size > 0:
                percent = (downloaded / total_size) * 100
                print(f"\rProgress: {percent:.1f}% ({downloaded / (1024*1024):.1f} MB)", end="")
        
        urllib.request.urlretrieve(model_url, compressed_file, download_progress)
        print("\n✓ Download complete!")
        
        print("\nExtracting model...")
        with bz2.open(compressed_file, 'rb') as f_in:
            with open(final_file, 'wb') as f_out:
                f_out.write(f_in.read())
        print(f"✓ Model extracted to '{final_file}'")
        
        # Clean up compressed file
        os.remove(compressed_file)
        print(f"✓ Cleaned up temporary file")
        
        print("\n" + "=" * 60)
        print("SUCCESS! Model ready to use.")
        print(f"You can now run: python code.py")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n✗ ERROR: {str(e)}")
        print("\nManual download alternative:")
        print(f"1. Visit: {model_url}")
        print("2. Extract the .bz2 file using 7-Zip or WinRAR")
        print("3. Place 'shape_predictor_68_face_landmarks.dat' in this directory")
        return False


if __name__ == "__main__":
    print("Driver Drowsiness Detection - Model Downloader")
    print("=" * 60)
    
    success = download_model()
    sys.exit(0 if success else 1)
