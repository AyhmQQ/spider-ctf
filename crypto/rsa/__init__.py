import decimal

def low_exponent_attack(c, e):
    """
    يقوم بفك التشفير عندما يكون الأس صغيراً جداً (e=3) 
    عن طريق حساب الجذر النوني للـ ciphertext.
    """
    decimal.getcontext().prec = 1024  # دقة عالية للحسابات الكبيرة
    c_dec = decimal.Decimal(c)
    e_dec = decimal.Decimal(e)
    
    # حساب الجذر (مثلاً الجذر التكعيبي إذا كان e=3)
    root = c_dec ** (decimal.Decimal(1) / e_dec)
    
    # تحويل النتيجة إلى نص مقروء
    try:
        m = int(round(root))
        # تحويل الرقم إلى bytes ثم إلى نص
        decrypted = bytes.fromhex(hex(m)[2:]).decode('utf-8', errors='ignore')
        return decrypted
    except Exception:
        return None
