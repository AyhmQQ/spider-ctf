import re
from crypto.rsa.attacks import low_exponent_attack
from crypto.classical.solvers import ClassicalSolvers

class Analyzer:
    def __init__(self, flag_format=r"flag\{.*?\}"):
        self.flag_format = flag_format

    def set_flag_format(self, fmt):
        self.flag_format = fmt

    def analyze(self, aggregated_data, raw_contents=None):
        findings = []
        candidates = []
        
        # 1. البحث عن الـ Flag بالصيغة المحددة في النصوص الخام
        if raw_contents:
            try:
                clean_format = self.flag_format.replace(r'\\', '\\')
                flag_regex = re.compile(clean_format)
                for content in raw_contents:
                    # أ. البحث المباشر
                    matches = flag_regex.findall(content)
                    candidates.extend(matches)
                    
                    # ب. محاولة فك Base64 تلقائياً إذا وجدنا نصاً مشتبهاً به
                    b64_matches = re.findall(r'[A-Za-z0-9+/]{10,}=*', content)
                    for b64 in b64_matches:
                        decoded = ClassicalSolvers.solve_base64(b64)
                        if decoded and any(f in decoded.lower() for f in ['flag', '{', 'ctf']):
                            candidates.append(f"Base64_Decoded: {decoded}")
            except Exception:
                pass

        vars = aggregated_data['variables']
        
        # 2. تحليل تحديات RSA
        if 'n' in vars and 'e' in vars:
            rsa_finding = {
                'type': 'RSA',
                'confidence': 'High',
                'details': f"Found modulus (n) and exponent (e={vars['e']}).",
                'suggestions': []
            }
            
            if 'c' in vars:
                rsa_finding['details'] += " Ciphertext (c) also found."
                if vars['e'] == 3:
                    rsa_finding['suggestions'].append("Try Cube Root attack (Low Exponent).")
                    try:
                        decrypted_msg = low_exponent_attack(vars['c'], vars['e'])
                        if decrypted_msg:
                            rsa_finding['details'] += f"\n    [!] AUTO-SOLVE SUCCESS: {decrypted_msg}"
                            candidates.append(f"Decrypted_RSA: {decrypted_msg}")
                    except Exception: pass
            findings.append(rsa_finding)

        return findings, list(set(candidates))
