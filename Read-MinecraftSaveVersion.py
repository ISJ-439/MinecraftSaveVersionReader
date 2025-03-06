import sys
import zipfile
import nbtlib
import tempfile
import os

def get_minecraft_version(zip_path):
    # Open ZIP archive containing Minecraft world data <button class="citation-flag" data-index="10">
    with zipfile.ZipFile(zip_path, 'r') as world_zip:
        # Locate level.dat file (supports nested directories) <button class="citation-flag" data-index="8">
        level_dat = next((f for f in world_zip.namelist() 
                         if f.endswith('level.dat')), None)
        if not level_dat:
            raise FileNotFoundError("level.dat not found in ZIP archive")

        # Read raw NBT data bytes from ZIP entry <button class="citation-flag" data-index="7">
        with world_zip.open(level_dat) as f:
            file_data = f.read()

    # Create temporary file to work around nbtlib's file handling limitations <button class="citation-flag" data-index="3"><button class="citation-flag" data-index="6">
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(file_data)
        tmp_path = tmp.name

    try:
        # Load NBT data using file path (required by older nbtlib versions) <button class="citation-flag" data-index="3"><button class="citation-flag" data-index="5">
        nbt_data = nbtlib.load(tmp_path)
    finally:
        # Clean up temporary file to avoid leftover artifacts <button class="citation-flag" data-index="6">
        os.unlink(tmp_path)

    try:
        # Parse Java Edition version information <button class="citation-flag" data-index="4">
        version = nbt_data['Data']['Version']['Name']
        data_version = nbt_data['Data']['Version']['Id']
    except KeyError:
        # Handle Bedrock Edition format differences <button class="citation-flag" data-index="4">
        version = nbt_data.get('header', {}).get('Version', 'Unknown')
        data_version = nbt_data.get('header', {}).get('StorageVersion', -1)

    return {
        'version_name': version,
        'data_version': data_version
    }

if __name__ == '__main__':
    # Validate command-line arguments <button class="citation-flag" data-index="1">
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <path_to_world_zip>")
        sys.exit(1)
    try:
        # Process the world file and output version information <button class="citation-flag" data-index="8">
        result = get_minecraft_version(sys.argv[1])
        print(f"Minecraft Version: {result['version_name']}")
        print(f"Data Version: {result['data_version']}")
    except Exception as e:
        # Catch and report all errors with proper exit code <button class="citation-flag" data-index="7">
        print(f"Error: {str(e)}")
        sys.exit(1)
