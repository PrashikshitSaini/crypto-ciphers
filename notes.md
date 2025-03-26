| **Criteria**                  | **Block Ciphers**                                                             | **Stream Ciphers**                                                                  |
| ----------------------------- | ----------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| **Basic Unit**                | Encrypts data in fixed-size blocks (e.g., 64-bit or 128-bit blocks).          | Encrypts data bit-by-bit or byte-by-byte (as a continuous stream).                  |
| **Encryption Method**         | Uses substitution and permutation (via Feistel networks or SPN structures).   | Combines plaintext with a pseudorandom keystream (generated using a key and nonce). |
| **Speed**                     | Slower for large data (due to block processing and padding).                  | Faster for real-time/bulk data (no padding, minimal latency).                       |
| **Error Propagation**         | Errors in ciphertext affect an entire block (depends on mode, e.g., CBC).     | Errors affect only the corresponding bit/byte (no propagation).                     |
| **Security Considerations**   | Vulnerable to padding oracle attacks (in modes like CBC).                     | Vulnerable if keystream is reused (e.g., WEP’s RC4 key reuse flaw).                 |
| **Use Cases**                 | File encryption, databases, SSL/TLS (with modes like AES-GCM).                | Real-time communication (e.g., Wi-Fi, Bluetooth, VoIP).                             |
| **Padding Requirement**       | Requires padding to fill incomplete blocks (e.g., PKCS#7).                    | No padding needed (works on arbitrary-length data).                                 |
| **Parallel Processing**       | Possible in certain modes (e.g., ECB, CTR).                                   | Not parallelizable (keystream is state-dependent).                                  |
| **Examples**                  | AES, DES, Blowfish, 3DES.                                                     | RC4, ChaCha20, Salsa20, A5/1 (GSM).                                                 |
| **Modes of Operation**        | ECB, CBC, CFB, OFB, CTR, GCM (modes define how blocks are chained/processed). | Typically no modes; keystream is XORed with plaintext directly.                     |
| **Key + Nonce/IV Usage**      | IV required in some modes (e.g., CBC, CTR) to ensure uniqueness.              | Nonce (number used once) required to generate unique keystreams.                    |
| **Memory Efficiency**         | Requires memory to store entire blocks during processing.                     | Minimal memory usage (processes data incrementally).                                |
| **Implementation Complexity** | More complex due to mode selection, padding, and block management.            | Simpler design but relies on secure pseudorandom keystream generation.              |
| **Resistance to Attacks**     | Susceptible to block-level attacks (e.g., meet-in-the-middle for DES).        | Susceptible to keystream reuse (e.g., two-time pad vulnerability).                  |
| **Resource Usage**            | Better suited for hardware acceleration (fixed-block operations).             | Efficient in software (lightweight operations).                                     |
| **Historical Context**        | Dominated early standards (e.g., DES in 1970s).                               | Gained popularity for real-time use cases (e.g., RC4 in 1980s).                     |

---

### **Key Takeaways**:

1. **Block Ciphers**:

   - Ideal for structured/static data (e.g., files, databases).
   - Provide robustness with modes like AES-GCM (combining encryption and authentication).
   - Require careful handling of IVs and padding.

2. **Stream Ciphers**:
   - Optimized for real-time/streaming data (e.g., video, voice).
   - Vulnerable to key/nonce reuse but highly efficient.
   - Modern designs (e.g., ChaCha20) prioritize speed and security.

### **1. Stream Ciphers**

#### **A5/1 (GSM Encryption)**

- **Structure**:
  - 3 LFSRs Linear Feedback Shift Register (Lengths: 19, 22, 23 bits).
  - **Clocking Rule**: Majority function on bits 8, 10, 10 of each LFSR.
  - **Output**: XOR of the 3 LFSRs’ most significant bits.
- **Example**:
  - _Alice_ sends an encrypted SMS to _Bob_.
  - **Key Setup**: 64-bit key + 22-bit frame number → XOR to initialize LFSRs.
  - **Attack by Trudy**:
    - _Trudy_ records 64 bits of keystream and uses a **time-memory trade-off** (Rainbow Table) to recover the key in $2^{54}$ operations.
- **Math**:
  - Feedback polynomials (e.g., LFSR1: $x^{19} + x^{18} + x^{17} + x^{14} + 1$).

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
  - **Round Function $F(R, K)$**:
    1. **Expansion**: 32-bit $R$ → 48 bits via permutation.
    2. **Key Mixing**: $\text{XOR}(E(R), K_{sub})$.
    3. **S-Boxes**: 8 non-linear 6→4-bit substitutions (e.g., S1: 0x0E → 14).
    4. **Permutation (P-box)**: Diffuse bits.
- **Math**:
  - Key Schedule: Permuted Choice 1 (PC1) → 56 bits → split into $C_0, D_0$.
  - Each round: Left shift $C_i, D_i$ (e.g., round 1: 1 shift, round 2: 1 shift, ..., round 16: 2 shifts).
- **Example**:

  - _Alice_ encrypts "Hello!" (hex: 48 65 6C 6C 6F 21) with DES.
  - **Key**: "DESkey56" (56 bits).
  - _Trudy_ brute-forces in $2^{56}$ steps (≈ 72 quadrillion attempts).

  **Video for more understanding:** [Link](https://www.youtube.com/watch?v=FGhj3CGxl8I&ab_channel=Computerphile)

---

#### **AES (Advanced Encryption Standard)**

- **Rijndael Structure** (SPN):
  - **State**: 4x4 byte matrix (128 bits).
  - **Key Expansion**:
    - 128-bit key → 44 words (176 bytes) using XOR, rotation, and S-box.
  - **Round Steps**:
  1. **SubBytes**: Non-linear S-box (e.g., $\text{SubByte}(0x53) = 0xED$).
  2. **ShiftRows**: Cyclic shifts (Row 0: 0, Row 1: 1, Row 2: 2, Row 3: 3).
  3. **MixColumns**: Matrix multiplication in GF($2^8$):
     $$
     \begin{bmatrix}
     02 & 03 & 01 & 01 \\
     01 & 02 & 03 & 01 \\
     01 & 01 & 02 & 03 \\
     03 & 01 & 01 & 02
     \end{bmatrix}
     $$

4. **AddRoundKey**: XOR with round key.

- **Example**:

  - _Alice_ encrypts "CryptoIsFun" (128-bit block) with AES-256.
  - **Key**: 256-bit randomly generated.
  - _Trudy_ attempts side-channel attacks but fails due to masking.

  **Video for more understanding:** [Link](https://www.youtube.com/watch?v=O4xNJsjtN6E&ab_channel=Computerphile)

---

### **3. Public Key Cryptography**

#### **RSA (Rivest-Shamir-Adleman)**

- **Key Generation**:
  1. Choose primes $p = 11$, $q = 23$.
  2. Compute $n = p \times q = 253$, $\phi(n) = (p-1)(q-1) = 220$.
  3. Choose $e = 3$ (coprime to $\phi(n)$).
  4. Compute $d = e^{-1} \mod \phi(n) = 147$.
- **Encryption**: $c = m^e \mod n$.
  - _Bob_ sends $m = 100$: $c = 100^3 \mod n = 156$.
- **Decryption**: $m = c^d \mod n = 156^{147} \mod n = 100$.
- **Attack**:

  - _Trudy_ tries to factor $n = 253$ → $p = 11$, $q = 23$, but fails for large $n$ (e.g., 2048 bits).

  **Video for more understanding:** [Link](https://www.youtube.com/watch?v=JD72Ry60eP4&ab_channel=Computerphile)

---

#### **Digital Signatures (RSA-Based)**

- **Signing**:
  1. _Alice_ hashes message $M$ → $H(M) = \text{SHA-256}(M)$.
  2. Encrypts hash with private key: $\text{Signature} = H(M)^d \mod n$.
- **Verification**:
  1. _Bob_ decrypts signature with Alice’s public key: $H'(M) = \text{Signature}^e \mod n$.
  2. Compares $H'(M)$ with $\text{SHA-256}(M)$.
- **Example**:
  - _Alice_ signs "Transfer $100" → _Trudy_ can’t reuse the signature for "Transfer $1000" (hash mismatch).

---

### **4. Knapsack Cryptosystem**

#### **Merkle-Hellman (Broken)**

- **Key Generation**:
  1. **Superincreasing Sequence**: $\{2, 3, 6, 13\}$.
  2. Choose modulus $M = 20 > \sum a_i$, multiplier $W = 7$ (coprime to $M$).
  3. **Public Key**: $b_i = W \times a_i \mod M \to \{14, 1, 2, 11\}$.
- **Encryption**:
  - _Bob_ encrypts bits $1101$ → $S = 14 + 1 + 11 = 26$.
- **Decryption**:
  1. Compute $S' = W^{-1} \times S \mod M = 3 \times 26 \mod M = 18$.
  2. Solve superincreasing knapsack: $13 + 6 - 1 = 18$.
- **Shamir’s Lattice Attack**:
  - _Trudy_ constructs a lattice from public key $\{14, 1, 2, 11\}$.
  - Uses **LLL algorithm** to find short vectors, recovering $W = 7$, $M = 20$.

---

### **5. Real-World Examples**

1. **A5/1 in GSM**:
   - _Alice_ calls _Bob_. _Trudy_ intercepts traffic but fails to decrypt due to A5/3.
2. **RC4 in WEP**:
   - _Trudy_ cracks _Alice_’s Wi-Fi by capturing 40,000 IVs (FMS attack).
3. **AES in TLS**:
   - _Alice_ visits "https://bank.com". AES-256 encrypts her session.
4. **RSA in SSH**:
   - _Bob_ logs into a server using RSA-2048. _Trudy_ cannot factor $n$.

---

### **6. Mathematical Appendix**

#### **Galois Field GF($2^8$)**

- **Addition**: XOR (e.g., $0x57 + 0x83 = 0xD4$).
- **Multiplication**: Polynomial multiplication modulo $x^8 + x^4 + x^3 + x + 1$.
  - Example: $0x57 \times 0x83$:
    - $(x^6 + x^4 + x^2 + x + 1)(x^7 + x + 1) \mod \text{irreducible}$.

#### **LLL Algorithm (Lattice Reduction)**

- **Goal**: Find short, nearly orthogonal vectors in a lattice.
- **Knapsack Attack**: Reduces breaking Merkle-Hellman to polynomial time.

### **5. RSA Cryptosystem: In-Depth Explanation**

#### **1. The Factoring Problem**

**Concept**:  
RSA's security relies on the **factoring problem**: factoring a large composite number $n$ into its prime factors $p$ and $q$ is computationally intractable. While multiplying $p$ and $q$ is easy, reversing the process (factoring $n$) is exponentially harder as $n$ grows.

**Why Factoring is Hard**:

- **Best Algorithms**: The fastest known classical algorithm, the **General Number Field Sieve (GNFS)**, has sub-exponential complexity:  
  \[
  \mathcal{O}\left(\exp\left(\left(\sqrt[3]{\frac{64}{9}} + o(1)\right) (\ln n)^{1/3} (\ln \ln n)^{2/3}\right)\right)
  \]
  For a 2048-bit $n$, this requires millions of years on classical computers.
- **Quantum Threat**: Shor’s algorithm (quantum) factors $n$ in polynomial time, but large-scale quantum computers don’t yet exist.

**Example**:

- Let $n = 3233$. Factoring it requires testing divisors until finding $p = 61$ and $q = 53$. For large $n$ (e.g., 617 digits), this is infeasible.

---

#### **2. Modular Exponentiation in RSA**

**Key Generation**:

1. Choose primes $p = 61$, $q = 53$.
2. Compute $n = p \times q = 3233$ and $\phi(n) = (p-1)(q-1) = 3120$.
3. Choose $e = 17$ (public exponent) such that $\gcd(e, \phi(n)) = 1$.
4. Compute $d = e^{-1} \mod \phi(n) = 2753$ (private exponent).

**Encryption & Decryption**:

- **Encrypt** plaintext $m$ (e.g., $m = 65$):
  $$
  c = m^e \mod n = 65^{17} \mod 3233 = 2790
  $$
- **Decrypt** ciphertext $c$:
  $$
  m = c^d \mod n = 2790^{2753} \mod 3233 = 65
  $$

**Mathematical Foundation**:

- **Euler’s Theorem**: If $\gcd(m, n) = 1$, $m^{\phi(n)} \equiv 1 \mod n$.
- **Decryption Works Because**:
  $$
  c^d \mod n = (m^e)^d \mod n = m^{ed} \mod n = m^{1 + k\phi(n)} \mod n = m \mod n
  $$
  (since $ed \equiv 1 \mod \phi(n)$).

---

#### **3. Repeated Squaring for Efficient Exponentiation**

**Problem**: Directly computing $m^e \mod n$ for large $e$ (e.g., $2^{1024}$) is computationally infeasible.

**Solution**: **Repeated squaring** reduces complexity from $\mathcal{O}(e)$ to $\mathcal{O}(\log e)$.

**Algorithm**:

1. Convert $e$ to binary (e.g., $17 = 10001_2$).
2. Compute powers of $m$ modulo $n$ using squaring:
   $$
   m^{2^k} \mod n = \left(m^{2^{k-1}}\right)^2 \mod n
   $$
3. Multiply relevant powers based on binary representation.

**Example**: Compute $65^{17} \mod 3233$:

1. $17 = 16 + 1 = 2^4 + 2^0$.
2. Compute powers:
   - $65^1 \mod 3233 = 65$
   - $65^2 \mod 3233 = 4225 \mod 3233 = 992$
   - $65^4 = (65^2)^2 \mod 3233 = 992^2 \mod 3233 = 2816$
   - $65^8 = 2816^2 \mod 3233 = 256$
   - $65^{16} = 256^2 \mod 3233 = 633$
3. Combine results:
   $$
   65^{17} \mod 3233 = (65^{16} \times 65^1) \mod 3233 = (633 \times 65) \mod 3233 = 2790
   $$

**Why It Works**:

- Binary decomposition minimizes multiplications (e.g., 17 requires 5 steps instead of 16).
- Each step uses $\mod n$ to keep numbers small.

---

#### **4. Full Example: RSA Workflow**

**Key Setup**:

- $p = 61$, $q = 53$, $n = 3233$, $\phi(n) = 3120$, $e = 17$, $d = 2753$.

**Encryption**:

- $m = 65$:
  $$
  c = 65^{17} \mod 3233 = 2790 \quad (\text{using repeated squaring})
  $$

**Decryption**:

- $c = 2790$:
  $$
  m = 2790^{2753} \mod 3233 = 65 \quad (\text{repeated squaring with binary decomposition of 2753})
  $$

---

#### **5. Security Implications**

- **Factoring $n$ Breaks RSA**: If Trudy factors $n = 3233$ into $61 \times 53$, she computes $\phi(n) = 3120$ and $d = 17^{-1} \mod 3120 = 2753$, decrypting any message.
- **Key Size**: Modern RSA uses $n$ with 2048–4096 bits. Factoring a 2048-bit $n$ is currently infeasible.

---

### **6. Hash Functions: Qualities of a Good Hash Function**

A hash function takes an input (message) of arbitrary length and produces a fixed-size output (hash/digest). A good hash function must satisfy these **five properties**:

---

#### **1. Preimage Resistance**

- **Definition**: Given a hash value \( H \), it should be computationally infeasible to find any input \( m \) such that \( H(m) = H \).
- **Example**:
  - If \( H(\text{"password123"}) = \text{abcd...} \), even if you know \( \text{abcd...} \), you can’t reverse-engineer the original input "password123".
- **Math**:
  - Hash functions are **one-way** due to non-linear operations (e.g., modular reductions, bitwise XOR).

---

#### **2. Second Preimage Resistance**

- **Definition**: Given an input \( m \), it’s hard to find another input \( m' \neq m \) such that \( H(m) = H(m') \).
- **Example**:
  - If \( H(\text{"Hello"}) = \text{xyz} \), you can’t find a different message "H3llo" that also hashes to \( \text{xyz} \).

---

#### **3. Collision Resistance**

- **Definition**: It’s hard to find any two distinct inputs \( m \) and \( m' \) where \( H(m) = H(m') \).
- **Example**:
  - Finding two different PDF files with the same SHA-256 hash is nearly impossible.

---

#### **4. Deterministic**

- The same input always produces the same hash.
- **Example**:
  - \( H(\text{"Alice"}) = \text{abc} \) today, and \( H(\text{"Alice"}) = \text{abc} \) tomorrow.

---

#### **5. Avalanche Effect**

- **Definition**: A small change in the input (e.g., flipping one bit) should drastically change the output (~50% of bits flipped).
- **Example**:
  - \( H(\text{"cat"}) = \text{1A3F...} \)
  - \( H(\text{"Cat"}) = \text{9B0E...} \) (capital "C" changes all bits).

---

### **7. The Birthday Problem**

**Question**: How many people are needed in a room for a 50% chance that two share a birthday?  
**Answer**: 23 people.

---

#### **Math Behind the Birthday Problem**

- Let \( P(n) \) = probability of **no collision** among \( k \) people.  
  \[
  P(n) = \frac{365}{365} \times \frac{364}{365} \times \cdots \times \frac{365 - k + 1}{365}
  \]
- Probability of **at least one collision**:  
  \[
  1 - P(n) \approx 1 - e^{-k^2 / (2 \times 365)}
  \]
- Solving for \( 1 - P(n) = 0.5 \):  
  \[
  k \approx \sqrt{2 \times 365 \times \ln 2} \approx 23
  \]

---

#### **Implications for Hash Functions**

- For a hash with \( N \)-bit output (\( 2^N \) possible hashes), collisions become likely after \( \sqrt{2^N} = 2^{N/2} \) trials.
- **Example**:
  - A 128-bit hash (e.g., MD5) has \( 2^{128} \) possible hashes. Collisions are expected after \( 2^{64} \) hashes.
  - This is why MD5 is broken (collisions found in \( 2^{24} \) steps).

---

### **8. Tiger Hash**

#### **Overview**

- Designed in 1995 as a fast, secure 192-bit hash for 64-bit CPUs.
- **Key Features**:
  - 512-bit input blocks.
  - 192-bit output (3×64 bits for 64-bit CPU efficiency).
  - 24 rounds with 4 S-boxes.

---

#### **Structure of Tiger Hash**

1. **Padding**:

   - Input is padded to a multiple of 512 bits.
   - Example: A 1000-bit message is padded with 1, followed by 407 zeros, and a 64-bit length field.

2. **Processing Blocks**:

   - Split padded message into 512-bit blocks.
   - Each block undergoes **24 rounds** of mixing.

3. **Avalanche Effect in Action**:
   - Each round uses non-linear S-boxes, modular additions, and XORs to ensure small changes propagate.

---

#### **Key Schedule Algorithm**

- **Purpose**: Expand the 512-bit block into 192 bits for each round.
- **Steps**:
  1. Split the 512-bit block into eight 64-bit words \( w_0, w_1, ..., w_7 \).
  2. Compute new words using XOR, addition, and S-boxes:  
     \[
     w*j = w*{j-1} \oplus (w*{j-2} + w*{j-3} + \text{S-box}(w\_{j-7}))
     \]
- **Example**:
  - Let \( w_0 = 0x1234 \), \( w_1 = 0x5678 \), ..., \( w_7 = 0xABCD \).
  - \( w_8 = w_7 \oplus (w_6 + w_5 + \text{S-box}(w_1)) \).

---

#### **S-Boxes**

- Tiger uses 4 S-boxes, each mapping 8 bits → 64 bits.
- **Role**: Introduce non-linearity to prevent reverse-engineering.

---

### **9. HMAC (Hashed Message Authentication Code)**

#### **Problem**

If Trudy alters both the message \( m \) and its hash \( H(m) \), Bob can’t detect tampering.

---

#### **Solution: HMAC**

- Uses a **secret key \( K \)** to "lock" the hash.
- **Steps**:
  1. **Inner Hash**: Compute \( H(\text{key} \oplus \text{ipad} \parallel \text{message}) \).
  2. **Outer Hash**: Compute \( H(\text{key} \oplus \text{opad} \parallel \text{inner hash}) \).

---

#### **HMAC Formula**

\[
\text{HMAC}(K, m) = H\left( (K \oplus \text{opad}) \parallel H\left( (K \oplus \text{ipad}) \parallel m \right) \right)
\]

- **Constants**:
  - \( \text{ipad} = 0x36 \) (repeated), \( \text{opad} = 0x5C \) (repeated).

---

#### **Example**

- **Key \( K \)**: "secret" (padded to block size).
- **Message \( m \)**: "Hello".
- **HMAC-SHA256 Computation**:
  1. Inner hash: \( \text{SHA256}(K \oplus \text{ipad} \parallel \text{"Hello"}) \).
  2. Outer hash: \( \text{SHA256}(K \oplus \text{opad} \parallel \text{Inner hash}) \).

---

### **Math Topics Needed to Master This**

1. **Probability**:
   - Birthday problem, collision probabilities.
2. **Modular Arithmetic**:
   - Used in hash functions (e.g., SHA-256, Tiger).
3. **Combinatorics**:
   - Counting hash collisions.
4. **Boolean Algebra**:
   - Bitwise operations (XOR, AND, OR) in hash functions.
5. **Information Theory**:
   - Entropy, avalanche effect.
6. **Cryptographic Protocols**:
   - HMAC structure, key scheduling.

