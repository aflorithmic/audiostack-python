import audiostack

audiostack.api_key = "your key"

# Upload a file. It's important that uploadPath contains the file extension. Upload file will be available to your organisation.
file = audiostack.Content.File.create(
    localPath="example.mp3", uploadPath="mydir/file.mp3", fileType="audio"
)

print("The file ID is:", file.fileId)

# List files in a directory
files = audiostack.Content.File.search(path="mydir")

print("Files found:", files.items)

# Delete the file
file.delete()
