#exercice 1
def count_bits(n):
    return bin(n).count('1')
#exercice 2
print(count_bits(7))   
print(count_bits(10)) 
def swap_bits(n, i, j):
    bit_i = (n >> i) & 1
    bit_j = (n >> j) & 1

    if bit_i != bit_j:
        n ^= (1 << i)
        n ^= (1 << j)

    return n

print(swap_bits(73, 1, 6))  # Sortie : 11