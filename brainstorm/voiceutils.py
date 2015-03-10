import speech_recognition as sr

r = sr.Recognizer()


def recognize(recognizer, audio):
    print(recognizer.energy_threshold)
    try:
        list = r.recognize(audio, True)  # generate a list of possible transcriptions
        print("Possible transcriptions:")
        for prediction in list:
            print(prediction)

    except LookupError:  # speech is unintelligible
        print("didn't do the thing")


print(r.energy_threshold)
for i in range(2, 6):
    with sr.WavFile("../test" + str(i) + ".wav") as source:  # use "test.wav" as the audio source
        print("./test" + str(i) + ".wav")
        audio = r.record(source)  # extract audio data from the file
        recognize(r, audio)




