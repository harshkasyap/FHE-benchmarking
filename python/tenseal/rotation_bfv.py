import tenseal as ts
import time
import numpy as np

# -------------------------------
# Parameters
# -------------------------------
n = 10**6
poly_mod_degree = 32768
plain_modulus = 1032193   # large prime

# -------------------------------
# Context Setup
# -------------------------------
context = ts.context(
    ts.SCHEME_TYPE.BFV,         # scheme
    poly_mod_degree,            # polynomial modulus degree
    plain_modulus               # plaintext modulus
)
context.generate_galois_keys()

print("✅ BFV context created and Galois keys generated.")

# -------------------------------
# Data and Encryption
# -------------------------------
data = np.random.randint(0, 100, size=n).tolist()
enc_vector = ts.bfv_vector(context, data)

rotation_steps = 100
print(f"\nTesting rotation with vector size {n} and rotation step {rotation_steps}")

# Left rotation
start = time.time()
enc_rot_left = enc_vector.rotate_left(rotation_steps)
print(f"⏱️ Left rotation time (BFV): {time.time() - start:.4f} s")

# Right rotation
start = time.time()
enc_rot_right = enc_vector.rotate_right(rotation_steps)
print(f"⏱️ Right rotation time (BFV): {time.time() - start:.4f} s")
