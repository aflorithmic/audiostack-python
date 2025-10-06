import audiostack

audiostack.api_key = "your key"

# Upload a file. It's important that uploadPath contains the file extension. Upload file will be available to your organisation.
file = audiostack.Files.File.create(
    localPath="example.mp3", uploadPath="mydir/file.mp3", fileName="file.mp3"
)

print("The file ID is:", file.fileId)

# Get file details
file_details = audiostack.Files.File.get(fileId=file.fileId)

print("File details:", file_details.fileName, file_details.size, file_details.status)

# Delete the file
audiostack.Files.File.delete(fileId=file.fileId)
