import yt_dlp

#Download video function
def get_video_info(link, save_path, progress_callback=None, selected_quality=None, download_option="both", user_selected_get_video_info=False): #run third then return to first after finish 
    try:
        # Determine format based on download option
         
        if user_selected_get_video_info == True and selected_quality:
            # Extract format ID from selected quality (e.g., "720p (60fps) - 50MB [ID:123]" -> "123")
            format_id = None
            resolution = None
            if "[ID:" in selected_quality:
                format_id = selected_quality.split("[ID:")[1].split("]")[0]
            # Extract resolution (e.g., "1080p (60fps)" -> "1080")
            if "p" in selected_quality:
                resolution = selected_quality.split("p")[0].strip()
            
            # use unique name function here 
            unique_filename = unique_name_download(link, selected_quality, download_option)
            
            if download_option == "audio":
                # Download audio only - prefer m4a format (like mp3)
                format_str = 'bestaudio[ext=m4a]/bestaudio'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            elif download_option == "video":
                # Download video only, NO AUDIO - prefer mp4
                if format_id:
                    format_str = format_id  # Just the video format, no audio
                else:
                    format_str = 'bestvideo[ext=mp4]/bestvideo'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            else:  # both
                # For "both", get pre-merged format with audio at selected resolution
                # Filter for formats that have BOTH video and audio, prefer mp4
                if resolution:
                    # Get best pre-merged format with audio at selected resolution, prefer mp4
                    format_str = f'best[height={resolution}][acodec!=none][ext=mp4]/best[height={resolution}][acodec!=none]/best[height<={resolution}][acodec!=none][ext=mp4]/best[height<={resolution}][acodec!=none]/best[acodec!=none][ext=mp4]/best[acodec!=none]'
                    print(f"Downloading both video+audio at {resolution}p resolution")
                else:
                    # Prefer mp4 format with audio
                    format_str = 'best[acodec!=none][ext=mp4]/best[acodec!=none]/best'
                output_template = save_path + f'/%(title)s_{unique_filename}.%(ext)s'
            
            ydl_opts = {
                'format': format_str,
                'outtmpl': output_template,
            }
        
        else: # user_selected_get_video_info == False or no quality selected
            #just put auto in the name / download the best resolution available 
            ydl_opts = {'format': 'best','outtmpl': save_path + '/%(title)s_auto.%(ext)s',}

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
            qualities_dict = {}  # Use dict to track unique combinations by key
            # Loop through all available formats
            for video_format in formats:
                video_resolution = video_format.get("height")
                # Some formats don’t have video video_resolution (audio only)
                if video_resolution is None:
                    continue
                
                format_id = video_format.get("format_id")
                fps = video_format.get("fps", 0)  # Default to 0 if no fps
                size_bytes = video_format.get("filesize") or video_format.get("filesize_approx")
                size_text = format_storage_size(size_bytes)
                
                # Create a unique key based on resolution + fps (not size, since size varies)
                unique_key = f"{video_resolution}p_{fps}fps"
                
                # Build quality text like "720p (60fps) - 50.5 MB [ID:format_id]"
                quality_text = f"{video_resolution}p"
                if fps and fps > 0:
                    quality_text += f" ({int(fps)}fps)"
                if size_text:
                    quality_text += f" - {size_text}"
                quality_text += f" [ID:{format_id}]"  # Add format ID for precise selection
                
                # Keep only the highest quality (largest file) for each unique resolution+fps combo
                if unique_key not in qualities_dict:
                    qualities_dict[unique_key] = (quality_text, video_resolution, size_bytes or 0)
                else:
                    # If this format has larger size, replace it
                    existing_size = qualities_dict[unique_key][2]
                    if (size_bytes or 0) > existing_size:
                        qualities_dict[unique_key] = (quality_text, video_resolution, size_bytes or 0)
            
            # Extract quality texts and sort by resolution (highest first)
            qualities = [q[0] for q in qualities_dict.values()]
            
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
    """Get the download option from the StringVar"""
    if download_option_var is not None:
        return download_option_var.get()
    return "both"

#----------------------------------------------
# This function generates a unique name for the downloaded file based on the selected quality and download option 
def unique_name_download(link, selected_quality, download_option):
    """Generate unique filename: name + download_option + resolution (if video)"""
    
    # Extract resolution from selected_quality (e.g., "720p (60fps)" -> "720p")
    resolution = ""
    if selected_quality:
        resolution = selected_quality.split("p")[0] + "p" if "p" in selected_quality else "best"
    else:
        resolution = "best"
    
    if download_option == "audio":
        # For audio, no resolution needed
        return f"audio"
    elif download_option == "video":
        # For video, include resolution
        return f"video_{resolution}"
    else:  # both
        # For both, include resolution
        return f"both_{resolution}"
