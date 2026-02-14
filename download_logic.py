import yt_dlp

#Download video function
def get_video_info(link, save_path, progress_callback=None, selected_quality=None, download_option="both"): #run third then return to first after finish 
    try:
        # Determine format based on download option
        if download_option == "audio":
            format_str = 'bestaudio[ext=m4a]/bestaudio'
            output_template = save_path + '/%(title)s_audio.%(ext)s'
        elif download_option == "video":
            format_str = 'bestvideo[ext=mp4]/best[ext=mp4]'
            output_template = save_path + '/%(title)s_video.%(ext)s'
        else:  # both
            format_str = 'best[ext=mp4]/best'
            output_template = save_path + '/%(title)s_both.%(ext)s'
        
        ydl_opts = {'format': format_str,'outtmpl': output_template,}
        
        # Add progress hook if callback is provided
        if progress_callback:
            ydl_opts['progress_hooks'] = [progress_callback]
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            print("Title: " + str({info['title']}))
            print("Download completed successfully.")
    except Exception as e:
        print("Error: " + str(e))

#---------------------------------------------
# Get available video qualities without downloading the video
def get_video_qualities(link):
    try:
        # Options for yt-dlp (keep output quiet)
        options = {"quiet": True,"no_warnings": True}
        with yt_dlp.YoutubeDL(options) as ydl:
            # Extract video information only (no download)
            video_info = ydl.extract_info(link, download=False)
            formats = video_info.get("formats", [])
            qualities = []
            # Loop through all available formats
            for video_format in formats:
                video_resolution = video_format.get("height")
                # Some formats don’t have video video_resolution (audio only)
                if video_resolution is None:
                    continue
                fps = video_format.get("fps")
                size_bytes = video_format.get("filesize") or video_format.get("filesize_approx") # Try to get exact filesize, if not available use approximate
                size_text = format_storage_size(size_bytes)
                # Build quality text like "720p (60fps)"
                quality_text = f"{video_resolution}p"
                if fps:
                    quality_text += f" ({fps}fps)"
                if size_text: # Add size info if available
                    quality_text += f" - {size_text}"
                # Avoid duplicates
                if quality_text not in qualities:
                    qualities.append(quality_text)
            # If no qualities were found, return a fallback
            if not qualities:
                return ["Best Available"]
            # Sort qualities by resolution (highest first)
            qualities.sort(
                key=lambda q: int(q.split("p")[0]),
                reverse=True
            )
            return qualities
    except Exception as error:
        print("Error fetching qualities:", error)
        return []
#------------------------------------
def format_storage_size(storage_size):
    if storage_size is None:
        return None
    size = float(storage_size)
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.2f} {unit}"
        size /= 1024.0
    return f"{size:.2f} PB"

#----------------------------------------------
# This function returns the selected download option (audio/video/both)
def get_download_option(download_option_var):
    """
    Returns the download option selected by the user
    download_option_var: The StringVar from the UI (from Radiobutton selection)
    """
    return download_option_var.get()
