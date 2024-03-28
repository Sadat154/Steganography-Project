import cv2
import sys
import string
import random
import os
import re
from cryptography.fernet import Fernet

def encode():
	print("\n-----------------------------")
	print("|     Encoding Starts..     |")
	print("-----------------------------\n")

	while True: # Asks the user for a carrier name, if none exists returns to start
		image = input("Enter image carrier name (inc. extension)...\n")
		if not image:
			print('Nothing has been Entered!\n')
			continue
		elif not os.path.isfile(image):
			print("\nNo file exists, try again!\n")
			continue
		else:
			break

	image = cv2.imread(image) # Loads image from specified
	max_bytes = (image.shape[0] * image.shape[1]) // 8 # maximum bytes to encode

	while True: # Asks the user for the secret message, if none exists returns to start
		secret_data = input("\nEnter secret message...\n")
		if not secret_data:
			print('Nothing has been Entered!\n')
			continue
		else:
			key = Fernet.generate_key() # Generates a key
			f = Fernet(key) # Assigns variable
			secret_data = f.encrypt(secret_data.encode()) # Encrypts secret message based on key

			secret_data = str(secret_data.decode()) + "e1g0l" # Adds an end delimiter to the message
			secret_data = "SdfD1" + secret_data + str(key.decode()) # Adds a start delimiter to the message
			secret_data = secret_data + "m1Ku1"
			#print(secret_data, "\n") # Test variable

			if len(secret_data) > max_bytes | len(key) > max_bytes:
				print("\n------------ ERROR ------------")
				print("Secret message is too big for the carrier")
				print("Try a bigger carrier or smaller message\n")
				print("RIP G")

			# Finds out the total amount of duplicate secret messages that can be embedded
			sizeOfMessage = sys.getsizeof(secret_data)
			lengthmessage = max_bytes//sizeOfMessage
			new_Secret_Data = secret_data * lengthmessage # Muliplies the secret message
			break # Else continues

	while True: # Asks the user for a new image name, if none exists returns to start
		newfile = input("\nEnter new image name (inc. extension)...\n")
		if not newfile:
			print('Nothing has been Entered!\n')
			continue
		else:
			break

	bank_secretMessage = 0 # Set index values to zero
	b_secretMessage = ''.join([ format(ord(i), "08b") for i in new_Secret_Data ]) # Converts the secret message & key to binary
	len_secretMessage = len(b_secretMessage) # Size of data to hide

	for row in image:
		for pixel in row:
			r, g, b = [ format(i, "08b") for i in pixel ] # Converts RGB pixels to binary
			if bank_secretMessage < len_secretMessage: # If data count is less than length
				pixel[0] = int(r[:-1] + b_secretMessage[bank_secretMessage], 2) # Modify the LSB (Red pixel)
				bank_secretMessage += 1 # Increase count

			if bank_secretMessage < len_secretMessage: # If data count is less than length
				pixel[1] = int(g[:-1] + b_secretMessage[bank_secretMessage], 2) # Modify the LSB (Green pixel)
				bank_secretMessage += 1 # Increase count

			if bank_secretMessage < len_secretMessage: # If data count is less than length
				pixel[2] = int(b[:-1] + b_secretMessage[bank_secretMessage], 2) # Modify the LSB (Blue pixel)
				bank_secretMessage += 1 # Increase count

			# If all data counts are greaterr than lengths
			if bank_secretMessage >= len_secretMessage:
				break

	cv2.imwrite(newfile, image) # Process to write a new image file, newfile = the new image name, image = the image data

	print("\nSteganography encoding complete!")


def decode():
	print("\n-----------------------------")
	print("|     Decoding Starts..     |")
	print("-----------------------------\n")

	while True:  # Asks the user for a carrier name, if none exists returns to start
		image = input("Enter image carrier name (inc. extension)...\n")
		if not image:
			print('Nothing has been Entered!\n')
			continue
		elif not os.path.isfile(image):
			print("\nNo file exists, try again!\n")
			continue
		else:
			break

	image = cv2.imread(image)  # read the image
	bank_secretMessage = ""  # Holds LSB secret message, (Red pixel)

	# Extract LSB and store in binary_data[x]
	for row in image:
		for pixel in row:
			r, g, b = [format(i, "08b") for i in pixel]
			bank_secretMessage += r[-1]
			bank_secretMessage += g[-1]
			bank_secretMessage += b[-1]

	# Divide all LSB and convert to charcters
	all_data_secretMessage = [bank_secretMessage[i: i + 8] for i in range(0, len(bank_secretMessage), 8)]
	decoded_secretMessage = ""

	for byte in all_data_secretMessage:
		decoded_secretMessage += chr(int(byte, 2))

	# Finds the first delimiter, then removes the last 5 chars
	secretMessage = decoded_secretMessage.split("SdfD1")[1]  # [:-5]
	# Takes the secretMessage splits backwards to recover the message, then removes the last 5 chars
	split_1 = secretMessage.split("e1g0l")[1][:-5]
	# Takes the secretMessage splits forwards to recover the key
	split_2 = secretMessage.split("e1g0l")[0]

	decoded = Fernet(split_1).decrypt(split_2.encode())  # Decrypt with key

	print("\n*************************")
	print("*     Secret Message    *")
	print("*************************")
	print(re.sub("(.{40})", "\\1\n", decoded.decode()))  # Prints secret message and displays 40 characters on CLI

	# print(decoded_data[:-5]) # Displays decoded message full width


