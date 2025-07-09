from pydub import AudioSegment
from basic_pitch.inference import predict
import pretty_midi

def convert_mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_path, format="wav")

def transcribe_wav_to_midi(wav_path, midi_path):
    _, midi_data, _ = predict(wav_path)
    midi_data.write(midi_path)

def quantize_note(note, grid_size):
    start = round(note.start / grid_size) * grid_size
    duration = note.end - note.start
    end = start + round(duration / grid_size) * grid_size
    return start, end

def clean_midi(input_midi, output_midi, min_duration=0.1, min_velocity=20, quantize=True, grid_size=0.125):
    midi = pretty_midi.PrettyMIDI(input_midi)
    for instrument in midi.instruments:
        cleaned = []
        for note in instrument.notes:
            if (note.end - note.start) >= min_duration and note.velocity >= min_velocity:
                if quantize:
                    note.start, note.end = quantize_note(note, grid_size)
                cleaned.append(note)
        instrument.notes = cleaned
    midi.write(output_midi)
