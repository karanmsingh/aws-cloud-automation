#!/usr/bin/env python3
import os
import time
import logging
from datetime import datetime, timedelta

# ========== CONFIGURATION ==========
EFS_MOUNT_PATH = "/efs"   # Change to your EFS mount path
DAYS_OLD = 30                 # Delete files older than 30 days
DRY_RUN = True               # Set to True to test without deleting
LOG_FILE = "./efs_cleanup.log"
# ===================================


# Setup logging
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

cutoff_time = time.time() - (DAYS_OLD * 86400)
deleted_files = 0
skipped_files = 0
errors = 0

def delete_old_files():
    global deleted_files, skipped_files, errors

    if not os.path.exists(EFS_MOUNT_PATH):
        logging.error(f"EFS mount path does not exist: {EFS_MOUNT_PATH}")
        return

    logging.info(f"Starting cleanup for files older than {DAYS_OLD} days")

    for root, dirs, files in os.walk(EFS_MOUNT_PATH):
        for filename in files:
            file_path = os.path.join(root, filename)

            try:
                file_mtime = os.stat(file_path).st_mtime

                if file_mtime < cutoff_time:
                    if DRY_RUN:
                        logging.info(f"[DRY RUN] Would delete: {file_path}")
                        skipped_files += 1
                    else:
                        os.remove(file_path)
                        deleted_files += 1
                        logging.info(f"Deleted: {file_path}")
                else:
                    skipped_files += 1

            except FileNotFoundError:
                continue
            except PermissionError:
                logging.warning(f"Permission denied: {file_path}")
                errors += 1
            except Exception as e:
                logging.error(f"Error deleting {file_path}: {str(e)}")
                errors += 1

    logging.info("Cleanup complete")
    logging.info(f"Deleted Files: {deleted_files}")
    logging.info(f"Skipped Files: {skipped_files}")
    logging.info(f"Errors: {errors}")


if __name__ == "__main__":
    delete_old_files()
