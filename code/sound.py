from music21 import stream, note, midi

# Define chunk data
chunk_data = [
    [1, 2, 3],
    [255, 99, 99],
    [255, 99, 99],
    [255, 99, 42],
    [155, 9, 32],
    [55, 10, 35],
    [75, 30, 16],
    [100, 69, 63]
]

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
    lowest_db = 60
    highest_db = 90
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

    # Set dynamic (loudness)
    midi_note.volume.velocity = loudness

    return midi_note

# Create a stream to hold the notes
melody = stream.Stream()

# Generate sounds for each chunk of data
for chunk_info in chunk_data:
    melody.append(generate_piano_sound(chunk_info, 0.5))  # Each chunk's sound is generated with its own loudness

# Save the melody as a MIDI file
melody.write('midi', fp='piano_sound1.mid')

print('Piano music generated and saved as piano_sound.mid')
