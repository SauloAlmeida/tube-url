import pytubefix
from flask import Flask, request, render_template, redirect, url_for, flash, jsonify

app = Flask(__name__)
app.secret_key = 'tube_url_secret_key'

def get_videoplayback_url(youtube_url):
    try:
        yt = pytubefix.YouTube(youtube_url)
        
        # First try to get 1080p or higher resolution
        high_res_streams = yt.streams.filter(res="1080p").order_by('bitrate').desc()
        
        if high_res_streams:
            # Found 1080p stream
            best_stream = high_res_streams[0]
            print(f"Found 1080p stream: {best_stream}")
            return best_stream.url
            
        # If no 1080p, try to get the highest resolution available
        all_streams = yt.streams.order_by('resolution').desc()
        
        if all_streams:
            best_stream = all_streams[0]
            print(f"Using highest available resolution: {best_stream.resolution}")
            return best_stream.url
            
        return None
    
    except Exception as e:
        print(f"Error processing video: {e}")
        return None

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract():
    youtube_url = request.form.get('youtube_url')
    
    if not youtube_url:
        flash('Please enter a YouTube URL')
        return redirect(url_for('home'))
    
    videoplayback_url = get_videoplayback_url(youtube_url)
    
    if videoplayback_url:
        return render_template('index.html', video_url=videoplayback_url)
    else:
        flash('Failed to extract video URL. Please check the YouTube link and try again.')
        return redirect(url_for('home'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)