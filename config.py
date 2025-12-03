"""
Configurações do YouTube Downloader
Edite este arquivo para personalizar o comportamento do downloader.
"""

# Arquivo com a lista de links
LINKS_FILE = "links.txt"

# Pasta onde os vídeos serão salvos
OUTPUT_DIR = "downloads"

# Template do nome do arquivo de saída
# Variáveis disponíveis: %(title)s, %(id)s, %(ext)s, %(channel)s, %(upload_date)s
# Exemplos:
#   "%(title)s.%(ext)s"                    -> Nome do vídeo
#   "%(channel)s/%(title)s.%(ext)s"        -> Organiza por canal
#   "%(upload_date)s - %(title)s.%(ext)s"  -> Data no nome
OUTPUT_TEMPLATE = "%(title)s.%(ext)s"

# Formato do vídeo (deixe None para qualidade máxima automática)
# Exemplos:
#   None                                   -> Melhor qualidade disponível
#   "bestvideo+bestaudio/best"             -> Melhor vídeo + áudio
#   "bestvideo[height<=1080]+bestaudio"    -> Máximo 1080p
#   "bestvideo[height<=720]+bestaudio"     -> Máximo 720p
#   "worst"                                -> Pior qualidade (menor arquivo)
VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"

# Formato de saída após merge (mp4, mkv, webm)
MERGE_FORMAT = "mp4"

# Baixar legendas automaticamente (True/False)
DOWNLOAD_SUBTITLES = False

# Idiomas das legendas (ex: ['pt', 'en'])
SUBTITLE_LANGS = ['pt', 'en']

# Baixar thumbnail (True/False)
DOWNLOAD_THUMBNAIL = False

# Limite de downloads simultâneos (não recomendado mais que 3)
CONCURRENT_DOWNLOADS = 1

# Tentar novamente em caso de erro (número de tentativas)
RETRIES = 3
