from PIL import Image, ImageTk
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# State mapping to image files
STATE_IMAGES = {
    "static": os.path.join(BASE_DIR, "computer_static.png"), #The static alway ( this is static_state)
    "downloading": os.path.join(BASE_DIR, "computer_downloading.gif"), #play when downloading is in progress ( this is downloading_state) since this is a gif do something 
    "success": os.path.join(BASE_DIR, "computer_download_succesfull.png"), #play when download is successful then after 10 second it will reset to static ( this is download_success_state)
    "failed": os.path.join(BASE_DIR, "computer_download_fail.png"), #play when download fails then after 10 second it will reset to static (this is download_fail_state)
    "error": os.path.join(BASE_DIR, "computer_error_encounter.png") #play when there is an error due to user input or  then after 10 second it will reset to static ( this is error_encounter_state)
}

# Store animation state per label using id() as key
_animation_state = {}

def get_image_path(state):
    """Return image path for given state"""
    return STATE_IMAGES.get(state, STATE_IMAGES["static"])

def _stop_animation(label):
    """Stop any running animation for this label"""
    label_id = id(label)
    if label_id in _animation_state:
        state = _animation_state[label_id]
        if 'after_id' in state and state['after_id']:
            label.after_cancel(state['after_id'])
        _animation_state[label_id] = {}

def _animate_gif(label, gif_path, frame_index=0):
    """Animate a GIF by cycling through frames"""
    label_id = id(label)
    
    try:
        img = Image.open(gif_path)
        
        # Get frame count (default to 1 if not available)
        frame_count = getattr(img, 'n_frames', 1)
        
        # Set to current frame
        img.seek(frame_index % frame_count)
        
        # Get frame duration in milliseconds
        duration = img.info.get('duration', 100)
        
        # Thumbnail the image
        img.thumbnail((200, 200))
        
        # Convert to PhotoImage
        photo = ImageTk.PhotoImage(img)
        label.config(image=photo)
        label.image = photo  # Keep a reference
        
        # Schedule next frame
        if frame_count > 1:
            next_frame = (frame_index + 1) % frame_count
            after_id = label.after(duration, _animate_gif, label, gif_path, next_frame)
            
            if label_id not in _animation_state:
                _animation_state[label_id] = {}
            _animation_state[label_id]['after_id'] = after_id
        
    except Exception as e:
        print(f"Error animating GIF: {e}")

def display_animation(label, state):
    """Display animation/image on label widget for given state"""
    # Stop any existing animation
    _stop_animation(label)
    
    image_path = get_image_path(state)
    
    if not os.path.exists(image_path):
        print(f"Warning: Image not found: {image_path}")
        return
    
    label_id = id(label)
    if label_id not in _animation_state:
        _animation_state[label_id] = {}
    
    try:
        # Check if it's a GIF
        if image_path.lower().endswith('.gif'):
            _animate_gif(label, image_path, 0)
            _animation_state[label_id]['gif_path'] = image_path
        else:
            # Static image
            img = Image.open(image_path)
            img.thumbnail((200, 200))  # Scale to fit
            photo = ImageTk.PhotoImage(img)
            label.config(image=photo)
            label.image = photo  # Keep a reference
            _animation_state[label_id]['after_id'] = None
    except Exception as e:
        print(f"Error displaying animation: {e}")