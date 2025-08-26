import zipfile
import shutil
from pathlib import Path
import tempfile
from tqdm import tqdm

def duplicate_tasks(n_copies: int, output_dir: str = "duplicated_tasks") -> None:
    """
    Extract tasks.zip and create n copies of the tasks in a new folder.
    
    Args:
        n_copies: Number of copies to create
        output_dir: Name of the output directory to create
    """
    repo_root = Path(__file__).parent
    tasks_zip_path = repo_root / "tasks.zip"
    output_path = repo_root / output_dir
    
    if not tasks_zip_path.exists():
        raise FileNotFoundError(f"tasks.zip not found at {tasks_zip_path}")
    
    # Remove output directory if it exists
    if output_path.exists():
        shutil.rmtree(output_path)
    
    output_path.mkdir()
    
    # Extract tasks.zip to temporary directory to see its structure
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        
        # Extract the zip file, excluding __MACOSX folders
        with zipfile.ZipFile(tasks_zip_path, 'r') as zip_ref:
            for member in zip_ref.infolist():
                if not member.filename.startswith('__MACOSX/'):
                    zip_ref.extract(member, temp_path)
        
        # Find the tasks folder in the extracted content
        tasks_source = temp_path / "tasks"
        if not tasks_source.exists():
            # If tasks folder doesn't exist at root, look for it
            for item in temp_path.iterdir():
                if item.is_dir() and item.name == "tasks":
                    tasks_source = item
                    break
            else:
                raise FileNotFoundError("No 'tasks' folder found in the extracted archive")
        
        # Create n copies
        for i in tqdm(range(n_copies)):
            copy_name = f"tasks_copy_{i+1}"
            copy_path = output_path / copy_name
            
            # Copy only the tasks content to each copy directory
            shutil.copytree(tasks_source, copy_path)
    
    print(f"Created {n_copies} copies of tasks in {output_path}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python duplicate_tasks.py <number_of_copies>")
        sys.exit(1)
    
    try:
        n = int(sys.argv[1])
        if n <= 0:
            raise ValueError("Number of copies must be positive")
        duplicate_tasks(n)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
