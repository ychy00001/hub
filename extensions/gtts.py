from Extensions import Extensions
import os

try:
    from playsound import playsound
except ImportError:
    import sys
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "playsound==1.2.2"])
    from playsound import playsound

try:
    import gtts as ts
except ImportError:
    import sys
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "gTTS==2.3.2"])
    import gtts as ts


class gtts(Extensions):
    def __init__(
        self,
        USE_GTTS: bool = False,
        **kwargs,
    ):
        self.USE_GTTS = USE_GTTS
        if USE_GTTS:
            self.commands = {"Speak with GTTS": self.speak_with_gtts}

    async def speak_with_gtts(self, text: str) -> bool:
        tts = ts.gTTS(text)
        tts.save("speech.mp3")
        playsound("speech.mp3", True)
        os.remove("speech.mp3")
        return True
