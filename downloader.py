#!/usr/bin/env python3
"""
YouTube Video Downloader - Download em massa usando yt-dlp
Lê links de um arquivo .txt e baixa todos os vídeos automaticamente.
Atualiza o yt-dlp automaticamente antes de iniciar os downloads.
"""

import subprocess
import sys
import os
from pathlib import Path
from datetime import datetime

# Tenta importar colorama, se não existir, usa fallback
try:
    from colorama import init, Fore, Style
    init(autoreset=True)
    HAS_COLORAMA = True
except ImportError:
    HAS_COLORAMA = False
    # Fallback sem cores
    class Fore:
        GREEN = RED = YELLOW = CYAN = MAGENTA = WHITE = RESET = ""
    class Style:
        BRIGHT = RESET_ALL = ""

# Tenta importar configurações personalizadas
try:
    from config import (
        LINKS_FILE, OUTPUT_DIR, OUTPUT_TEMPLATE,
        VIDEO_FORMAT, MERGE_FORMAT, DOWNLOAD_SUBTITLES,
        SUBTITLE_LANGS, DOWNLOAD_THUMBNAIL, RETRIES
    )
except ImportError:
    # Configurações padrão caso config.py não exista
    LINKS_FILE = "links.txt"
    OUTPUT_DIR = "downloads"
    OUTPUT_TEMPLATE = "%(title)s.%(ext)s"
    VIDEO_FORMAT = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    MERGE_FORMAT = "mp4"
    DOWNLOAD_SUBTITLES = False
    SUBTITLE_LANGS = ['pt', 'en']
    DOWNLOAD_THUMBNAIL = False
    RETRIES = 3


def print_header():
    """Exibe o cabeçalho do programa."""
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}   YouTube Video Downloader - Download em Massa")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")


def print_success(msg):
    """Imprime mensagem de sucesso."""
    print(f"{Fore.GREEN}✓ {msg}{Style.RESET_ALL}")


def print_error(msg):
    """Imprime mensagem de erro."""
    print(f"{Fore.RED}✗ {msg}{Style.RESET_ALL}")


def print_info(msg):
    """Imprime mensagem informativa."""
    print(f"{Fore.CYAN}ℹ {msg}{Style.RESET_ALL}")


def print_warning(msg):
    """Imprime mensagem de aviso."""
    print(f"{Fore.YELLOW}⚠ {msg}{Style.RESET_ALL}")


def get_python_executable():
    """Retorna o caminho do executável Python no ambiente virtual."""
    return sys.executable


