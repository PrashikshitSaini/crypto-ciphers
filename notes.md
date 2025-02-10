### **1. Stream Ciphers**

#### **A5/1 (GSM Encryption)**

- **Structure**:
  - 3 LFSRs (Lengths: 19, 22, 23 bits).
  - **Clocking Rule**: Majority function on bits 8, 10, 10 of each LFSR.
  - **Output**: XOR of the 3 LFSRs’ least significant bits.
- **Example**:
  - _Alice_ sends an encrypted SMS to _Bob_.
  - **Key Setup**: 64-bit key + 22-bit frame number → XOR to initialize LFSRs.
  - **Attack by Trudy**:
    - _Trudy_ records 64 bits of keystream and uses a **time-memory trade-off** (Rainbow Table) to recover the key in \( 2^{54} \) operations.
- **Math**:
  - Feedback polynomials (e.g., LFSR1: \( x^{19} + x^{18} + x^{17} + x^{14} + 1 \)).

---

#### **RC4 (SSL/WEP)**

- **Algorithm**:
  1. **Key Scheduling (KSA)**:
     - Initialize S-box (0-255).
     - Scramble S-box with key:
       ```python
       j = 0
       for i in 0 to 255:
           j = (j + S[i] + key[i % keylen]) % 256
           swap(S[i], S[j])
       ```
  2. **PRGA (Keystream)**:
     ```python
     i = j = 0
     while True:
         i = (i + 1) % 256
         j = (j + S[i]) % 256
         swap(S[i], S[j])
         yield S[(S[i] + S[j]) % 256]
     ```
- **Example**:
  - _Alice_ uses RC4 in WEP (flawed!).
  - **Key**: "AliceKey" (ASCII hex: 41 6C 69 63 65 4B 65 79).
  - _Trudy_ exploits the **FMS attack** (Fluhrer-Mantin-Shamir):
    - Weak IVs (e.g., 0x03 0xFF 0xXX) leak key bytes via statistical biases.

---

### **2. Block Ciphers**

#### **DES (Data Encryption Standard)**

- **Feistel Structure**:
  - 64-bit block, 56-bit key, 16 rounds.
  - **Round Function \( F(R, K) \)**:
    1. **Expansion**: 32-bit \( R \) → 48 bits via permutation.
    2. **Key Mixing**: \( \text{XOR}(E(R), K\_{\text{sub}}) \).
    3. **S-Boxes**: 8 non-linear 6→4-bit substitutions (e.g., S1: 0x0E → 14).
    4. **Permutation (P-box)**: Diffuse bits.
- **Math**:
  - Key Schedule: Permuted Choice 1 (PC1) → 56 bits → split into \( C_0, D_0 \).
  - Each round: Left shift \( C_i, D_i \) (e.g., round 1: 1 shift, round 2: 1 shift, ..., round 16: 2 shifts).
- **Example**:
  - _Alice_ encrypts "Hello!" (hex: 48 65 6C 6C 6F 21) with DES.
  - **Key**: "DESkey56" (56 bits).
  - _Trudy_ brute-forces in \( 2^{56} \) steps (≈ 72 quadrillion attempts).

---

#### **AES (Advanced Encryption Standard)**

- **Rijndael Structure** (SPN):
  - **State**: 4x4 byte matrix (128 bits).
  - **Key Expansion**:
    - 128-bit key → 44 words (176 bytes) using XOR, rotation, and S-box.
  - **Round Steps**:
    1. **SubBytes**: Non-linear S-box (e.g., \( \text{SubByte}(0x53) = 0xED \)).
    2. **ShiftRows**: Cyclic shifts (Row 0: 0, Row 1: 1, Row 2: 2, Row 3: 3).
    3. **MixColumns**: Matrix multiplication in GF(\( 2^8 \)):  
       \[  
       \begin{bmatrix}  
       02 & 03 & 01 & 01 \\  
       01 & 02 & 03 & 01 \\  
       01 & 01 & 02 & 03 \\  
       03 & 01 & 01 & 02  
       \end{bmatrix}  
       \times  
       \begin{bmatrix}  
       s*{0,c} \\  
       s*{1,c} \\  
       s*{2,c} \\  
       s*{3,c}  
       \end{bmatrix}  
       \]
    4. **AddRoundKey**: XOR with round key.
