import json
from pathlib import Path
from ffmpeg import FFmpeg

class Configuration():
    def __init__(self, compressedTimes, audioBitrate, videoFormat, targetBytes, duration, containerMargin, targetTotalBitrate, counter):
        self.compressedTimes = compressedTimes          # 64
        self.audioBitrate = audioBitrate                # "16000"
        self.videoFormat = videoFormat                  # ".mkv"
        self.targetBytes = targetBytes                  # Path(input_file).stat().st_size / compressed_times
        self.duration = duration                        # getduration()
        self.containerMargin = containerMargin          # 0.90   
        self.targetTotalBitrate = targetTotalBitrate    # (targetBytes * 8 / duration) * containerMargin ##### need it or no? 
        self.counter = counter                          # 0

    def getduration():
        ffprobe = (FFmpeg(executable="ffprobe").input(str(input_file),print_format="json",show_format=None,show_streams=None,))
        media = json.loads(ffprobe.execute())
        duration_seconds = float(media["format"]["duration"])

        return duration_seconds