def update_ytdlp():
    """
    Verifica e atualiza o yt-dlp para a versão mais recente.
    Retorna True se a atualização foi bem-sucedida ou se já está atualizado.
    """
    print_info("Verificando atualizações do yt-dlp...")

    python_exe = get_python_executable()

    try:
        # Primeiro, verifica a versão atual
        result = subprocess.run(
            [python_exe, "-m", "pip", "show", "yt-dlp"],
            capture_output=True,
            text=True
        )

        current_version = None
        for line in result.stdout.split('\n'):
            if line.startswith('Version:'):
                current_version = line.split(':')[1].strip()
                break

        if current_version:
            print_info(f"Versão atual do yt-dlp: {current_version}")

        # Atualiza o yt-dlp
        print_info("Atualizando yt-dlp para a versão mais recente...")
        result = subprocess.run(
            [python_exe, "-m", "pip", "install", "--upgrade", "yt-dlp"],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Verifica a nova versão
            result = subprocess.run(
                [python_exe, "-m", "pip", "show", "yt-dlp"],
                capture_output=True,
                text=True
            )

            new_version = None
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    new_version = line.split(':')[1].strip()
                    break

            if new_version and current_version != new_version:
                print_success(f"yt-dlp atualizado: {current_version} → {new_version}")
            else:
                print_success(f"yt-dlp já está na versão mais recente: {new_version}")

            return True
        else:
            print_error(f"Erro ao atualizar yt-dlp: {result.stderr}")
            return False

    except Exception as e:
        print_error(f"Erro ao verificar/atualizar yt-dlp: {e}")
        return False


def read_links(file_path):
    """
    Lê os links do arquivo especificado.
    Ignora linhas vazias e comentários (linhas começando com #).
    """
    links = []

    if not os.path.exists(file_path):
        print_error(f"Arquivo não encontrado: {file_path}")
        return links

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()

            # Ignora linhas vazias e comentários
            if not line or line.startswith('#'):
                continue

            # Valida se parece ser um link do YouTube
            if 'youtube.com' in line or 'youtu.be' in line:
                links.append((line_num, line))
            else:
                print_warning(f"Linha {line_num}: Link ignorado (não parece ser do YouTube): {line[:50]}...")

    return links


def download_video(url, output_dir, video_num, total_videos):
    """
    Baixa um vídeo usando yt-dlp.
    Retorna True se o download foi bem-sucedido.
    """
    try:
        # Importa yt-dlp
        import yt_dlp

        # Configurações do yt-dlp
        ydl_opts = {
            'format': VIDEO_FORMAT,
            'outtmpl': os.path.join(output_dir, OUTPUT_TEMPLATE),
            'ignoreerrors': False,
            'no_warnings': False,
            'quiet': False,
            'progress_hooks': [lambda d: None],  # Mantém o progresso padrão
            'merge_output_format': MERGE_FORMAT,
            'retries': RETRIES,
        }

        # Configurações opcionais
        if DOWNLOAD_SUBTITLES:
            ydl_opts['writesubtitles'] = True
            ydl_opts['subtitleslangs'] = SUBTITLE_LANGS

        if DOWNLOAD_THUMBNAIL:
            ydl_opts['writethumbnail'] = True

        print(f"\n{Fore.MAGENTA}[{video_num}/{total_videos}] Baixando...{Style.RESET_ALL}")
        print(f"{Fore.WHITE}URL: {url}{Style.RESET_ALL}")

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Primeiro obtém informações do vídeo
            info = ydl.extract_info(url, download=False)
            title = info.get('title', 'Título desconhecido')
            duration = info.get('duration', 0)

            duration_str = f"{duration // 60}:{duration % 60:02d}" if duration else "N/A"
            print(f"{Fore.CYAN}Título: {title}")
            print(f"{Fore.CYAN}Duração: {duration_str}{Style.RESET_ALL}")

            # Faz o download
            ydl.download([url])

        print_success(f"Download concluído: {title}")
        return True

    except Exception as e:
        print_error(f"Erro ao baixar {url}: {e}")
        return False


def create_output_dir(output_dir):
    """Cria o diretório de saída se não existir."""
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    print_info(f"Diretório de downloads: {os.path.abspath(output_dir)}")


def main():
    """Função principal do programa."""
    print_header()

    # Passo 1: Atualizar yt-dlp
    print(f"{Fore.YELLOW}[Etapa 1/3] Atualizando yt-dlp...{Style.RESET_ALL}")
    print("-" * 40)

    if not update_ytdlp():
        print_warning("Continuando com a versão atual do yt-dlp...")

    print()

    # Passo 2: Ler links do arquivo
    print(f"{Fore.YELLOW}[Etapa 2/3] Lendo links do arquivo...{Style.RESET_ALL}")
    print("-" * 40)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    links_file = os.path.join(script_dir, LINKS_FILE)

    links = read_links(links_file)

    if not links:
        print_error("Nenhum link válido encontrado!")
        print_info(f"Adicione links do YouTube ao arquivo: {links_file}")
        print_info("Um link por linha. Linhas com # são comentários.")
        return

    print_success(f"Encontrados {len(links)} links para download")
    print()

    # Passo 3: Baixar vídeos
    print(f"{Fore.YELLOW}[Etapa 3/3] Baixando vídeos...{Style.RESET_ALL}")
    print("-" * 40)

    output_dir = os.path.join(script_dir, OUTPUT_DIR)
    create_output_dir(output_dir)

    successful = 0
    failed = 0
    failed_links = []

    start_time = datetime.now()

    for idx, (line_num, url) in enumerate(links, 1):
        if download_video(url, output_dir, idx, len(links)):
            successful += 1
        else:
            failed += 1
            failed_links.append((line_num, url))

    end_time = datetime.now()
    duration = end_time - start_time

    # Resumo final
    print(f"\n{Fore.CYAN}{'='*60}")
    print(f"{Fore.CYAN}   RESUMO DO DOWNLOAD")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.GREEN}✓ Downloads concluídos: {successful}")
    print(f"{Fore.RED}✗ Downloads falharam: {failed}")
    print(f"{Fore.CYAN}⏱ Tempo total: {duration}")
    print(f"{Fore.CYAN}📁 Pasta de downloads: {os.path.abspath(output_dir)}{Style.RESET_ALL}")

    if failed_links:
        print(f"\n{Fore.YELLOW}Links que falharam:{Style.RESET_ALL}")
        for line_num, url in failed_links:
            print(f"  Linha {line_num}: {url}")

    print()


if __name__ == "__main__":
    main()
