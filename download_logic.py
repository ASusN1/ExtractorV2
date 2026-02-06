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
            print(f"Title: {info['title']}")
            print("Download completed successfully.")
    except Exception as e:
        print(f"Error: {e}")

