import os
import subprocess
from pathlib import Path


class MP4Driver:
    def __init__(self, mount_point: str = "/media"):
        # Initialize with a base mount point. 
        # Using '/media' allows the driver to find USBs regardless of the username.
        self.mount_point = Path(mount_point)

    
    def list_mp4_files(self) -> list[str]:
        """
        List all MP4 files found dynamically in any subfolder of the mount point.
        Returns a list of file names (strings).
        Addresses the static pathing bug by searching recursively.
        """
        if not self.mount_point.exists():
            return []

        # Uses rglob for recursive, case-insensitive-like search (TODO: Use Path)
        # Finds .mp4 and .MP4 files
        return [str(p) for p in self.mount_point.rglob("*.[mM][pP]4")]

    def get_file_names(self) -> list[str]:
        """Return only the file names (without paths)."""
        return [os.path.basename(f) for f in self.list_mp4_files()]

    def print_mp4_files(self):
        """Print the names of all MP4 files found."""
        files = self.get_file_names()
        if not files:
            print("No MP4 files found.")
        else:
            print("MP4 Files found:")
            for f in files:
                print(f)

    def get_full_path(self, filename: str) -> str:
        """
        Returns the full system path for a given filename.
        Crucial for passing paths to the Projector module.
        """
        for full_path in self.list_mp4_files():
            if os.path.basename(full_path) == filename:
                return full_path
        raise FileNotFoundError(f"File {filename} not found.")

    def safe_eject(self) -> bool:
        """
        Safely unmounts USB drives found in the mount point.
        Call this from the Rotary Encoder 'click' event.
        """
        try:
            # Identify subdirectories (the actual mounted drives)
            mounts = [p for p in self.mount_point.iterdir() if p.is_dir()]
            
            for mnt in mounts:
                # Sync ensures all data is written before unmounting
                subprocess.run(["/usr/bin/sync"], check=True)
                # Unmount the specific drive
                subprocess.run(["/usr/bin/umount", str(mnt)], check=True)
                print(f"Safe to remove drive at: {mnt}")
            return True
        except subprocess.CalledProcessError:
            print("Eject failed: Drive is likely busy (video still playing?)")
            return False
        except Exception as e:
            print(f"Error during eject: {e}")
            return False

# Example Usage:
if __name__ == "__main__":
    # Create an MP4Driver instance with the USB mount point
    driver = MP4Driver(mount_point="/media")

    # List MP4 file names
    mp4_files = driver.get_file_names()
    print(mp4_files)

    # Or print them directly
    driver.print_mp4_files()
