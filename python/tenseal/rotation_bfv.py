import tenseal as ts
import time
import numpy as np

# -------------------------------
# Parameters
# -------------------------------
n = 10**6
# CKKS parameters
POLY_MODULUS_DEGREE = 8192   # typical secure choice
COEFF_MOD_BIT_SIZES = [60, 40, 40, 60]  # coefficient modulus bit sizes, used for ckks
PLAIN_MODULUS = 786433         # must be a prime number; can also use 2**20 or 65537, used for bfv

# Create TenSEAL CKKS context
ctx = ts.context(
    ts.SCHEME_TYPE.CKKS,
    poly_modulus_degree=POLY_MODULUS_DEGREE,
    coeff_mod_bit_sizes=COEFF_MOD_BIT_SIZES
)

# Create TenSEAL BFV context
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_modulus_degree=POLY_MODULUS_DEGREE,
    plain_modulus=PLAIN_MODULUS
)

context.generate_galois_keys()   # if you need rotations
context.generate_relin_keys()    # if you need multiplications
context.global_scale = 2**40

# -------------------------------
# Data and Encryption
# -------------------------------
# -------------------------------
# Data preparation and chunking
# -------------------------------
data = np.random.randint(0, 100, size=n).tolist()
chunks = [data[i:i + POLY_MODULUS_DEGREE] for i in range(0, n, POLY_MODULUS_DEGREE)]
print(f"Total chunks created: {len(chunks)}")

# -------------------------------
# Encryption (batched)
# -------------------------------
enc_chunks = []
start = time.time()
for chunk in chunks:
    enc_chunks.append(ts.bfv_tensor(context, chunk, True))
enc_time = time.time() - start
print(f"🔐 Encrypted {len(enc_chunks)} chunks in {enc_time:.2f} s")

# -------------------------------
# Left rotation on all chunks
# -------------------------------
print(f"\nTesting LEFT rotation (step={rotation_steps}) on all chunks...")
start = time.time()
rotated_left = [enc_vec.rotate_left(rotation_steps) for enc_vec in enc_chunks]
left_time = time.time() - start
print(f"⏱️ Total left rotation time (BFV, all chunks): {left_time:.2f} s")

# -------------------------------
# Right rotation on all chunks
# -------------------------------
print(f"\nTesting RIGHT rotation (step={rotation_steps}) on all chunks...")
start = time.time()
rotated_right = [enc_vec.rotate_right(rotation_steps) for enc_vec in enc_chunks]
right_time = time.time() - start
print(f"⏱️ Total right rotation time (BFV, all chunks): {right_time:.2f} s")

# -------------------------------
# Summary
# -------------------------------
print("\n====== BFV Rotation Benchmark Summary ======")
print(f"Vector size: {n}")
print(f"Chunks: {len(chunks)} (each {poly_mod_degree} elements)")
print(f"Plain modulus bit size: {plain_mod_bit_size}")
print(f"Left rotation total time:  {left_time:.2f} s")
print(f"Right rotation total time: {right_time:.2f} s")
