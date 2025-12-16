from pathlib import Path
from datetime import datetime 
import os, sys
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import csv 


def export_to_csv(records, output_path): 

   if not records: 
       print("No records to export")
       return 
   

   # Add the field names from the first record 
   fieldnames = list(records[0].keys())

   with open(output_path, "w", newline="", encoding="utf-8") as f: 
       
       writer = csv.DictWriter(f, fieldnames=fieldnames)
       writer.writeheader()
       for record in records: 
           writer.writerow(record)
    
   print(f"Exported {len(records)} records to {output_path}")


   
# Hard code folder path for now
folder_path = Path(r"C:\Users\marcm\OneDrive\Desktop\Python_Forensics_Project\Photos")
image_path = Path(r"C:\Users\marcm\OneDrive\Desktop\Python_Forensics_Project\Photos\Photo_1\IMG_1681.PNG")
print("Scanning:", folder_path)
print("Exists:", folder_path.exists())

im = Image.open(image_path)

# Define which file images count as images 
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff"}


#create a list that will one record dictionary per image file

results = []

if not folder_path.exists(): 
    print("Folder does not exist. Check the path ad try again.")

else: 

    # Walk through all files 
    for file in folder_path.rglob("*"): 

        if not file.is_file(): 
            continue
        
        # Skip if the extension is not an image
        if file.suffix.lower() not in IMAGE_EXTS: 
            continue

        # Ask the OS for metadata about this file

        file_stat = file.stat()

        # Extract raw values 

        size_bytes = file_stat.st_size
        modified_ts = file_stat.st_mtime
        created_ts = file_stat.st_ctime

        # Convert timestamps to readable code 

        modified_dt = datetime.fromtimestamp(modified_ts)
        created_ts = datetime.fromtimestamp(created_ts)

        # Convert to a string

        modified_str = modified_dt.isoformat()
        created_str = created_ts.isoformat()

        record = { 

            "path": str(file), 
            "size_bytes": size_bytes, 
            "modified_time": modified_str,
            "created_time": created_str, 

        }

        results.append(record)

        # Quick summarry of the infromation 
        print("File", file)
        print(" Size (bytes):", size_bytes)
        print(" Modified:    ", modified_str)
        print(" created:     ", created_str)

    print(f"Finished. Collected metatdata for {len(results)} image files.")

    if results:

        export_to_csv(results, "metadata_report.csv")









            


