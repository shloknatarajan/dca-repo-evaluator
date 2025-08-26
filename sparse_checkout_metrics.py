import time
import shutil
import subprocess
from pathlib import Path

# def time_sparse_clone(repo_url: str,
#                       subpath: str,
#                       dest: str = "sparse_clone",
#                       branch: str | None = None,
#                       verbose: bool = False) -> float:
#     """
#     Clone only one subdirectory using sparse checkout and measure elapsed time.
#     Requires Git ≥ 2.25 (for `git sparse-checkout set`).

#     Args:
#         repo_url: The repository URL.
#         subpath: The subdirectory to sparse-checkout.
#         dest: Destination folder for the clone.
#         branch: Optional branch name.
#         verbose: If True, show normal git output; if False, hide progress/info.
#                  Errors will still print either way.
#     """
#     dest_path = Path(dest)
#     if dest_path.exists():
#         shutil.rmtree(dest_path)

#     # Build clone cmd
#     cmd_clone = ["git", "clone", "--filter=blob:none", "--sparse"]
#     if not verbose:
#         cmd_clone += ["--quiet", "--no-progress"]  # hide normal progress/info
#     if branch:
#         cmd_clone += ["--branch", branch, "--single-branch"]
#     cmd_clone += [repo_url, dest]

#     # Build sparse-checkout cmd
#     cmd_sparse = ["git", "-C", dest, "sparse-checkout", "set", subpath]
#     if not verbose:
#         cmd_sparse.insert(4, "-q")  # `git sparse-checkout -q set ...`

#     # Silence stdout; leave stderr alone so real errors still appear
#     out_stream = None if verbose else subprocess.DEVNULL

#     start = time.perf_counter()

#     subprocess.run(cmd_clone, check=True, stdout=out_stream)        # errors still on stderr
#     subprocess.run(cmd_sparse, check=True, stdout=out_stream)       # errors still on stderr

#     end = time.perf_counter()
#     return end - start

def time_sparse_clone(repo_url: str,
                      subpath: str,
                      dest: str = "sparse_clone",
                      branch: str | None = None) -> float:
    """
    Clone only one subdirectory using sparse checkout and measure elapsed time.

    Requires Git ≥ 2.25 (for `git sparse-checkout set`).
    """
    dest_path = Path(dest)
    if dest_path.exists():
        shutil.rmtree(dest_path)

    # Build the clone command:
    # --filter=blob:none avoids downloading file contents you won't need
    # --sparse enables sparse checkout mode immediately
    cmd_clone = ["git", "clone", "--filter=blob:none", "--sparse", repo_url, dest]
    if branch:
        cmd_clone += ["--branch", branch, "--single-branch"]

    start = time.perf_counter()

    subprocess.run(cmd_clone, check=True)

    # Limit the working tree to your folder
    subprocess.run(["git", "-C", dest, "sparse-checkout", "set", subpath], check=True)

    end = time.perf_counter()
    return end - start

def main():
    # 1k
    repo_1k = "https://github.com/shloknatarajan/dca-tasks-1k"
    # Measure sparse clone time
    subtask = "tasks/tasks_copy_1/"
    sparse_time_1k = time_sparse_clone(repo_url=repo_1k, subpath=subtask, dest="1k-sparse-clone")
    print(f"1k 100 tasks took {sparse_time_1k:.2f} seconds")

    # 10k
    repo_10k = "https://github.com/shloknatarajan/dca-tasks-10k"
    subtask = "tasks/tasks_copy_1/"
    sparse_time_10k = time_sparse_clone(repo_url=repo_10k, subpath=subtask, dest="10k-sparse-clone")
    print(f"10k 100 tasks took {sparse_time_10k:.2f} seconds")

    # 50k
    repo_50k = "https://github.com/shloknatarajan/dca-tasks-50k"
    subtask = "tasks/tasks_copy_1/"
    sparse_time_50k = time_sparse_clone(repo_url=repo_50k, subpath=subtask, dest="50k-sparse-clone")
    print(f"50k 100 tasks took {sparse_time_50k:.2f} seconds")

    # 100k  
    repo_100k = "https://github.com/shloknatarajan/dca-tasks-100k"
    subtask = "tasks/tasks_copy_1/"
    sparse_time_100k = time_sparse_clone(repo_url=repo_100k, subpath=subtask, dest="100k-sparse-clone")
    print(f"100k 100 tasks took {sparse_time_100k:.2f} seconds")

    # Save results to a CSV file
    with open("sparse_checkout_metrics.csv", "w") as f:
        f.write("repo,sparse_time\n")
        f.write(f"1k,{sparse_time_1k}\n")
        f.write(f"10k,{sparse_time_10k}\n")
        f.write(f"50k,{sparse_time_50k}\n")
        f.write(f"100k,{sparse_time_100k}\n")
    
    # Print summary
    print(" --- Summary --- ")
    print(f"1k 100 tasks took {sparse_time_1k:.2f} seconds")
    print(f"10k 100 tasks took {sparse_time_10k:.2f} seconds")
    print(f"50k 100 tasks took {sparse_time_50k:.2f} seconds")
    print(f"100k 100 tasks took {sparse_time_100k:.2f} seconds")

if __name__ == "__main__":
    main()