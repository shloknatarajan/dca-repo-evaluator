import subprocess
import time
from pathlib import Path
import shutil
from typing import Dict
import os
from sparse_checkout_metrics import time_sparse_clone

def measure_git_clone(repo_url: str, dest: str = None) -> float:
    """
    Clone a Git repository and return the time taken (in seconds).
    
    Args:
        repo_url: The GitHub/Git URL of the repository to clone.
        dest: Optional destination folder name.
    """
    cmd = ["git", "clone", repo_url]
    if dest:
        cmd.append(dest)

    start = time.perf_counter()
    subprocess.run(cmd, check=True)
    end = time.perf_counter()

    return end - start

# Example usage:
def main():
    # 1k
    repo_1k = "https://github.com/shloknatarajan/dca-tasks-1k"
    clone_time_1k = measure_git_clone(repo_1k, "1k-clone")
    print(f"1k clone took {clone_time_1k:.2f} seconds")
    
    # Measure sparse clone time
    subtask = "tasks/tasks_copy_1/acl-permissions-inheritance"
    sparse_time_1k = time_sparse_clone(repo_url=repo_1k, subpath=subtask, dest="1k-sparse-clone")
    print(f"1k single task took {sparse_time_1k:.2f} seconds")

    # 10k
    repo_10k = "https://github.com/shloknatarajan/dca-tasks-10k"
    clone_time_10k = measure_git_clone(repo_10k, "10k-clone")
    print(f"10k clone took {clone_time_10k:.2f} seconds")
    
    # Measure sparse clone time
    sparse_time_10k = time_sparse_clone(repo_url=repo_10k, subpath=subtask, dest="10k-sparse-clone")
    print(f"10k single task took {sparse_time_10k:.2f} seconds")

    # 50k
    repo_50k = "https://github.com/shloknatarajan/dca-tasks-50k"
    clone_time_50k = measure_git_clone(repo_50k, "50k-clone")
    print(f"50k clone took {clone_time_50k:.2f} seconds")
    
    # Measure sparse clone time
    sparse_time_50k = time_sparse_clone(repo_url=repo_50k, subpath=subtask, dest="50k-sparse-clone")
    print(f"50k single task took {sparse_time_50k:.2f} seconds")

    # 100k
    repo_100k = "https://github.com/shloknatarajan/dca-tasks-100k"
    clone_time_100k = measure_git_clone(repo_100k, "100k-clone")
    print(f"100k clone took {clone_time_100k:.2f} seconds")
    
    # Measure sparse clone time
    sparse_time_100k = time_sparse_clone(repo_url=repo_100k, subpath=subtask, dest="100k-sparse-clone")
    print(f"100k single task took {sparse_time_100k:.2f} seconds")

    # Save results to a CSV file
    with open("clone_checkout_metrics.csv", "w") as f:
        f.write("repo,clone_time,sparse_time\n")
        f.write(f"1k,{clone_time_1k},{sparse_time_1k}\n")
        f.write(f"10k,{clone_time_10k},{sparse_time_10k}\n")
        f.write(f"50k,{clone_time_50k},{sparse_time_50k}\n")
        f.write(f"100k,{clone_time_100k},{sparse_time_100k}\n")
    
if __name__ == "__main__":
    main()