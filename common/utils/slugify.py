import re

def slugify(s:str) -> str:
  s = s.lower().strip()
  s = re.sub(r'[^\u0E00-\u0E7Fa-zA-Z0-9 _-]', '', s)
  s = re.sub(r'[\s_-]+', '-', s)
  s = re.sub(r'^-+|-+$', '', s)
  return s