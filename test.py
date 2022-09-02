import googletrans
from googletrans import Translator

print(googletrans.LANGUAGES)

text1 = "Hello welcome to my website!"
translator = Translator()
trans1 = translator.translate(text1, src='en', dest='ja')
print("English to Japanese: ", trans1.text)

from gtts import gTTS
tts = gTTS('hello')
tts.save('hello.mp3')