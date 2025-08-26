# Sparse checkout a single task 1k times and see how long it takes / if you get an error or timeout
import time
import shutil
import subprocess
from pathlib import Path
from tqdm import tqdm
from sparse_checkout_metrics import time_sparse_clone

def ping_repo(repo_task_suffix: str, n_tries: int = 500):
    # Check to make sure the suffix is 1k, 10k, 50k, 100k
    if repo_task_suffix not in ["1k", "10k", "50k", "100k"]:
        raise ValueError("Repo task suffix must be 1k, 10k, 50k, or 100k")
    repo_1k = f"https://github.com/shloknatarajan/dca-tasks-{repo_task_suffix}"
    subtask = f"tasks/tasks_copy_1/"
    # start timer
    start_time = time.time()
    for i in tqdm(range(n_tries)):
        sparse_time_1k = time_sparse_clone(repo_url=repo_1k, subpath=subtask, dest=f"{repo_task_suffix}-sparse-clone-ping", verbose=False)
        # remove the sparse clone
        shutil.rmtree(f"{repo_task_suffix}-sparse-clone-ping")
    end_time = time.time()
    print(f"Getting single task {n_tries} times took {end_time - start_time:.2f} seconds from {repo_task_suffix} repo")

if __name__ == "__main__":
    try:
        ping_repo("1k")
    except Exception as e:
        print(e)
        # Save error to file
        with open("ping_rate_test_error.txt", "a") as f:
            f.write(f"1k error: {e}\n")