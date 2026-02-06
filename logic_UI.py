from download_logic import get_video_info


def UI_get_data(link_entry, path_entry):
#Extract values from the given Entry widgets and call downloader
    link = link_entry.get().strip()
    save_path = path_entry.get().strip()
    if not link or not save_path:
        return
    get_video_info(link, save_path)