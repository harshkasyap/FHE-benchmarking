import tenseal as ts
import time
import numpy as np

# -------------------------------
# Parameters
# -------------------------------
n = 10**6
poly_mod_degree = 32768  # large enough for big vectors
plain_modulus = 1032193   # should be prime and large enough

# -------------------------------
# Context Setup
# -------------------------------
context = ts.context(
    ts.SCHEME_TYPE.BFV,
    poly_mod_degree=poly_mod_degree,
    plain_modulus=plain_modulus
)
context.generate_galois_keys()

print("BFV context created and Galois keys generated.")

# -------------------------------
# Data and Encryption
# -------------------------------
data = np.random.randint(0, 100, size=n).tolist()
enc_vector = ts.bfv_vector(context, data)

# -------------------------------
# Rotation Tests
# -------------------------------
rotation_steps = 100  # you can change this
print(f"\nTesting rotation with vector size {n} and rotation step {rotation_steps}")

# Left rotation
start = time.time()
enc_rot_left = enc_vector.rotate_left(rotation_steps)
end = time.time()
print(f"Left rotation time (BFV): {end - start:.4f} seconds")

# Right rotation
start = time.time()
enc_rot_right = enc_vector.rotate_right(rotation_steps)
end = time.time()
print(f"Right rotation time (BFV): {end - start:.4f} seconds")# cook your dish here
