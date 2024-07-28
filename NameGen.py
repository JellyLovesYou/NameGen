import itertools
import random
import time
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog

# Mappings for letter-to-number and letter-to-symbol
letter_to_number = {
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7',
    'l': '1', 'L': '1'
}

letter_to_symbol = {
    'a': ['4', '@', 'ä', 'á'], 
    'A': ['4', '@', 'Ä', 'Á'],
    'e': ['3', '€', 'ë', 'é'],
    'E': ['3', '€', 'Ë', 'É'],
    'i': ['1', '!', '|', 'ï'],
    'I': ['1', '!', '|', 'Ï'],
    'o': ['0', '()', '<3', 'ö'],
    'O': ['0', '()', '<3', 'Ö'],
    's': ['5', '$', '§'],
    'S': ['5', '$', '§'],
    't': ['7', '+', '†'],
    'T': ['7', '+', '†'],
    'l': ['1', '|', '!', '£'],
    'L': ['1', '|', '!', '£']
}

def replace_letters(username, mapping):
    """Replace letters in the username based on the given mapping."""
    variations = set()
    positions = [i for i, char in enumerate(username) if char in mapping]
    
    for num_changes in range(0, len(positions) + 1):
        for combo in itertools.combinations(positions, num_changes):
            username_list = list(username)
            for pos in combo:
                char = username_list[pos]
                if char in mapping:
                    replacement = random.choice(mapping[char])
                    username_list[pos] = replacement
            variations.add(''.join(username_list))
    
    return variations

def add_special_characters(usernames):
    """Add special characters (., _) to usernames without repeating ."""
    special_patterns = ['._', '_.', '._.', '_._']
    expanded_usernames = set()
    for username in usernames:
        if len(username) > 32:
            continue  # Skip usernames that exceed the max length
        for pattern in special_patterns:
            for i in range(1, len(username)):
                with_special_char = username[:i] + pattern + username[i:]
                if len(with_special_char) <= 32:
                    expanded_usernames.add(with_special_char)
    
    # Ensure that usernames do not exceed 32 characters and are unique
    return {username[:32] for username in expanded_usernames}

def add_suffixes(usernames, suffixes):
    """Add given suffixes to each username."""
    suffixed_usernames = set()
    for username in usernames:
        if len(username) > 32:
            continue  # Skip usernames that exceed the max length
        for suffix in suffixes:
            suffixed_usernames.add(f"{username}{suffix}")
    return suffixed_usernames

def generate_usernames_with_numbers(base_usernames, output_file):
    """Generate usernames using letter-to-number mapping."""
    all_usernames = set()
    start_time = time.time()
    
    for base in base_usernames:
        print(f"Scrambling {base} with numbers...")
        variations = replace_letters(base, letter_to_number)
        variations_with_special_chars = add_special_characters(variations)
        all_usernames.update(variations_with_special_chars)
        print(f"Finished scrambling {base}. Current unique usernames count: {len(all_usernames)}")
        
        if len(all_usernames) % 10000 == 0:
            print(f"Progress: {len(all_usernames)} unique number-based usernames generated.")
            elapsed_time = time.time() - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds")

    with open(output_file, 'w', encoding='utf-8') as file:
        for username in sorted(all_usernames):
            file.write(f"{username}\n")

def generate_usernames_with_symbols(base_usernames, output_file):
    """Generate usernames using letter-to-symbol mapping."""
    all_usernames = set()
    start_time = time.time()
    
    suffixes = ["", "<3", "</3", "<\\3"]
    for base in base_usernames:
        print(f"Scrambling {base} with symbols...")
        variations = replace_letters(base, letter_to_symbol)
        suffixed_variations = add_suffixes(variations, suffixes)
        suffixed_variations_with_special_chars = add_special_characters(suffixed_variations)
        all_usernames.update(suffixed_variations_with_special_chars)
        print(f"Finished scrambling {base}. Current unique usernames count: {len(all_usernames)}")
        
        if len(all_usernames) % 10000 == 0:
            print(f"Progress: {len(all_usernames)} unique symbol-based usernames generated.")
            elapsed_time = time.time() - start_time
            print(f"Elapsed time: {elapsed_time:.2f} seconds")

    with open(output_file, 'w', encoding='utf-8') as file:
        for username in sorted(all_usernames):
            file.write(f"{username}\n")

def generate_usernames():
    base_usernames = username_input.get().split(',')
    if not base_usernames:
        messagebox.showerror("Error", "Please enter at least one username.")
        return

    numbers_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Number-Based Usernames As")
    if not numbers_file:
        return

    symbols_file = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")], title="Save Symbol-Based Usernames As")
    if not symbols_file:
        return

    # Generate and save usernames with numbers and symbols
    generate_usernames_with_numbers(base_usernames, numbers_file)
    generate_usernames_with_symbols(base_usernames, symbols_file)
    
    messagebox.showinfo("Success", "Usernames have been generated and saved.")

# Create the GUI
root = tk.Tk()
root.title("Username Generator")

tk.Label(root, text="Enter usernames (comma-separated):").pack(pady=10)
username_input = tk.Entry(root, width=50)
username_input.pack(pady=5)

tk.Button(root, text="Generate Usernames", command=generate_usernames).pack(pady=20)

root.mainloop()
