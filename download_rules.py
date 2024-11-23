import os
import requests

def ensure_dir(file_path):
  directory = os.path.dirname(file_path)
  if not os.path.exists(directory):
    os.makedirs(directory)

def download_file(url, local_path):
  response = requests.get(url)
  response.raise_for_status()
  ensure_dir(local_path)
  
  content = response.content
  # 如果是 google.txt, 添加 Gemini 域名
  if local_path.endswith('google.txt'):
    content = content + b'  - \'+.gemini.google.com\''
  
  with open(local_path, 'wb') as f:
    f.write(content)
  print(f"Downloaded: {url} -> {local_path}")

# 读取 clash.txt
with open('clash.txt', 'r') as f:
  urls = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]

# 下载每个文件
for url in urls:
  if url.startswith('https://cdn.jsdelivr.net/gh/'):
    # 解析路径
    path_parts = url.split('gh/')[1].split('/')
    local_path = os.path.join('clash', *path_parts)
    try:
      download_file(url, local_path)
    except Exception as e:
      print(f"Error downloading {url}: {str(e)}")
