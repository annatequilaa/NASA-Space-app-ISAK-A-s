from music21 import stream, note
from PIL import Image
import os
from pydub import AudioSegment

def get_hue_saturation_brightness(chunk):
    # Convert the image chunk to HSV (Hue, Saturation, Value)
    hsv_image = chunk.convert("HSV")
    pixels = list(hsv_image.getdata())
    hue_values = [pixel[0] for pixel in pixels]
    saturation_values = [pixel[1] for pixel in pixels]
    brightness_values = [pixel[2] for pixel in pixels]
    avg_hue = sum(hue_values) / len(hue_values)
    avg_saturation = sum(saturation_values) / len(saturation_values)
    avg_brightness = sum(brightness_values) / len(brightness_values)
    return avg_hue, avg_saturation, avg_brightness

def split_image(size, imagee):
    image = Image.open(imagee)
    chunk_width = size
    chunk_height = size
    img_width, img_height = image.size
    chunks = []
    chunk_attributes = []

    for top in range(0, img_height, chunk_height):
        for left in range(0, img_width, chunk_width):
            box = (left, top, left + chunk_width, top + chunk_height)
            chunk = image.crop(box)
            chunks.append(chunk)
            avg_hue, avg_saturation, avg_brightness = get_hue_saturation_brightness(chunk)
            chunk_attributes.append([
                int(avg_hue),
                int(avg_saturation),
                int(avg_brightness)
            ])

    return chunk_attributes

def generate_pitch(h: int) -> int:
    lowest_h = 0
    highest_h = 360
    lowest_midi = 36  # Lowest MIDI note for piano
    highest_midi = 108  # Highest MIDI note
    note_interval = (highest_h - lowest_h) / (highest_midi - lowest_midi)
    return lowest_midi + round(h / note_interval)

def generate_loudness(s: int) -> int:
    lowest_s = 0
    highest_s = 100
    lowest_db = 50
    highest_db = 70
    loud_interval = (highest_s - lowest_s) / (highest_db - lowest_db)
    return lowest_db + round(s / loud_interval)

def generate_chord_type(v: int) -> int:
    lowest_v = 0
    highest_v = 100
    lowest_timbre = 0
    highest_timbre = 3
    timbre_interval = (highest_v - lowest_v) / (highest_timbre - lowest_timbre)
    return lowest_timbre + round(v / timbre_interval)

def generate_melody(chunk_info: list, note_duration: float, last_note=None):
    pitch = generate_pitch(chunk_info[0])
    loudness = generate_loudness(chunk_info[2])

    # Create a stream for supporting notes
    melody = stream.Stream()

    # Check if last_note is the same as the current pitch
    if last_note and last_note.pitch.midi == pitch:
        # Increase the duration of the last note
        last_note.quarterLength += note_duration
        melody.append(last_note)  # Re-append the modified note
    else:
        midi_note = note.Note(pitch)
        midi_note.quarterLength = note_duration  # Set duration
        midi_note.volume.velocity = loudness  # Set loudness
        melody.append(midi_note)
        last_note = midi_note  # Update last_note for the next iteration

    return melody, last_note

def generate_piano(chunk_info: list, note_duration: float) -> note.Note:
    pitch = generate_pitch(chunk_info[0])
    timbre = generate_chord_type(chunk_info[1])
    loudness = generate_loudness(chunk_info[2])

    if timbre == 0:
        supporting_notes = [ #diminished
            pitch - 6,
            pitch - 12,
            pitch - 9
        ]
    elif timbre == 1:
        supporting_notes = [ #minor
            pitch - 5,
            pitch - 12,
            pitch - 9
        ]
    elif timbre == 2:
        supporting_notes = [ #minor 7
            pitch - 2,
            pitch - 5,
            pitch - 12,
            pitch - 9
        ]
    elif timbre == 3:
        supporting_notes = [ #sus2
            pitch - 5,
            pitch - 12,
            pitch - 9,
        ]
    elif timbre == 4:
        supporting_notes = [ #minor ninth
            pitch + 2,
            pitch - 12,
            pitch - 9,
            pitch - 5,
            pitch - 2
        ]
    elif timbre == 5:
        supporting_notes = [ #major ninth
            pitch + 2,
            pitch - 12,
            pitch - 8,
            pitch - 5,
            pitch - 2
        ]
    elif timbre == 6:
        supporting_notes = [
            pitch - 5,
            pitch - 12,
            pitch - 7
        ]
    elif timbre == 7:
        supporting_notes = [
            pitch - 2,
            pitch - 5,
            pitch - 12,
            pitch - 8
        ]
    else:
        supporting_notes = [
            pitch - 5,
            pitch - 12,
            pitch - 8,
        ]


    # Create a stream for supporting notes
    supporting_stream = stream.Stream()

    for supporting_pitch in supporting_notes:
        midi_note = note.Note(supporting_pitch)
        midi_note.quarterLength = note_duration / len(supporting_notes)  # Divide duration among notes
        midi_note.volume.velocity = loudness - 10  # Slightly quieter for support
        supporting_stream.append(midi_note)

    return supporting_stream

# Create streams to hold the notes



names = [
    'IMG\\1.jpg',
    'IMG\\2.jpg',
    'IMG\\3.jpg',
    'IMG\\4.jpg',
    'IMG\\5.jpg',
    'IMG\\6.jpg',
    'IMG\\7.jpg',
    'IMG\\8.jpg',
    'IMG\\9.jpg',
    'IMG\\10.jpg',
    'IMG\\11.jpg',
    'IMG\\12.jpg',
    'IMG\\13.jpg',
    'IMG\\14.jpg',
    'IMG\\15.jpg'
]

# Generate sounds for each chunk of data
 # Initialize to keep track of the last melody note

for name in names:
    last_melody_note = None

    melody = stream.Stream()
    piano = stream.Stream()

    chunk_data = split_image(300, name)
    for chunk_info in chunk_data:
        # Generate supporting piano notes
        supporting_notes = generate_piano(chunk_info, 1.5)
        piano.append(supporting_notes)

        # Generate melody and update last note
        melody_notes, last_melody_note = generate_melody(chunk_info, 1.5, last_melody_note)
        melody.append(melody_notes)

    # Save the melody and piano accompaniment,
    melody.write('midi', fp=f'{name}.mid')
    piano.write('midi', fp=f'{name}piano.mid')

    os.system(f"fluidsynth -ni soundfont.sf2 {name}.mid -F {name}.wav -n audio.file")
    os.system(f"fluidsynth -ni soundfont.sf2 {name}piano.mid -F {name}piano.wav -n audio.file")

    os.remove(f'{name}.mid')
    os.remove(f'{name}piano.mid')

    wav1 = AudioSegment.from_wav(f"{name}.wav")
    wav2 = AudioSegment.from_wav(f"{name}piano.wav")

    if len(wav1) > len(wav2):
        wav1 = wav1[:len(wav2)]
    else:
        wav2 = wav2[:len(wav1)]

    combined = wav1.overlay(wav2)

    combined.export(f"{name}.mp3", format = "mp3")

    os.remove(f"{name}.wav")
    os.remove(f"{name}piano.wav")

    print(f'{name}.mp3 created')
