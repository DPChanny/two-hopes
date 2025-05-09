import requests

image_path = "local_image.jpg"  # 업로드할 이미지 파일 경로
presigned_url = "https://twohopes.s3.amazonaws.com/posts/e859a5fbc2b14b59aaf76e1d8dee7333.jpg?AWSAccessKeyId=AKIA4ORHLI5B6TM26B36&Signature=eda0QEU38Lpb6nBDNuD6oo8fCPE%3D&content-type=image%2Fjpeg&Expires=1746803483"

with open(image_path, "rb") as f:
    file_data = f.read()

response = requests.put(
    presigned_url, data=file_data, headers={"Content-Type": "image/jpeg"}
)

print("Status:", response.status_code)
