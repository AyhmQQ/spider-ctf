import decimal

def low_exponent_attack(c, e):
    """
    يقوم بفك التشفير عندما يكون الأس صغيراً جداً (e=3) 
    عن طريق حساب الجذر النوني للـ ciphertext.
    هذا الهجوم ينجح إذا كان m^e < n.
    """
    try:
        # إعداد الدقة للحسابات الكبيرة جداً
        decimal.getcontext().prec = 2048 
        
        # تحويل القيم إلى Decimal للتعامل مع الجذور بدقة
        c_dec = decimal.Decimal(int(c))
        e_dec = decimal.Decimal(int(e))
        
        # حساب الجذر (الجذر التكعيبي إذا كان e=3)
        # الصيغة: m = c ^ (1/e)
        root = c_dec ** (decimal.Decimal(1) / e_dec)
        
        # تحويل النتيجة إلى عدد صحيح
        m = int(round(root))
        
        # التحقق من صحة النتيجة (m^e يجب أن يساوي c)
        if pow(m, int(e)) != int(c):
            # إذا لم يتساويا، فهذا يعني أن m^e تجاوز n والهجوم لا يصلح هنا
            return None

        # تحويل الرقم المستخرج إلى نص مقروء
        # نحول الرقم إلى Hex ثم إلى Bytes ثم إلى UTF-8
        hex_val = hex(m)[2:]
        if len(hex_val) % 2 != 0:
            hex_val = '0' + hex_val
            
        decrypted = bytes.fromhex(hex_val).decode('utf-8', errors='ignore')
        return decrypted
        
    except Exception as e:
        # في حال حدوث أي خطأ حسابي
        return None
