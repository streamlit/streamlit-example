import streamlit as st
import soundfile as sf
from scipy.io.wavfile import write as write_wav
from transformers import AutoProcessor, BarkModel

processor = AutoProcessor.from_pretrained("suno/bark")
model = BarkModel.from_pretrained("suno/bark")
selected_voice_preset = "v2/en_speaker_6" #DEFAULT

def text_to_speech(text, voice_preset):
    # Process the text
    #OLD inputs = processor(text, voice_preset=voice_preset)
    inputs = processor(
        text=[text],
        return_tensors="pt",
        voice_preset=voice_preset  
        )

    # Generate speech
    with st.spinner('Generating speech...'):
        #OLD speech = model.generate(**inputs)
        speech = model.generate(
            input_ids=inputs["input_ids"],
            attention_mask=inputs["attention_mask"],
            do_sample=True)   

    # Convert the output to an audio array and save it
    audio_array = speech.cpu().numpy().squeeze()
    sample_rate = model.generation_config.sample_rate
    write_wav("output.wav", sample_rate, audio_array)
    return "output.wav"

def run_app(): 
    st.title('Text to Speech Converter')
    selected_voice_preset = st.selectbox(
        'Select voice',
    ('v2/en_speaker_6', 'v2/hi_speaker_2', 'v2/hi_speaker_3', 'v2/hi_speaker_6'))
    text = st.text_area("Enter text for speech conversion", height=300, max_chars=500)
    if st.button('Convert'):
        if text:
            wav_file_path = text_to_speech(text,selected_voice_preset)
            
            # Read the saved .wav file for playback
            with open(wav_file_path, "rb") as file:
                st.audio(file.read(), format='audio/wav')

            # Provide a button for the user to download the .wav file
            with open(wav_file_path, "rb") as file:
                st.download_button(
                    label="Download WAV",
                    data=file,
                    file_name="output.wav",
                    mime="audio/wav"
                )
        else:
            st.write("Please enter some text.")

if __name__ == "__main__":
    run_app()
