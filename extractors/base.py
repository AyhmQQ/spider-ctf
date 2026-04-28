
import re

class Extractor:
    def __init__(self):
        # Patterns for common crypto variables
        self.var_patterns = {
            'n': re.compile(r'(?:n|modulus)\s*[:=]\s*([0-9a-fA-Fx]+)', re.IGNORECASE),
            'e': re.compile(r'\be\b\s*[:=]\s*([0-9a-fA-Fx]+)', re.IGNORECASE),
            'c': re.compile(r'(?:c|ct|ciphertext)\s*[:=]\s*([0-9a-fA-Fx]+)', re.IGNORECASE),
            'p': re.compile(r'p\s*[:=]\s*([0-9a-fA-Fx]+)', re.IGNORECASE),
            'q': re.compile(r'q\s*[:=]\s*([0-9a-fA-Fx]+)', re.IGNORECASE),
        }
        self.hex_pattern = re.compile(r'(?:0x)?([0-9a-fA-F]{32,})')
        self.b64_pattern = re.compile(r'(?:[A-Za-z0-9+/]{4}){10,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?')

    def parse_value(self, val_str):
        val_str = val_str.strip()
        try:
            if val_str.lower().startswith('0x'):
                return int(val_str, 16)
            return int(val_str)
        except ValueError:
            try:
                return int(val_str, 16)
            except ValueError:
                return None

    def extract(self, file_info):
        content = file_info['content']
        extracted = {
            'variables': {},
            'patterns': {
                'hex': [],
                'base64': []
            }
        }

        # Extract labeled variables
        for var, pattern in self.var_patterns.items():
            matches = pattern.findall(content)
            for m in matches:
                val = self.parse_value(m)
                if val:
                    extracted['variables'][var] = val

        # Extract hex patterns
        hex_matches = self.hex_pattern.findall(content)
        extracted['patterns']['hex'] = list(set(hex_matches))

        # Extract base64 patterns
        b64_matches = self.b64_pattern.findall(content)
        extracted['patterns']['base64'] = list(set(b64_matches))

        return extracted
