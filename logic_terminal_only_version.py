import yt_dlp

# Download video function
def get_video_info(link, save_path):
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

# Get user input for video link and download path
def get_user_info():
    while True:
        try:
            link = input("Enter the YouTube video link: ") 
            save_path = input("Enter the path to save the video: ") 
            return link, save_path
        except Exception as e:
            print(f"Error: {e}")
            print("Please try again.")

def run_program():
    run_program = True 
    while run_program == True: 
        user_run_program = int(input("Do you want to download a YouTube video? (1 for Yes, 0 for No): "))
        if user_run_program == 1: 
            link, save_path = get_user_info() 
            get_video_info(link, save_path) 
        else: 
            run_program = False 
            print("Exiting the program. Goodbye!")

# Run the program test version
run_program()

