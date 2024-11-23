import os
import requests

def ensure_dir(file_path):
  directory = os.path.dirname(file_path)
  if not os.path.exists(directory):
    os.makedirs(directory)

def download_file(url, local_path):
  try:
    response = requests.get(url)
    response.raise_for_status()
  except Exception as e:
    print(f"Failed to load URL {url}: {str(e)}")
    return
  
  ensure_dir(local_path)
  
  content = response.content
  # 如果是 google.txt, 添加 Gemini 域名
  if local_path.endswith('google.txt'):
    content = content + b'  - \'+.gemini.google.com\''
  
  with open(local_path, 'wb') as f:
    f.write(content)
  print(f"Downloaded: {url} -> {local_path}")

def cache_file_list(file_path):
  # 检查文件是否存在
  if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    return

  # 读取 file_path
  with open(file_path, 'r') as f:
    urls = [line.strip() for line in f if line.strip() and line.strip().startswith('https://')]

  # 取得文件名，不包括扩展名
  filename = os.path.splitext(os.path.basename(file_path))[0] 
  # 下载每个文件
  for url in urls:
    if url.startswith('https://cdn.jsdelivr.net/gh/'):
      # 解析路径
      path_parts = url.split('gh/')[1].split('/')
      local_path = os.path.join(filename, *path_parts)
      try:
        download_file(url, local_path)
      except Exception as e:
        print(f"Error downloading {url}: {str(e)}")

# 缓存 Clash 资源
cache_file_list('clash.txt')
# 缓存 Loon 资源
cache_file_list('loon.txt')
