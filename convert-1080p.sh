#!/bin/bash

# Set the directory containing the files
input_dir="./"
output_dir="$input_dir/1080p"

# Create output directory if it doesn't exist
mkdir -p "$output_dir"

# Loop through all .mkv files in the directory
for file in "$input_dir"/*.mkv; do
    # Check if the file exists and ends with .mkv
    if [ -e "$file" ] && [[ "$file" == *.mkv ]]; then
        # Extract the filename without extension
        filename=$(basename -- "$file")
        filename_no_ext="${filename%.*}"
        
        # Run ffmpeg command to convert the file
        ffmpeg -i "$file" -vf scale=1920:1080 -c:a copy -c:v hevc_nvenc -c:s copy -map 0 "$output_dir/$filename_no_ext-1080p.mkv"
        
        echo "Conversion complete for $filename"
    fi
done

echo "All conversions complete."

