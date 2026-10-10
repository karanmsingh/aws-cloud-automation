def url_encode(input_string):
    """
    Encodes a string by converting special characters to hex representation.
    Characters are considered special if they are non-alphanumeric or have
    ASCII values greater than 127.
    
    Args:
        input_string (str): The string to encode
        
    Returns:
        str: The encoded string
    """
    hex_output = ""
    
    for char in input_string:
        if ord(char) > 127 or not char.isalnum():
            # Convert special character to hex
            hex_value = format(ord(char), '02x')
            hex_output += f'\\x{hex_value}'
        else:
            hex_output += char
            
    return hex_output

def main():
    """Main function to handle user input and display results."""
    print("URL Encoder - Convert special characters to hex representation")
    print("=" * 60)
    
    while True:
        input_string = input("\nEnter a string to encode (or 'exit' to quit): ")
        
        if input_string.lower() == 'exit':
            print("Exiting program. Goodbye!")
            break
            
        encoded_string = url_encode(input_string)
        
        print("\nOriginal string:", input_string)
        print("Encoded string: ", encoded_string)
        
        # Show examples of characters that were encoded
        print("\nEncoding details:")
        for i, (original, encoded) in enumerate(zip(input_string, encoded_string)):
            if original != encoded and len(encoded) > 1:
                print(f"  '{original}' (ASCII: {ord(original)}) → {encoded}")

if __name__ == "__main__":
    main()
