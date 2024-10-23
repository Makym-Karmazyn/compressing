import random
import string
import hashlib
import os
import time
import logging
from database import load_code, check_password, save_code

logging.getLogger('sqlalchemy.engine').removeHandler(logging.CRITICAL)

# Декоратор для вимірювання часу виконання функцій
def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"time: {end_time - start_time:.4f} seconds")
        return result
    return wrapper



# Функція для генерації пароля
def generate_password():
    characters = string.ascii_letters + string.digits
    password = ''.join(random.choice(characters) for i in range(11))
    return password


# ООП для вузлів дерева
class Node:
    def __init__(self, probability, symbol, left=None, right=None):
        self.probability = probability
        self.symbol = symbol
        self.left = left
        self.right = right
        self.code = ''


# Функція для обчислення ймовірностей символів у даних
def calculate_probability(data):
    symbols = {}
    for item in data:
        symbols[item] = item.count(item)
    return symbols


# Функція для розрахунку кодів символів
def calculate_codes(node, value=''):
    codes = {}
    new_value = value + str(node.code)
    if node.left:
        codes.update(calculate_codes(node.left, new_value))
    if node.right:
        codes.update(calculate_codes(node.right, new_value))
    if not node.left and not node.right:
        codes[node.symbol] = new_value
    return codes


# Функція для кодування
def output_encoded(data, coding):
    return ''.join([coding[element] for element in data])


# Функція для запису бітової послідовності у файл
def write_bits_to_file(file_name, encoded_data, password):
    with open(file_name, 'wb') as f:
        byte_array = bytearray()
        f.write(password.encode('utf-8') + b'\n')
        for i in range(0, len(encoded_data), 8):
            byte_chunk = encoded_data[i:i + 8]
            byte_array.append(int(byte_chunk, 2))
        f.write(byte_array)


# Функція для декодування бітової послідовності з файлу
def read_bits_from_file(file_name):
    with open(file_name, 'rb') as f:
        password = f.readline().strip().decode('utf-8')
        byte_data = f.read()
        bits = ''.join(format(byte, '08b') for byte in byte_data)
    return password, bits


# Основна функція стискання з паралелізмом
@timer
def huffman_encoding(data):
    symbol_with_probs = calculate_probability(data)
    nodes = [Node(prob, symbol) for symbol, prob in symbol_with_probs.items()]

    while len(nodes) > 1:
        nodes = sorted(nodes, key=lambda x: x.probability)
        left = nodes.pop(0)
        right = nodes.pop(0)
        left.code = '0'
        right.code = '1'
        new_node = Node(left.probability + right.probability, left.symbol + right.symbol, left, right)
        nodes.append(new_node)

    codes = calculate_codes(nodes[0])

    password = generate_password()
    while check_password(password):
        password = generate_password()

    save_code(codes, password)
    encoded_output = output_encoded(data, codes)
    return encoded_output, nodes[0], password


# Функція декодування
@timer
def huffman_decoding(encoded_data, huffman_tree):
    tree_head = huffman_tree
    decoded_output = []
    for bit in encoded_data:
        huffman_tree = huffman_tree.right if bit == '1' else huffman_tree.left
        if not huffman_tree.left and not huffman_tree.right:
            decoded_output.append(huffman_tree.symbol)
            huffman_tree = tree_head
    return ''.join(decoded_output)


# Функція декодування з використанням бази даних кодів
@timer
def huffman_decoding_using_db(encoded_data, password):
    codes = load_code(password)  # Завантажуємо коди з бази даних
    reverse_codes = {code: symbol for symbol, code in codes.items()}  # Інвертуємо словник

    decoded_output = []
    temp_code = ''
    for bit in encoded_data:
        temp_code += bit
        if temp_code in reverse_codes:
            decoded_output.append(reverse_codes[temp_code])
            temp_code = ''

    return ''.join(decoded_output)


# Порівняння розміру початкового та стиснутого файлу
def compare_file_sizes(original_file, compressed_file):
    original_size = os.path.getsize(original_file)
    compressed_size = os.path.getsize(compressed_file)
    print(f"Original file size: {original_size} bytes")
    print(f"Compressed file size: {compressed_size} bytes")
    return original_size, compressed_size

def compress(name_file):
    with open(f"{name_file}.txt", "r") as first_file:
        file = first_file.read()

        # Стиснення
    encoded_data, huffman_tree, password = huffman_encoding(file)
    # print(f"Password for this file: {password}")

    # Запис у файл
    compressed_file = f"{name_file}_compressed.bin"
    write_bits_to_file(compressed_file, encoded_data, password)



    # Порівняння розмірів
    original, compressed = compare_file_sizes(f"{name_file}.txt", compressed_file)

    return original, compressed

def decompress(name_file):
    password, encoded_bits = read_bits_from_file(f"{name_file}_compressed.bin")
    # Декодування за допомогою кодів із бази даних
    decoded_data = huffman_decoding_using_db(encoded_bits, password)
    # Запис у файл
    with open(f"{name_file}_decompressed.txt", "w") as new_file:
        new_file.write(decoded_data)
    return "file is succesfully decompressed"
