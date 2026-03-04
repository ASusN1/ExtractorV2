import yt_dlp
import os
import glob
import ffmpeg
import sys


def _get_runtime_base_dir():
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return sys._MEIPASS
    return os.path.dirname(os.path.abspath(__file__))


def _get_ffmpeg_executable():
    base_dir = _get_runtime_base_dir()
    local_ffmpeg = os.path.join(base_dir, 'ffmpeg.exe')
    if os.path.exists(local_ffmpeg):
        return local_ffmpeg
    return 'ffmpeg'


def _get_ffmpeg_location():
    ffmpeg_exe = _get_ffmpeg_executable()
    if ffmpeg_exe.lower().endswith('.exe') and os.path.exists(ffmpeg_exe):
        return os.path.dirname(ffmpeg_exe)
    return None

def get_video_info(link, save_path, progress_callback=None, selected_quality=None, download_option="both", user_selected_get_video_info=False):
    try:
        if user_selected_get_video_info == True and selected_quality:
            format_id = None
            resolution = None
            if "[ID:" in selected_quality:
                format_id = selected_quality.split("[ID:")[1].split("]")[0]
            if "p" in selected_quality:
                resolution = selected_quality.split("p")[0].strip()
            
            unique_filename = unique_name_download(link, selected_quality, download_option)
            
            # ALWAYS download with both audio AND video merged (complete file)
            # Then remove audio if video-only is selected
            if download_option == "audio":
                # Download best audio
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            else:
                # For both and video: download with merged audio+video
                if format_id:
                    format_str = f'{format_id}+bestaudio[ext=m4a]/{format_id}+bestaudio/{format_id}'
                    if resolution:
                        print(f"Downloading video+audio using selected format at {resolution}p")
                else:
                    format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            
            ydl_opts = {
                'format': format_str,
                'outtmpl': output_template,
                'merge_output_format': 'mp4',  # Merge audio+video as MP4 (media player compatible)
            }
        
        else:
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best',
                'outtmpl': save_path + '/%(title)s_auto.%(ext)s',
                'merge_output_format': 'mp4',
            }

        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]

        ffmpeg_location = _get_ffmpeg_location()
        if ffmpeg_location:
            ydl_opts['ffmpeg_location'] = ffmpeg_location
        
        downloaded_file = None
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            print("Title: " + str({info['title']}))
            
            # Get the downloaded file path
            if 'requested_downloads' in info and len(info['requested_downloads']) > 0:
                downloaded_file = info['requested_downloads'][0].get('filepath')
            
            print("Download completed successfully.")
        
        # Post-processing: Remove audio if video-only selected
        if download_option == "video" and downloaded_file and os.path.exists(downloaded_file):
            print(f"Processing: Removing audio from {os.path.basename(downloaded_file)}")
            remove_audio_from_video(downloaded_file)
        
        return info if user_selected_get_video_info else None
    except Exception as e:
        raise Exception(str(e))

def get_video_qualities(link):
    try:
        options = {"quiet": True,"no_warnings": True}
        with yt_dlp.YoutubeDL(options) as ydl:
            video_info = ydl.extract_info(link, download=False)
            formats = video_info.get("formats", [])
            qualities_dict = {}
            for video_format in formats:
                video_resolution = video_format.get("height")
                if video_resolution is None:
                    continue
                
                format_id = video_format.get("format_id")
                fps = video_format.get("fps", 0)
                size_bytes = video_format.get("filesize") or video_format.get("filesize_approx")
                size_text = format_storage_size(size_bytes)
                
                unique_key = f"{video_resolution}p_{fps}fps"
                
                quality_text = f"{video_resolution}p"
                if fps and fps > 0:
                    quality_text += f" ({int(fps)}fps)"
                if size_text:
                    quality_text += f" - {size_text}"
                quality_text += f" [ID:{format_id}]"
                
                if unique_key not in qualities_dict:
                    qualities_dict[unique_key] = (quality_text, video_resolution, size_bytes or 0)
                else:
                    existing_size = qualities_dict[unique_key][2]
                    if (size_bytes or 0) > existing_size:
                        qualities_dict[unique_key] = (quality_text, video_resolution, size_bytes or 0)
            
            qualities = [q[0] for q in qualities_dict.values()]
            
            if not qualities:
                return ["Best Available"]
            qualities.sort(
                key=lambda q: int(q.split("p")[0]),
                reverse=True
            )
            return qualities
    except Exception as error:
        return []

def remove_audio_from_video(filepath):
    """
    Remove audio track from video file using FFmpeg.
    Creates a new file without audio (silent video).
    """
    try:
        output_path = filepath.replace('.mp4', '_silent.mp4').replace('.mkv', '_silent.mp4')
        
        # Use ffmpeg-python to copy video and remove audio
        stream = ffmpeg.input(filepath)
        stream = ffmpeg.output(stream.video, output_path, 
                              vcodec='copy',  # Copy video codec without re-encoding
                              an=None)        # Remove audio
        ffmpeg.run(
            stream,
            overwrite_output=True,
            capture_stderr=True,
            quiet=True,
            cmd=_get_ffmpeg_executable()
        )
        
        # Replace original with silent version
        if os.path.exists(output_path):
            os.replace(output_path, filepath)
            print(f"Audio removed from: {filepath}")
            return True
    except ffmpeg.Error as e:
        print(f"FFmpeg error removing audio: {e.stderr.decode() if e.stderr else str(e)}")
        return False
    except Exception as e:
        print(f"Error removing audio: {e}")
        return False

def format_storage_size(storage_size):
    if storage_size is None:
        return None
    size = float(storage_size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

def get_download_option(download_option_var):
    """Get the download option from the StringVar"""
    if download_option_var is not None:
        return download_option_var.get()
    return "both"

def unique_name_download(link, selected_quality, download_option):
    """Generate unique filename: name + download_option + resolution (if video)"""
    resolution = ""
    if selected_quality:
        resolution = selected_quality.split("p")[0] + "p" if "p" in selected_quality else "best"
    else:
        resolution = "best"
    
    if download_option == "audio":
        return f"audio"
    elif download_option == "video":
        return f"video_{resolution}"
    else:
        return f"both_{resolution}"
