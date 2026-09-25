class AVCodec():
    audioCodec = ""
    videoCodec = ""

    def __init__(self, audioCodec, videoCodec):
        self.audioCodec = audioCodec
        self.videoCodec = videoCodec

    def getAudioCodec(self):
        return self.audioCodec

    def setAudioCodec(new_audioCodec):
        self.audioCodec = new_audioCodec

    def getVideoCodec(self):
        return self.videoCodec
    
    def setVideoCodec(new_videoCodec):
        self.videoCodec = new_videoCodec