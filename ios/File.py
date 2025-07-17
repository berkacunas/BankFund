import os

def list_files(dir) -> list:
    
    files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir, f))]
    
    return files

def file_count(dir) -> int:
    
    count = len([entry for entry in os.listdir(dir) if os.path.isfile(os.path.join(dir, entry))])
    
    return count

def subdir_count(dir) -> int:
    
    count = len([entry for entry in os.listdir(dir) if os.path.isdir(os.path.join(dir, entry))])
    