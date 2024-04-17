def decimal_to_binary(decimal_value):
    # Convert decimal to binary string
    binary_string = bin(decimal_value)[2:]  # Remove '0b' prefix from binary string
    # Pad the binary string with leading zeros if necessary to ensure it's 8 bits long
    padded_binary_string = binary_string.zfill(8)
    return padded_binary_string



print(decimal_to_binary((-1)))