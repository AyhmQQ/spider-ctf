class Aggregator:
    def __init__(self):
        self.data = {
            'variables': {},
            'patterns': {
                'hex': set(),
                'base64': set()
            },
            'sources': {}
        }

    def aggregate(self, extracted_list):
        for entry in extracted_list:
            filepath = entry['filepath']
            extracted = entry['extracted']

            # تجميع المتغيرات (n, e, c, etc)
            for var, val in extracted['variables'].items():
                if var not in self.data['variables']:
                    self.data['variables'][var] = val
                    self.data['sources'][var] = filepath
                elif self.data['variables'][var] != val:
                    # في حال وجود تعارض، يمكن إضافة منطق للتعامل معه هنا
                    pass

            # تجميع الأنماط (Hex, Base64)
            for h in extracted['patterns']['hex']:
                self.data['patterns']['hex'].add(h)
            for b in extracted['patterns']['base64']:
                self.data['patterns']['base64'].add(b)
        
        return self.data
