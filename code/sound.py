from music21 import stream, note, midi
from PIL import Image


def get_hue_saturation_brightness(chunk):
    # Convert the image chunk to HSV (Hue, Saturation, Value)
    hsv_image = chunk.convert("HSV")

    # Get pixel data and calculate average values for hue, saturation, and brightness (value)
    pixels = list(hsv_image.getdata())

    # Separate into individual channels
    hue_values = [pixel[0] for pixel in pixels]  # Hue channel
    saturation_values = [pixel[1] for pixel in pixels]  # Saturation channel
    brightness_values = [pixel[2] for pixel in pixels]  # Brightness (value) channel

    # Calculate the average hue, saturation, and brightness
    avg_hue = sum(hue_values) / len(hue_values)
    avg_saturation = sum(saturation_values) / len(saturation_values)
    avg_brightness = sum(brightness_values) / len(brightness_values)

    return avg_hue, avg_saturation, avg_brightness


def split_image(size):
    image = Image.open("space.jpg")

    chunk_width = size
    chunk_height = size

    img_width, img_height = image.size
    chunks = []
    chunk_attributes = []  # List to store attributes

    for top in range(0, img_height, chunk_height):
        for left in range(0, img_width, chunk_width):
            # Define the box (left, upper, right, lower)
            box = (left, top, left + chunk_width, top + chunk_height)

            # Crop the image using the box
            chunk = image.crop(box)

            # Save each chunk as a separate image file or append to a list
            chunks.append(chunk)

            # Get the hue, saturation, and brightness for the chunk
            avg_hue, avg_saturation, avg_brightness = get_hue_saturation_brightness(chunk)

            # Get and store attributes like dimensions and color mode
            chunk_size = chunk.size  # (width, height)
            chunk_mode = chunk.mode  # Color mode (e.g., 'RGB')

            # Append the attributes directly as a list
            chunk_attributes.append([
                int(avg_hue),  # average hue
                int(avg_saturation),  # average saturation
                int(avg_brightness)  # average brightness
            ])

    return chunk_attributes


chunk_data = split_image(50)

from music21 import stream, note, midi

# Define chunk data

from music21 import stream, note, midi

# Define chunk data
from music21 import stream, note, midi


def generate_pitch(h: int) -> int:
    lowest_h = 0
    highest_h = 360
    lowest_midi = 36  # Lowest MIDI note
    highest_midi = 108  # Highest MIDI note
    note_interval = (highest_h - lowest_h) / (highest_midi - lowest_midi)
    return lowest_midi + round(h / note_interval)


def generate_loudness(s: int) -> int:
    lowest_s = 0
    highest_s = 100
    lowest_db = 40
    highest_db = 60
    loud_interval = (highest_s - lowest_s) / (highest_db - lowest_db)
    return lowest_db + round(s / loud_interval)


def generate_timbre(v: int) -> int:
    lowest_v = 0
    highest_v = 100
    lowest_timbre = 0
    highest_timbre = 3
    timbre_interval = (highest_v - lowest_v) / (highest_timbre - lowest_timbre)
    return lowest_timbre + round(v / timbre_interval)


def generate_piano_sound(chunk_info: list, note_duration: float) -> note.Note:
    pitch = generate_pitch(chunk_info[0])
    loudness = generate_loudness(chunk_info[1])
    timbre = generate_timbre(chunk_info[2])

    # Create a MIDI note
    midi_note = note.Note(pitch)
    midi_note.quarterLength = note_duration  # Set duration in quarter lengths
    midi_note.volume.velocity = loudness

    return midi_note


def generate_supporting_piano(chunk_info: list, note_duration: float) -> note.Note:
    pitch = generate_pitch(chunk_info[0])
    loudness = generate_loudness(chunk_info[1])
    timbre = generate_timbre(chunk_info[2])

    # Create a supporting piano note (using a different pattern)
    supporting_notes = [
        pitch - 12,  # One octave below
        pitch - 7,  # Perfect fifth below
        pitch - 5  # Perfect fourth below
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
melody = stream.Stream()
supporting_piano = stream.Stream()

# Generate sounds for each chunk of data
for chunk_info in chunk_data:
    # Generate main piano melody note
    new_note = generate_piano_sound(chunk_info, 0.5)

    # Check for merging notes
    if melody and melody[-1].name == new_note.name:
        melody[-1].quarterLength += new_note.quarterLength
    else:
        melody.append(new_note)

    # Generate supporting piano notes
    supporting_notes = generate_supporting_piano(chunk_info, 1.0)

    # Append supporting notes to the supporting stream
    supporting_piano.append(supporting_notes)

# Combine the melody and supporting track into a single stream
combined = stream.Score()
combined.append(melody)
combined.append(supporting_piano)

# Save the combined melody and support as a MIDI file
combined.write('midi', fp='piano_with_supporting_piano3.mid')

print('Piano music with supporting piano track generated and saved as piano_with_supporting_piano.mid')
