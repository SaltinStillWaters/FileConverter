import fitz
import img2pdf
from pytubefix import YouTube
from pytubefix.cli import on_progress
from pathlib import Path
import os
import subprocess
import re

os.environ["PATH"] += r";C:\\ffmpeg\\bin"

def convert_pdf_to_png(pdf_paths):
    if not isinstance(pdf_paths, list):
        pdf_paths = [pdf_paths]
    
    for pdf_path in pdf_paths:
        #cleaning
        pdf_path = pdf_path.replace("\\", "/")
        output_filename = pdf_path.split("/")[-1]
        output_filename = output_filename.split(".")[0]
        
        output_path = Path.home() / "Desktop" / output_filename
        output_path.mkdir(parents=True, exist_ok=True)
        
        pdf_file = fitz.open(pdf_path)
        for page_num in range(len(pdf_file)):
            page = pdf_file.load_page(page_num)
            zoom = 2
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            output_file = f"{output_path}/page_{page_num + 1}.png"
            pix.save(output_file)
            print('Saved!')

def convert_jpg_or_png_to_pdf(image_paths):
    #cleaning
    if isinstance(image_paths, list):
        output_filename = image_paths[0].split("/")[-1]
        for path in image_paths:
            path = path.replace("\\", "/")
    else:
        output_filename = image_paths.split("/")[-1]
        image_paths = image_paths.replace("\\", "/")
    output_filename = output_filename.split(".")[0]
    
    output_path = Path.home() / "Desktop" / output_filename
    with open(f"{output_path}.pdf", "wb") as f:
        f.write(img2pdf.convert(image_paths))    

def convert_yt_to_m4a(yt_links):
    if not isinstance(yt_links, list):
        yt_links = [yt_links]
    
    for yt_link in yt_links:
        
        output_path = Path.home() / "Desktop"
        
        try:
            yt = YouTube(yt_link, on_progress_callback=on_progress)
            title = re.sub(r'[\\/*?:"<>|]', '_', yt.title)
            
            audio_stream = yt.streams.filter(file_extension="mp4", only_audio=True).order_by("abr").desc().first()
            
            if not audio_stream:
                print(f"Error: No suitable audio stream found for: {title}")
                continue
            
            audio_stream.download(output_path=output_path)
            
            print("Audio downloaded")
        except Exception as e:
            print(f"Error downloading audio: {e}")
    
def convert_yt_to_mp4(yt_links):
    if not isinstance(yt_links, list):
        yt_links = [yt_links]
        
    for yt_link in yt_links:
            
        output_path = Path.home() / "Desktop"
        
        try:
            yt = YouTube(yt_link, on_progress_callback=on_progress)
            title = re.sub(r'[\\/*?:"<>|]', '_', yt.title)
            
            video_stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_video=True).order_by("resolution").desc().first()
            audio_stream = yt.streams.filter(adaptive=True, file_extension="mp4", only_audio=True).order_by("abr").desc().first()
            
            if not video_stream:
                print(f"Error: No suitable video stream found for: {title}")
                continue
            if not audio_stream:
                print(f"Error: No suitable audio stream found for: {title}")
                continue
            
            vid_temp_name = str(output_path / f"{title}_vid.mp4")
            audio_temp_name = str(output_path / f"{title}_vid.m4a")
            
            video_file = video_stream.download(output_path=output_path, filename=vid_temp_name)
            audio_file = audio_stream.download(output_path=output_path, filename=audio_temp_name)
            
            output_file = output_path / f"{title}.mp4"
            merge_command = f'ffmpeg -i "{video_file}" -i "{audio_file}" -c:v copy -c:a aac "{output_file}" -y'
            subprocess.run(merge_command, shell=True)
            
            os.remove(video_file)
            os.remove(audio_file)
            
            print("Video downloaded")
        except Exception as e:
            print(f"Error downloading video: {e}")

def on_progress(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percent = (bytes_downloaded / total_size) * 100      
    print(f"Downloaded: {percent:.2f}%")

def on_complete(stream, file_path):
    print(f"Download complete: {file_path}")
    print(f"Stream info: {stream}")
    
#convert_yt_to_m4a(["https://www.youtube.com/watch?v=ffSS4gOHagE&t=1s", "https://www.youtube.com/watch?v=HfshBrqCw9k"])
#convert_jpg_or_png_to_pdf("jpgtest.jpg")
#convert_pdf_to_png(r"C:\Users\Salti\Downloads\PEJANA_Skew_Kurtosis.pdf")