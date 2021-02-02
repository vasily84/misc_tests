"""
запись видео из массива numpy c использованием FFMPEG
варианты работы с использованием временных файлов
и stdio pipe.
В.Симонов, 2-фев-2021, vasily_simonov@mail.ru
"""
import numpy as np
import os,imageio
from subprocess import Popen,PIPE,call

VIDEO_FPS = 10
VIDEO_FILE = 'video.mp4'
FRAMES_COUNT = 255

def test_ffmpeg_video_from_files(videoFile = VIDEO_FILE):
    """ проверить запись видео FFMPEG через набор файлов png на диске """
    Files = []
    rgb_image = np.ndarray(shape=(360,480,3),dtype=np.uint8)
    rgb_image[::] = 0

    for fileNum in range(FRAMES_COUNT):
        fileName = "framefile_%08d.png" % fileNum
        rgb_image[:,:] = (fileNum%256,0,0)
        imageio.imwrite(fileName, rgb_image)
        Files.append(fileName)
    
    # разные варианты вызова FFMPEG
    #call(['ffmpeg', '-y','-framerate', '8', '-i', 'framefile_%08d.png', '-r', str(VIDEO_FPS), '-pix_fmt', 'yuv420p',videoFile])
    #call(['ffmpeg', '-y','-i', 'framefile_%08d.png', '-r', str(VIDEO_FPS), '-pix_fmt', 'yuv420p',videoFile])
    call(['ffmpeg', '-y','-i', 'framefile_%08d.png', '-r', str(VIDEO_FPS),'-vcodec', 'mpeg4',videoFile])

    for file_name in Files: # удаляем временные файлы
        os.remove(file_name)

def test_ffmpeg_video_from_pipe(videoFile = VIDEO_FILE):
    """ проверить запись видео FFMPEG через stdin.pipe """
    # разные варианты вызова FFMPEG
    #pipe = Popen(['ffmpeg','-nostats','-loglevel','16', '-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', str(VIDEO_FPS), '-i', '-', '-vcodec', 'mpeg4', '-qscale', '5', '-r', str(VIDEO_FPS), videoFile], stdin=PIPE,bufsize = 0)
    pipe = Popen(['ffmpeg','-y', '-f', 'image2pipe', '-vcodec', 'png', '-r', str(VIDEO_FPS), '-i', '-', '-vcodec', 'mpeg4', '-qscale', '5', '-r', str(VIDEO_FPS), videoFile], stdin=PIPE,bufsize = 0)
    rgb_image = np.ndarray(shape=(360,480,3),dtype=np.uint8)
    rgb_image[::] = 0
    for c in range(FRAMES_COUNT):
        rgb_image[:,:] = (c%256,0,0)
        imageio.imwrite(pipe.stdin,rgb_image,format='png')
    
    pipe.stdin.close()
    pipe.wait()

def main():
    test_ffmpeg_video_from_files()
    test_ffmpeg_video_from_pipe()

if __name__ == "__main__":
    main()