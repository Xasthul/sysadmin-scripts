#!/bin/bash

# This is a simple backup script with logging.
# It compresses the archive with all files that are given as arguments to the script.
# All errors that occur are being written to the log file and shown after script's work.

backup_dir="/path/to/backup/directory"

backup_file=$(date +%Y-%m-%d)-backup.tar.gz

if [ -f $backup_dir/$backup_file ]; then
	i=1
	while [ -f $backup_dir/$backup_file-$i ]; do
		((i++))
	done
	backup_file=$backup_file-$i
fi

log_file=$backup_dir/backup.log

mkdir -p $backup_dir

touch $log_file

tar -czf $backup_dir/$backup_file $@ > $log_file 2>&1

if [ -f $backup_dir/$backup_file ]; then
	echo "Backup successful! Filename: $backup_file"
else
	echo "Backup failed!"
fi

if grep -q "tar: " $log_file; then
	echo "Error detected in the log file: "
	grep "tar: " $log_file
fi
