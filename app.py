import gradio as gr
import os
from utils.processing import convert_mp3_to_wav, transcribe_wav_to_midi, clean_midi

def process_file(audio_path, min_dur, min_vel, quant, grid):
    raw_wav = "converted.wav"
    raw_midi = "raw.mid"
    clean_midi_path = "cleaned.mid"

    if audio_path.endswith(".mp3"):
        convert_mp3_to_wav(audio_path, raw_wav)
    else:
        raw_wav = audio_path

    transcribe_wav_to_midi(raw_wav, raw_midi)
    clean_midi(raw_midi, clean_midi_path,
               min_duration=min_dur,
               min_velocity=min_vel,
               quantize=quant,
               grid_size=grid)

    return clean_midi_path

demo = gr.Interface(
    fn=process_file,
    inputs=[
        gr.Audio(type="filepath", label="🎵 Upload MP3 or WAV"),
        gr.Slider(0.01, 0.5, value=0.1, step=0.01, label="Minimum Note Duration (s)"),
        gr.Slider(1, 127, value=20, step=1, label="Minimum Note Velocity"),
        gr.Checkbox(value=True, label="Enable Quantization"),
        gr.Slider(0.03125, 1.0, value=0.125, step=0.03125, label="Quantization Grid (sec)")
    ],
    outputs=gr.File(label="🎼 Download Cleaned MIDI"),
    title="🪄 MP3/WAV to Clean MIDI Converter",
    description="Upload music, tune filters, and get clean, quantized MIDI."
)

if __name__ == "__main__":
    demo.launch()
