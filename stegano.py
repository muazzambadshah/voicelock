# stegano.py

import numpy as np
import scipy.io.wavfile as wav

# --- Helper: Convert message to binary ---
def str_to_bin(message):
    return ''.join(format(ord(char), '08b') for char in message)

# --- Helper: Convert binary to string ---
def bin_to_str(binary):
    chars = [binary[i:i+8] for i in range(0, len(binary), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

# --- Hide text in audio ---
def hide_message(audio_path, message, output_path="stego_output.wav"):
    rate, data = wav.read(audio_path)
    if data.ndim > 1:
        data = data[:, 0]  # Only use one channel

    message_bin = str_to_bin(message) + '1111111111111110'  # EOF marker
    data_flat = data.flatten()

    if len(message_bin) > len(data_flat):
        raise ValueError("Message too long for this audio file.")

    # Modify LSB
    for i, bit in enumerate(message_bin):
        data_flat[i] = (data_flat[i] & ~1) | int(bit)

    wav.write(output_path, rate, data_flat.astype(data.dtype))
    print(f"[✓] Message hidden -> {output_path}")

# --- Extract text from audio ---
def extract_message(stego_path):
    rate, data = wav.read(stego_path)
    if data.ndim > 1:
        data = data[:, 0]

    data_flat = data.flatten()
    bits = ''.join([str(sample & 1) for sample in data_flat])

    # Stop at EOF pattern
    eof = bits.find('1111111111111110')
    message_bits = bits[:eof]

    message = bin_to_str(message_bits)
    print(f"[✓] Hidden message extracted:\n{message}")
    return message

# --- CLI Menu ---
if __name__ == "__main__":
    print("1. Hide Message\n2. Extract Message")
    choice = input("Select an option: ")

    if choice == "1":
        path = input("Enter path to .wav file: ")
        secret = input("Enter secret message to hide: ")
        hide_message(path, secret)
    elif choice == "2":
        path = input("Enter path to stego .wav file: ")
        extract_message(path)
    else:
        print("Invalid choice.")
