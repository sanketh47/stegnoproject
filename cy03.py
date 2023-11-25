import cv2
import numpy as np

def dct_encode(img, message):
    # Apply Discrete Cosine Transform (DCT) to the image
    img_dct = cv2.dct(np.float32(img)/255.0)

    # Flatten the message
    flat_msg = [ord(char) for char in message]

    # Embed the message in the DCT coefficients
    for i, value in enumerate(flat_msg):
        row = i // img.shape[1]
        col = i % img.shape[1]
        img_dct[row, col, 0] += value / 10.0  # Adjust the scaling factor for strength

    return img_dct

def dct_decode(img_dct, message_length):
    # Extract the message from the DCT coefficients
    extracted_msg = ""
    for i in range(message_length):
        row = i // img_dct.shape[1]
        col = i % img_dct.shape[1]
        extracted_msg += chr(int(img_dct[row, col, 0] * 10.0))  # Adjust the scaling factor

    return extracted_msg

# Load image
img = cv2.imread("triumph.jpg")

if img is None:
    print("Error: Image not found or cannot be read.")
    exit()

# Input secret message
msg = input("Enter your secret message: ")
password = input("Enter a password: ")

# Encode message using DCT
encoded_img_dct = dct_encode(img, msg)

# Save the encoded image
cv2.imwrite("encryptedmsg_dct.jpg", cv2.idct(encoded_img_dct)*255.0)

# Reset variables for decoding
decoded_message = ""

# Input password for decoding
pas = input("Enter your password: ")

# Decode message using DCT
if password == pas:
    decoded_message = dct_decode(encoded_img_dct, len(msg))
    print("Decoded message:", decoded_message)
else:
    print("Password not valid")
