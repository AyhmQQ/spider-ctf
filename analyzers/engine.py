import re

class Analyzer:
    def __init__(self, flag_format=r"flag\{.*?\}"):
        self.flag_format = flag_format

    def set_flag_format(self, fmt):
        self.flag_format = fmt

    def analyze(self, aggregated_data, raw_contents=None):
        findings = []
        candidates = []
        
        # Flag Detection
        if raw_contents:
            try:
                flag_regex = re.compile(self.flag_format)
                for content in raw_contents:
                    matches = flag_regex.findall(content)
                    candidates.extend(matches)
            except Exception as e:
                print(f"Error in flag regex: {e}")

        vars = aggregated_data['variables']
        
        # RSA Detection
        if 'n' in vars and 'e' in vars:
            rsa_finding = {
                'type': 'RSA',
                'confidence': 'High',
                'details': 'Found modulus (n) and exponent (e).',
                'suggestions': []
            }
            if vars['e'] == 3 or vars['e'] == 65537:
                rsa_finding['details'] += f" Standard exponent e={vars['e']} detected."
            
            if 'c' in vars:
                rsa_finding['details'] += " Ciphertext (c) also found."
                if vars['e'] == 3:
                    rsa_finding['suggestions'].append("Try Cube Root attack (Low Exponent).")
            
            findings.append(rsa_finding)

        # XOR/Encoding detection could be added here
        
        return findings, list(set(candidates))
