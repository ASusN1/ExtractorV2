import yt_dlp

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
            
            if download_option == "audio":
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            elif download_option == "video":
                if format_id:
                    format_str = format_id
                else:
                    format_str = 'bestvideo[ext=mp4]/bestvideo'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            else:
                if format_id:
                    format_str = f'{format_id}+bestaudio[ext=m4a]/{format_id}+bestaudio/{format_id}'
                else:
                    format_str = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/bestvideo+bestaudio/best'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            
            ydl_opts = {
                'format': format_str,
                'outtmpl': output_template,
            }
        
        else:
            ydl_opts = {'format': 'best','outtmpl': save_path + '/%(title)s_auto.%(ext)s',}

        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.extract_info(link, download=True)
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
