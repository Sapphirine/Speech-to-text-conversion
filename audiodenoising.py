import numpy as np
import soundfile as sf
from sklearn.decomposition import FastICA

def denoise(input_wav, n_components=2, max_iter=200):
    """
    Denoise input WAV file using Independent Component Analysis (ICA).
    
    Parameters:
        input_wav (str): Path to the input WAV file.
        n_components (int): Number of independent components to extract (default is 2).
        max_iter (int): Maximum number of iterations for the FastICA algorithm (default is 200).
    
    Returns:
        np.ndarray: Denoised audio data.
    """
    # Load the input WAV file
    audio_data, samplerate = sf.read(input_wav)
    
    # Perform FastICA
    ica = FastICA(n_components=n_components, max_iter=max_iter)
    separated_audio = ica.fit_transform(audio_data.T)
    
    # Transpose the separated audio data back to its original shape
    denoised_audio = separated_audio.T
    
    return denoised_audio, samplerate

def create_wav_file(audio_data, samplerate, file_path):
    # Write audio data to WAV file
    sf.write(file_path, audio_data, samplerate)

# Example usage:
input_wav = "test.wav"
output_wav = "denoisedaudio.wav"

# Denoise the input WAV file
denoised_audio, samplerate = denoise(input_wav)

# Create a new WAV file from the denoised audio data
create_wav_file(denoised_audio, samplerate, output_wav)