- **Example**:
  - _Alice_ encrypts "CryptoIsFun" (128-bit block) with AES-256.
  - **Key**: 256-bit randomly generated.
  - _Trudy_ attempts side-channel attacks but fails due to masking.

---

### **3. Public Key Cryptography**

#### **RSA (Rivest-Shamir-Adleman)**

- **Key Generation**:
  1. Choose primes \( p = 11 \), \( q = 23 \).
  2. Compute \( n = p \times q = 253 \), \( \phi(n) = (p-1)(q-1) = 220 \).
  3. Choose \( e = 3 \) (coprime to \( \phi(n) \)).
  4. Compute \( d = e^{-1} \mod \phi(n) = 147 \).
- **Encryption**: \( c = m^e \mod n \).
  - _Bob_ sends \( m = 100 \): \( c = 100^3 \mod 253 = 156 \).
- **Decryption**: \( m = c^d \mod n = 156^{147} \mod 253 = 100 \).
- **Attack**:
  - _Trudy_ tries to factor \( n = 253 \) → \( p = 11 \), \( q = 23 \), but fails for large \( n \) (e.g., 2048 bits).

---

#### **Digital Signatures (RSA-Based)**

- **Signing**:
  1. _Alice_ hashes message \( M \) → \( H(M) = \text{SHA-256}(M) \).
  2. Encrypts hash with private key: \( \text{Signature} = H(M)^d \mod n \).
- **Verification**:
  1. _Bob_ decrypts signature with Alice’s public key: \( H'(M) = \text{Signature}^e \mod n \).
  2. Compares \( H'(M) \) with \( \text{SHA-256}(M) \).
- **Example**:
  - _Alice_ signs "Transfer $100" → _Trudy_ can’t reuse the signature for "Transfer $1000" (hash mismatch).

---

### **4. Knapsack Cryptosystem**

#### **Merkle-Hellman (Broken)**

- **Key Generation**:
  1. **Superincreasing Sequence**: \( \{2, 3, 6, 13\} \).
  2. Choose modulus \( M = 20 > \sum a_i \), multiplier \( W = 7 \) (coprime to \( M \)).
  3. **Public Key**: \( b_i = W \times a_i \mod M → \{14, 1, 2, 11\} \).
- **Encryption**:
  - _Bob_ encrypts bits \( 1101 \) → \( S = 14 + 1 + 11 = 26 \).
- **Decryption**:
  1. Compute \( S' = W^{-1} \times S \mod M = 3 \times 26 \mod 20 = 18 \).
  2. Solve superincreasing knapsack: \( 13 + 6 - 1 = 18 \).
- **Shamir’s Lattice Attack**:
  - _Trudy_ constructs a lattice from public key \( \{14, 1, 2, 11\} \).
  - Uses **LLL algorithm** to find short vectors, recovering \( W = 7 \), \( M = 20 \).

---

### **5. Real-World Examples**

1. **A5/1 in GSM**:
   - _Alice_ calls _Bob_. _Trudy_ intercepts traffic but fails to decrypt due to A5/3.
2. **RC4 in WEP**:
   - _Trudy_ cracks _Alice_’s Wi-Fi by capturing 40,000 IVs (FMS attack).
3. **AES in TLS**:
   - _Alice_ visits "https://bank.com". AES-256 encrypts her session.
4. **RSA in SSH**:
   - _Bob_ logs into a server using RSA-2048. _Trudy_ cannot factor \( n \).

---

### **6. Mathematical Appendix**

#### **Galois Field GF(\( 2^8 \))**

- **Addition**: XOR (e.g., \( 0x57 + 0x83 = 0xD4 \)).
- **Multiplication**: Polynomial multiplication modulo \( x^8 + x^4 + x^3 + x + 1 \).
  - Example: \( 0x57 \times 0x83 \):
    - \( (x^6 + x^4 + x^2 + x + 1)(x^7 + x + 1) \mod \text{irreducible} \).

#### **LLL Algorithm (Lattice Reduction)**

- **Goal**: Find short, nearly orthogonal vectors in a lattice.
- **Knapsack Attack**: Reduces breaking Merkle-Hellman to polynomial time.
