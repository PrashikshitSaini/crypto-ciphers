import random
import math

def is_prime(n, k=5):
    """
    Miller-Rabin primality test.
    
    Args:
        n: Number to test for primality
        k: Number of test rounds (higher k increases accuracy)
    
    Returns:
        bool: True if probably prime, False if definitely composite
    """
    if n <= 1 or n == 4:
        return False
    if n <= 3:
        return True
    
    # Write n-1 as 2^r * d
    d = n - 1
    r = 0
    while d % 2 == 0:
        d //= 2
        r += 1
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def generate_large_prime(bits=256):
    """
    Generate a large prime number with specified bit size.
    
    Args:
        bits: Number of bits in the prime number
    
    Returns:
        A prime number of the specified bit size
    """
    while True:
        # Generate random number of specified bit size
        num = random.getrandbits(bits)
        # Make sure it's odd
        num |= 1
        # Ensure it's the right bit size
        num |= (1 << (bits - 1))
        # Test for primality
        if is_prime(num):
            return num

def find_primitive_root(p):
    """
    Find a primitive root (generator) for the prime p.
    
    Args:
        p: Prime number
    
    Returns:
        A primitive root (generator) for prime p
    """
    if p == 2:
        return 1
    
    # Find the prime factors of p-1
    factors = set()
    phi = p - 1
    
    # Find prime factors of phi
    n = phi
    for i in range(2, int(math.sqrt(phi)) + 1):
        if n % i == 0:
            factors.add(i)
            while n % i == 0:
                n //= i
    if n > 1:
        factors.add(n)
    
    # Test random values until a primitive root is found
    while True:
        g = random.randint(2, p - 1)
        if all(pow(g, phi // factor, p) != 1 for factor in factors):
            return g

def mod_exp(base, exponent, modulus):
    """
    Calculate (base^exponent) % modulus efficiently.
    
    Args:
        base: Base value
        exponent: Exponent value
        modulus: Modulus value
    
    Returns:
        (base^exponent) % modulus
    """
    return pow(base, exponent, modulus)

def generate_private_key(p):
    """
    Generate a private key (a) for Diffie-Hellman.
    
    Args:
        p: Prime modulus
        
    Returns:
        A random integer between 2 and p-2
    """
    return random.randint(2, p - 2)

def compute_public_key(g, private_key, p):
    """
    Compute the public key (A = g^a mod p) for Diffie-Hellman.
    
    Args:
        g: Generator
        private_key: Private key (a)
        p: Prime modulus
        
    Returns:
        Public key (A)
    """
    return mod_exp(g, private_key, p)

def compute_shared_secret(other_public_key, private_key, p):
    """
    Compute the shared secret (s = B^a mod p) for Diffie-Hellman.
    
    Args:
        other_public_key: The other party's public key (B)
        private_key: Own private key (a)
        p: Prime modulus
        
    Returns:
        Shared secret (s)
    """
    return mod_exp(other_public_key, private_key, p)

def diffie_hellman_demo(use_predefined=False):
    """
    Complete demonstration of the Diffie-Hellman key exchange protocol.
    
    Args:
        use_predefined: If True, use predefined values for demonstration.
                       If False, generate random values.
    """
    print("Diffie-Hellman Key Exchange Demonstration\n")
    
    if use_predefined:
        # Using small predefined values for demonstration
        p = 23  # Prime modulus
        g = 5   # Generator
        print(f"Using predefined values for demo: p = {p}, g = {g}")
    else:
        # Generate cryptographically secure parameters
        print("Generating cryptographically secure parameters...")
        p = generate_large_prime(bits=512)  # Use 2048+ bits for real applications
        g = find_primitive_root(p)
        print(f"Prime modulus p = {p}")
        print(f"Generator g = {g}")
    
    print("\nStep 1: Alice and Bob agree on public parameters p and g")
    
    # Alice generates her keys
    print("\nStep 2: Alice generates her private and public keys")
    alice_private = generate_private_key(p)
    alice_public = compute_public_key(g, alice_private, p)
    print(f"Alice's private key (a): {alice_private}")
    print(f"Alice's public key (A = g^a mod p): {alice_public}")
    
    # Bob generates his keys
    print("\nStep 3: Bob generates his private and public keys")
    bob_private = generate_private_key(p)
    bob_public = compute_public_key(g, bob_private, p)
    print(f"Bob's private key (b): {bob_private}")
    print(f"Bob's public key (B = g^b mod p): {bob_public}")
    
    # Alice and Bob exchange public keys and compute the shared secret
    print("\nStep 4: Alice and Bob exchange public keys")
    
    # Alice computes the shared secret
    print("\nStep 5: Alice computes the shared secret using Bob's public key")
    alice_shared_secret = compute_shared_secret(bob_public, alice_private, p)
    print(f"Alice's computation: s = B^a mod p = {bob_public}^{alice_private} mod {p} = {alice_shared_secret}")
    
    # Bob computes the shared secret
    print("\nStep 6: Bob computes the shared secret using Alice's public key")
    bob_shared_secret = compute_shared_secret(alice_public, bob_private, p)
    print(f"Bob's computation: s = A^b mod p = {alice_public}^{bob_private} mod {p} = {bob_shared_secret}")
    
    # Verify that both have the same shared secret
    print("\nStep 7: Verify that both shared secrets are identical")
    if alice_shared_secret == bob_shared_secret:
        print(f"✓ Success! Both Alice and Bob have computed the same shared secret: {alice_shared_secret}")
        # In practice, this shared secret would be used to derive symmetric encryption keys
        print("\nThis shared secret can now be used to derive symmetric encryption keys.")
    else:
        print("❌ Error! The shared secrets do not match. Something went wrong.")

if __name__ == "__main__":
    # Run with smaller numbers for demonstration
    diffie_hellman_demo(use_predefined=True)
    
    # Uncomment to run with cryptographically secure parameters (slower)
    # diffie_hellman_demo(use_predefined=False)
