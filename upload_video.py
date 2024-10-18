import requests
import base64

def upload_video_to_github(video_path, github_token, repository_owner, repository_name, file_path, commit_message):
    # Đọc nội dung của video và mã hóa thành chuỗi Base64
    with open(video_path, 'rb') as video_file:
        video_content = video_file.read()
        encoded_video = base64.b64encode(video_content).decode('utf-8')

    # Xây dựng URL endpoint
    url = f'https://api.github.com/repos/{repository_owner}/{repository_name}/contents/{file_path}'

    # Tạo payload cho yêu cầu API
    payload = {
        "message": commit_message,
        "content": encoded_video
    }

    # Thêm token xác thực vào header
    headers = {
        "Authorization": f"Bearer {github_token}"
    }

    # Gửi yêu cầu POST để tạo hoặc cập nhật nội dung file trên GitHub
    response = requests.put(url, json=payload, headers=headers)

    if response.status_code == 201:
        print("Video uploaded successfully.")
    else:
        print("Failed to upload video.")
        print(f"Response: {response.status_code} - {response.text}")



def upload_vid(video_path, file_path):
    # Thông tin xác thực và thông tin repository
    github_token = "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"
    repository_owner = "sonnh7289"
    repository_name = "video-upload"

    # Thông điệp commit
    commit_message = "Upload video file"

    # Gọi hàm để tải lên video lên GitHub
    upload_video_to_github(video_path, github_token, repository_owner, repository_name, file_path, commit_message)

    link = f"https://github.com/sonnh7289/video-upload/blob/main/{file_path}"
    print(link)
    # note: this will break if a repo/organization or subfolder is named "blob" -- would be ideal to use a fancy regex
    # to be more precise here
    link_vid = link.replace("github.com", "raw.githubusercontent.com").replace("/blob/", "/")
    return link_vid