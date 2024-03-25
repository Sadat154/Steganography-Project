def generate_decimal_value(bit_position):
    if not (0 <= bit_position <= 7):
        raise ValueError("Bit position must be between 0 and 7 (inclusive)")

    # Create a bitmask with all bits up to and including the input bit set to 1
    bitmask = (1 << (bit_position + 1)) - 1

    return bitmask

# Example usage:
input_bit_position = 6
result = generate_decimal_value(input_bit_position)
print(f"Decimal value with all bits up to bit {input_bit_position} set to 1: {result}")

x = 255

bitpos = 0
bitchoice = bitpos+1
ans = 0
for i in range(0, (8-bitchoice)):

    y = (1 << (i))
    ans += y

finalAns = 255 - ans
print(finalAns)

