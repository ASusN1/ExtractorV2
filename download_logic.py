import yt_dlp

#Download video function
def get_video_info(link, save_path): #run third then return to first after finish 
    try:
        ydl_opts = {
            'format': 'best',
            'outtmpl': save_path + '/%(title)s.%(ext)s',
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(link, download=True)
            print("Title: " +str({info['title']}))
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
                # Build quality text like "720p (60fps)"
                quality_text = f"{video_resolution}p"
                if fps:
                    quality_text += f" ({fps}fps)"
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
