from distill.renderers import renderer
import speech_recognition as sr
from sql.orm import Transcription


def recognize(source,mid):
	r = sr.Recognizer()
	audio = r.record(source) # extract audio data from the file
	
	try:
		list = r.recognize(audio,True) # generate a list of possible transcriptions
		Session().add(Transcription(mid,list[0]["text"]))
		try:
			Session().commit()
		except:
			Session().rollback()
		
	except LookupError: # speech is unintelligible
		


class IdeaController(object):
    @renderer('prettyjson')
    def get_ideas(self, request, resposne):
        return request.user.ideas
 
	

