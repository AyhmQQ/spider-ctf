import base64
import string

class ClassicalSolvers:
    @staticmethod
    def solve_base64(data):
        try:
            missing_padding = len(data) % 4
            if missing_padding: data += '=' * (4 - missing_padding)
            decoded = base64.b64decode(data).decode('utf-8', errors='ignore')
            # نرجع النتيجة فقط إذا كانت تحتوي على أحرف مقروءة
            if any(c in string.printable for c in decoded):
                return decoded
        except: return None

    @staticmethod
    def solve_caesar(ciphertext, flag_format="flag"):
        results = []
        for shift in range(1, 26):
            shifted = ""
            for char in ciphertext:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    shifted += chr((ord(char) - base - shift) % 26 + base)
                else:
                    shifted += char
            # إذا وجدنا صيغة العلم نضعها في البداية، وإلا نحفظ كل الاحتمالات
            if flag_format.lower() in shifted.lower():
                results.insert(0, {"shift": shift, "text": shifted, "found": True})
            else:
                results.append({"shift": shift, "text": shifted, "found": False})
        return results

    @staticmethod
    def solve_vigenere(ciphertext, key):
        """فك تشفير Vigenere مع تجربة الاتجاهين لضمان النجاح"""
        if not key: return None
        
        def vigenere_logic(text, k, mode='decrypt'):
            res = ""
            k = k.lower()
            k_idx = 0
            for char in text:
                if char.isalpha():
                    base = ord('a') if char.islower() else ord('A')
                    shift = ord(k[k_idx % len(k)]) - ord('a')
                    if mode == 'decrypt':
                        res += chr((ord(char) - base - shift) % 26 + base)
                    else:
                        res += chr((ord(char) - base + shift) % 26 + base)
                    k_idx += 1
                else:
                    res += char
            return res

        # نجرب فك التشفير والتشفير (لأن بعض التحديات تعكس العملية)
        dec = vigenere_logic(ciphertext, key, 'decrypt')
        enc = vigenere_logic(ciphertext, key, 'encrypt')
        return {"decrypted": dec, "encrypted": enc}

    @staticmethod
    def solve_atbash(ciphertext):
        res = ""
        for char in ciphertext:
            if char.isalpha():
                base = ord('a') if char.islower() else ord('A')
                res += chr(base + (25 - (ord(char) - base)))
            else:
                res += char
        return res

    @staticmethod
    def solve_xor(ciphertext, key):
        try:
            if isinstance(key, str): key = key.encode()
            try: data_bytes = bytes.fromhex(ciphertext)
            except: data_bytes = ciphertext.encode()
            decrypted = bytes([b ^ key[i % len(key)] for i, b in enumerate(data_bytes)])
            return decrypted.decode('utf-8', errors='ignore')
        except: return None
