import os
import subprocess
import time
import sys

def check_command(cmd):
    """Check if a command exists in the system."""
    try:
        subprocess.run([cmd, "--version"], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except Exception:
        return False

def main():
    project_dir = os.path.expanduser("~/esports-frontend")

    if not os.path.exists(project_dir):
        print(f"Error: Frontend project directory not found at {project_dir}")
        sys.exit(1)

    if not check_command("node"):
        print("Error: Node.js is not installed. Please install Node.js first.")
        sys.exit(1)
    if not check_command("npm"):
        print("Error: npm is not installed. Please install npm first.")
        sys.exit(1)

    try:
        print("Starting Frontend Service...")
        time.sleep(1)

        print("Installing dependencies (this may take a moment)...")
        subprocess.run(["npm", "install"], cwd=project_dir, check=True)

        print("Starting Vite development server on port 7012...")
        subprocess.run(["npm", "run", "dev", "--", "--host", "--port", "7012"], cwd=project_dir, check=True)

    except subprocess.CalledProcessError as e:
        print(f"Error during process: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\nShutting down frontend service...")
        sys.exit(0)

if __name__ == "__main__":
    main()
