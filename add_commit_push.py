import os
import time
import subprocess
from typing import Dict

def git_add_commit_push_with_timing(
    directory: str,
    commit_message: str,
    remote: str = "origin",
    branch: str = "main"
) -> Dict[str, float]:
    """
    Perform git add, commit, and push operations on a directory and measure timing.
    
    Args:
        directory (str): Path to the local directory containing the git repository
        commit_message (str): Commit message for the changes
        remote (str): Remote repository name (default: "origin")
        branch (str): Branch name to push to (default: "main")
    
    Returns:
        Dict[str, float]: Dictionary containing timing information for each operation
        
    Raises:
        FileNotFoundError: If the directory doesn't exist
        subprocess.CalledProcessError: If any git command fails
        Exception: If the directory is not a git repository
    """
    
    # Validate directory exists
    if not os.path.exists(directory):
        raise FileNotFoundError(f"Directory '{directory}' does not exist")
    
    # Check if directory is a git repository
    git_dir = os.path.join(directory, '.git')
    if not os.path.exists(git_dir):
        raise Exception(f"Directory '{directory}' is not a git repository")
    
    # Store original working directory
    original_dir = os.getcwd()
    timing_results = {}
    
    try:
        # Change to the target directory
        os.chdir(directory)
        
        # Start total timing
        total_start_time = time.time()
        
        # Git add
        print("Starting git add...")
        add_start_time = time.time()
        subprocess.run(['git', 'add', '.'], check=True, capture_output=True, text=True)
        add_end_time = time.time()
        timing_results['git_add'] = add_end_time - add_start_time
        print(f"Git add completed in {timing_results['git_add']:.4f} seconds")
        
        # Git commit
        print("Starting git commit...")
        commit_start_time = time.time()
        subprocess.run(['git', 'commit', '-m', commit_message], check=True, capture_output=True, text=True)
        commit_end_time = time.time()
        timing_results['git_commit'] = commit_end_time - commit_start_time
        print(f"Git commit completed in {timing_results['git_commit']:.4f} seconds")
        
        # Git push
        print("Starting git push...")
        push_start_time = time.time()
        subprocess.run(['git', 'push', remote, branch], check=True, capture_output=True, text=True)
        push_end_time = time.time()
        timing_results['git_push'] = push_end_time - push_start_time
        print(f"Git push completed in {timing_results['git_push']:.4f} seconds")
        
        # Calculate total time
        total_end_time = time.time()
        timing_results['total_time'] = total_end_time - total_start_time
        
        print(f"\n--- Summary ---")
        print(f"Git add:    {timing_results['git_add']:.4f} seconds")
        print(f"Git commit: {timing_results['git_commit']:.4f} seconds")
        print(f"Git push:   {timing_results['git_push']:.4f} seconds")
        print(f"Total time: {timing_results['total_time']:.4f} seconds")
        
        return timing_results
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
        print(f"Error output: {e.stderr if e.stderr else 'No error output'}")
        raise
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
    finally:
        # Always return to original directory
        os.chdir(original_dir)

if __name__ == "__main__":
    # repo = "https://github.com/shloknatarajan/dca-tasks-100k"
    # subtask = "tasks/tasks_copy_1/acl-permissions-inheritance"
    # clone_time = measure_git_clone(repo, "bench_clone")
    # print(f"Clone took {clone_time:.2f} seconds")
    # sparse_time = time_sparse_clone(repo_url=repo, subpath=subtask)
    # print(f"Single Task took {sparse_time:.2f} seconds")
    directory = "dca-tasks-10k"
    git_add_commit_push_with_timing(directory, "feat: add tasks")