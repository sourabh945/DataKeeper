# DataKeeper

DataKeeper is a semi-automatic program designed to back up files to Google Drive using the Google Drive API. It ensures that every file is reliably backed up and includes built-in version control.

## Overview

The tool requires manual execution and does not run automatically in the background. Upon running, it compares your local directory with the remote Google Drive backup, providing a clear summary of differences before performing any synchronization actions.

## Key Features

* **Pre-built Executable:** A ready-to-use executable is available for Ubuntu users. This version is designed for ease of use and bypasses the need for you to provide your own Google API client ID or client secret.
* **Version Control & File Tracking:** It tracks file versions, file sizes, and modification times to intelligently determine which files have been modified between your local machine and Google Drive.
* **Interactive Synchronization:** After indexing and comparing both sources, the program displays a detailed breakdown of total, new, deleted, and modified folders/files. It then prompts you to choose the desired operation:
1. Upload only
2. Download only
3. Upload and then download
4. Cancel


* **Asynchronous Execution:** Utilizes asynchronous routines (`async_run`) to process heavy tasks like folder creation and file transfers efficiently.

## How it Works

1. **Initialization:** The application loads configurations, backend access tokens, and connects to Google Drive.
2. **Indexing:** It recursively indexes both the specified local folder path and the corresponding remote folder on Google Drive to create a structural map.
3. **Comparison:** The internal engine cross-references items to flag files that require updating, checking differences in file size and modification timestamps.
4. **Execution:** Based on your selected option from the menu, the tool automatically handles necessary directory creation and executes the required upload or download jobs.

## Downloads

* **Ubuntu Executable:** [https://github.com/sourabh945/DataKeeper/tree/main/Executables/Ubuntu/DataKeeper](https://github.com/sourabh945/DataKeeper/tree/main/Executables/Ubuntu/DataKeeper)
