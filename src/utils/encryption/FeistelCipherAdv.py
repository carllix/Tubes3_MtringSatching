class FeistelCipherAdv:
    def __init__(self, master_key: str, rounds: int = 8):
        self.rounds = rounds
        self.master_key = master_key
        self.round_keys = self.generate_round_keys(master_key, rounds)
        self.sbox = self.generate_custom_sbox()
        self.inv_sbox = self.generate_inv_sbox()
        self.pbox = self.generate_permutation_box()
        self.inv_pbox = self.generate_inv_permutation_box()
    
    def hash(self, data: str) -> int:
        hash_value = 0
        prime1 = 31
        prime2 = 37
        prime3 = 41
        
        for i, char in enumerate(data):
            char_val = ord(char)
            # Multiple mixing operations
            hash_value = (hash_value * prime1) ^ char_val
            hash_value = ((hash_value << 5) | (hash_value >> 27)) & 0xFFFFFFFF
            hash_value ^= (char_val * prime2 + i * prime3)
            hash_value = hash_value & 0xFFFFFFFF
        
        # Additional avalanche effect
        hash_value ^= hash_value >> 16
        hash_value *= 0x85EBCA6B
        hash_value = hash_value & 0xFFFFFFFF
        hash_value ^= hash_value >> 13
        hash_value *= 0xC2B2AE35
        hash_value = hash_value & 0xFFFFFFFF
        hash_value ^= hash_value >> 16
        
        return hash_value
    
    def linear_congruential_generator(self, seed: int, count: int) -> list:
        a = 1664525
        c = 1013904223
        m = 2**32
        
        values = []
        current = seed
        
        for _ in range(count):
            current = (a * current + c) % m
            values.append(current)
        
        return values
    
    def generate_round_keys(self, master_key: str, rounds: int) -> list:
        round_keys = []
        
        key_seed = self.hash(master_key)
        
        key_values = self.linear_congruential_generator(key_seed, rounds * 4)
        
        for round_num in range(rounds):
            # Ambil 4 values untuk setiap round key
            base_idx = round_num * 4
            round_seed = key_values[base_idx]
            
            # Key derivation dengan operasi bit manual
            derived_key = round_seed
            
            # Multiple transformations untuk complexity
            derived_key ^= (derived_key << 13) | (derived_key >> 19)
            derived_key = derived_key & 0xFFFFFFFF
            derived_key ^= round_num * 0x9E3779B9  # Golden ratio
            derived_key = derived_key & 0xFFFFFFFF
            derived_key ^= (derived_key << 7) | (derived_key >> 25)
            derived_key = derived_key & 0xFFFFFFFF
            
            # Convert ke 4-byte string
            key_bytes = [
                (derived_key >> 24) & 0xFF,
                (derived_key >> 16) & 0xFF,
                (derived_key >> 8) & 0xFF,
                derived_key & 0xFF
            ]
            
            round_key = ''.join(chr(b) for b in key_bytes)
            round_keys.append(round_key)
        
        return round_keys
    
    def generate_custom_sbox(self) -> list:
        # Create initial S-Box
        sbox = list(range(256))
        
        # Shuffle menggunakan master key sebagai seed
        seed = self.hash(self.master_key + "_sbox")
        
        for i in range(255, 0, -1):
            # Generate pseudo-random index menggunakan LCG
            seed = ((seed * 1103515245) + 12345) & 0xFFFFFFFF
            j = seed % (i + 1)
            
            # Swap elements
            sbox[i], sbox[j] = sbox[j], sbox[i]
        
        return sbox
    
    def generate_inv_sbox(self) -> list:
        inv_sbox = [0] * 256
        for i, val in enumerate(self.sbox):
            inv_sbox[val] = i
        return inv_sbox
    
    def generate_permutation_box(self) -> list:
        # 32-bit permutation box (untuk 4-byte block)
        pbox = list(range(32))
        
        # Shuffle bit positions menggunakan key-derived seed
        seed = self.hash(self.master_key + "_pbox")
        
        for i in range(31, 0, -1):
            seed = ((seed * 16807) + 0) & 0xFFFFFFFF
            j = seed % (i + 1)
            pbox[i], pbox[j] = pbox[j], pbox[i]
        
        return pbox
    
    def generate_inv_permutation_box(self) -> list:
        inv_pbox = [0] * 32
        for i, pos in enumerate(self.pbox):
            inv_pbox[pos] = i
        return inv_pbox
    
    def sbox_substitute(self, data: str) -> str:
        return ''.join(chr(self.sbox[ord(c)]) for c in data)
    
    def inv_sbox_substitute(self, data: str) -> str:
        return ''.join(chr(self.inv_sbox[ord(c)]) for c in data)
    
    def permute_32bit(self, value: int) -> int:
        result = 0
        for i in range(32):
            if (value >> i) & 1:
                result |= (1 << self.pbox[i])
        return result
    
    def inv_permute_32bit(self, value: int) -> int:
        result = 0
        for i in range(32):
            if (value >> i) & 1:
                result |= (1 << self.inv_pbox[i])
        return result
    
    def permute_string(self, data: str) -> str:
        result = ""
        
        # Pad ke kelipatan 4
        padded_data = data
        while len(padded_data) % 4 != 0:
            padded_data += '\0'
        
        # Process per 4-byte chunks
        for i in range(0, len(padded_data), 4):
            chunk = padded_data[i:i+4]
            
            # Convert ke 32-bit integer
            value = 0
            for j, c in enumerate(chunk):
                value |= (ord(c) << (j * 8))
            
            # Apply permutation
            permuted = self.permute_32bit(value)
            
            # Convert back ke string
            chunk_result = ""
            for j in range(4):
                chunk_result += chr((permuted >> (j * 8)) & 0xFF)
            
            result += chunk_result
        
        return result[:len(data)] 
    
    def inv_permute_string(self, data: str) -> str:
        result = ""
        
        # Pad ke kelipatan 4
        padded_data = data
        while len(padded_data) % 4 != 0:
            padded_data += '\0'
        
        for i in range(0, len(padded_data), 4):
            chunk = padded_data[i:i+4]
            
            # Convert ke 32-bit integer
            value = 0
            for j, c in enumerate(chunk):
                value |= (ord(c) << (j * 8))
            
            # Apply inverse permutation
            unpermuted = self.inv_permute_32bit(value)
            
            # Convert back ke string
            chunk_result = ""
            for j in range(4):
                chunk_result += chr((unpermuted >> (j * 8)) & 0xFF)
            
            result += chunk_result
        
        return result[:len(data)] 
    
    def advanced_nonlinear_transform(self, data: str, round_num: int) -> str:
        result = ""
        
        for i, c in enumerate(data):
            byte_val = ord(c)
            
            # Multiple non-linear operations
            # Operation 1: Galois Field multiplication-like
            temp = byte_val
            temp = ((temp << 1) ^ (0x1B if temp & 0x80 else 0)) & 0xFF
            
            # Operation 2: Non-linear feedback
            temp ^= ((temp << 2) ^ (temp >> 6)) & 0xFF
            
            # Operation 3: Position and round dependent mixing
            temp ^= (i * round_num) & 0xFF
            
            # Operation 4: Polynomial operation
            temp = (temp * 3 + 7) & 0xFF
            
            # Operation 5: Bit reversal pattern
            reversed_bits = 0
            for bit in range(8):
                if temp & (1 << bit):
                    reversed_bits |= (1 << (7 - bit))
            
            temp = reversed_bits ^ byte_val
            
            result += chr(temp & 0xFF)
        
        return result
    
    def F(self, r: str, round_key: str, round_num: int) -> str:
        temp = r
        
        # Layer 1: Key mixing dengan complex operation
        temp_result = ""
        for i, c in enumerate(temp):
            key_char = round_key[i % len(round_key)]
            mixed = (ord(c) ^ ord(key_char) ^ round_num ^ (i * 7)) & 0xFF
            temp_result += chr(mixed)
        temp = temp_result
        
        # Layer 2: S-Box substitution (non-linear)
        temp = self.sbox_substitute(temp)
        
        # Layer 3: Advanced permutation
        temp = self.permute_string(temp)
        
        # Layer 4: Non-linear transformation
        temp = self.advanced_nonlinear_transform(temp, round_num)
        
        # Layer 5: Additional S-Box pass
        temp = self.sbox_substitute(temp)
        
        # Layer 6: Cross-byte mixing
        if len(temp) > 1:
            mixed_result = ""
            for i, c in enumerate(temp):
                next_char = temp[(i + 1) % len(temp)]
                prev_char = temp[(i - 1) % len(temp)]
                
                mixed = (ord(c) ^ ord(next_char) ^ ord(prev_char)) & 0xFF
                mixed_result += chr(mixed)
            temp = mixed_result
        
        # Layer 7: Final avalanche operation
        avalanche_result = ""
        checksum = sum(ord(c) for c in temp) & 0xFF
        for i, c in enumerate(temp):
            avalanched = (ord(c) ^ checksum ^ (i * round_num)) & 0xFF
            avalanche_result += chr(avalanched)
        temp = avalanche_result
        
        return temp
    
    def encrypt(self, plaintext: str) -> str:
        if not plaintext:
            return ""
        
        # Padding ke kelipatan 8
        while len(plaintext) % 8 != 0:
            plaintext += '\0'
        
        ciphertext = ''
        
        # Process each 8-byte block
        for i in range(0, len(plaintext), 8):
            block = plaintext[i:i+8]
            l, r = block[:4], block[4:]
            
            # Feistel rounds dengan enhanced F-function
            for round_num in range(self.rounds):
                new_l = r
                f_out = self.F(r, self.round_keys[round_num], round_num)
                
                # XOR left dengan F output
                new_r = ""
                for j in range(len(l)):
                    xor_result = ord(l[j]) ^ ord(f_out[j])
                    new_r += chr(xor_result)
                
                l, r = new_l, new_r
            
            # Final block (L||R)
            ciphertext += l + r
        
        return ciphertext
    
    def decrypt(self, ciphertext: str) -> str:
        if not ciphertext:
            return ""
        
        plaintext = ''
        
        # Process each 8-byte block
        for i in range(0, len(ciphertext), 8):
            block = ciphertext[i:i+8]
            l, r = block[:4], block[4:]
            
            # Reverse Feistel rounds
            for round_num in reversed(range(self.rounds)):
                new_r = l
                f_out = self.F(new_r, self.round_keys[round_num], round_num)
                
                # XOR right dengan F output
                new_l = ""
                for j in range(len(r)):
                    xor_result = ord(r[j]) ^ ord(f_out[j])
                    new_l += chr(xor_result)
                
                l, r = new_l, new_r
            
            plaintext += l + r
        
        # Remove padding
        return plaintext.rstrip('\0')