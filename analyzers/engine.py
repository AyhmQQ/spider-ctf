import re
# السطر التالي هو الأهم: تأكد أنه لا يبدأ بكلمة spider.
from crypto.rsa.attacks import low_exponent_attack

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
                # تنظيف الصيغة من أي هروب زائد قد يسبب مشاكل في ويندوز
                clean_format = self.flag_format.replace(r'\\', '\\')
                flag_regex = re.compile(clean_format)
                for content in raw_contents:
                    matches = flag_regex.findall(content)
                    candidates.extend(matches)
            except Exception as e:
                # إذا فشل الريجيكس، نحاول البحث عن كلمة flag العادية
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
                
                # هجوم الأس الصغير (Low Exponent Attack)
                if vars['e'] == 3:
                    rsa_finding['suggestions'].append("Try Cube Root attack (Low Exponent).")
                    
                    # محاولة فك التشفير تلقائياً باستخدام الوحدة التي استوردناها
                    try:
                        decrypted_msg = low_exponent_attack(vars['c'], vars['e'])
                        if decrypted_msg:
                            rsa_finding['details'] += f"\n    [!] AUTO-SOLVE SUCCESS: {decrypted_msg}"
                            candidates.append(f"Decrypted: {decrypted_msg}")
                    except Exception:
                        pass

            findings.append(rsa_finding)

        return findings, list(set(candidates))
