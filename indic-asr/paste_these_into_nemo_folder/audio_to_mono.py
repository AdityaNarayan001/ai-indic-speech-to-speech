from pydub import AudioSegment 

RAW_AUDIO = "/Users/aditya.narayan/Desktop/ASR+LLM/raw_audio/sample_audio.wav"
PROCESSED_AUDIO_0 = "/Users/aditya.narayan/Desktop/ASR+LLM/processed_audio/mono_left.wav"
PROCESSED_AUDIO_1 = "/Users/aditya.narayan/Desktop/ASR+LLM/processed_audio/mono_right.wav"

def audio_to_mono(RAW_AUDIO, PROCESSED_AUDIO_0, PROCESSED_AUDIO_1):
	# Open the stereo audio file as 
	# an AudioSegment instance 
	stereo_audio = AudioSegment.from_file( 
		RAW_AUDIO, 
		format="wav") 

	mono_audios = stereo_audio.split_to_mono() 
	try:
		mono_left = mono_audios[0].export( 
			PROCESSED_AUDIO_0, 
			format="wav") 
	except:
		print("🔴 Something happend with 'mono_left' audio generation...")

	try:
		mono_right = mono_audios[1].export( 
			PROCESSED_AUDIO_1, 
			format="wav") 
	except:
		print("🔴 Something happend with 'mono_right' audio generation...")

	return "Mono files generated."
