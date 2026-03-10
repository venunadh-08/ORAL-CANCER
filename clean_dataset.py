import os
import shutil

base_dir = r"c:\Users\venun\OneDrive\Desktop\PAD\OralCancer"
cancer_dir = os.path.join(base_dir, "CANCER")
non_cancer_dir = os.path.join(base_dir, "NON CANCER")

bad_keywords = [
    'symptom', 'treatment', 'guide', 'youtube', 'screenshot', 'fig.', 'fig1', 'what_does',
    'article', 'fact', 'credit', 'reference', 'preview', 'protect', 'youtube'
]

mislabel_keywords = ['cancer', 'carcinoma', 'tumor']

def clean_directory(directory, is_non_cancer=False):
    if not os.path.exists(directory):
        print(f"Directory not found: {directory}")
        return

    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if not os.path.isfile(filepath):
            continue

        filename_lower = filename.lower()
        
        # 1. Check for noisy/scraped files to delete
        should_delete = False
        for kw in bad_keywords:
            if kw in filename_lower:
                should_delete = True
                break
        
        if should_delete:
            print(f"Deleting noisy file: {filename}")
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
            continue
            
        # 2. Check for mislabeled files in NON CANCER to move to CANCER
        if is_non_cancer:
            should_move = False
            for kw in mislabel_keywords:
                if kw in filename_lower:
                    should_move = True
                    break
            
            if should_move:
                dest_path = os.path.join(cancer_dir, filename)
                print(f"Moving mislabeled file to CANCER: {filename}")
                try:
                    shutil.move(filepath, dest_path)
                except Exception as e:
                    print(f"Error moving {filename}: {e}")

print("Cleaning CANCER directory...")
clean_directory(cancer_dir, is_non_cancer=False)

print("\nCleaning NON CANCER directory...")
clean_directory(non_cancer_dir, is_non_cancer=True)

print("\nDone cleaning OralCancer dataset.")
