import os 
import platform 


def hide_folder(folder_path):
  """Hides a folder on different operating systems.

  Args:
    folder_path: The path to the folder you want to hide.
  """

  if not os.path.exists(folder_path):
    print(f"Error: Folder not found: {folder_path}")
    return

  system = platform.system()

  if system == "Windows":
    os.system(f'attrib +h "{folder_path}"')
  elif system == "Linux" or system == "Darwin":  # Linux or macOS
    os.system(f'chflags hidden "{folder_path}"')
  else:
    print(f"Warning: Unsupported operating system: {system}")