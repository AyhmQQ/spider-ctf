import sys
import os

# إضافة المسار لضمان العثور على الموديولات عند الاستيراد
sys.path.append(os.getcwd())

from ingest.ingestor import Ingestor
from extractors.base import Extractor
from aggregation.aggregator import Aggregator
from analyzers.engine import Analyzer
from models.challenge import CryptoChallenge

class SpiderEngine:
    def __init__(self, flag_format=r"flag\{.*?\}"):
        self.ingestor = Ingestor()
        self.extractor = Extractor()
        self.aggregator = Aggregator()
        self.analyzer = Analyzer(flag_format=flag_format)

    def run_full_analysis(self, paths):
        # 1. استلام الملفات وتصنيفها
        files = self.ingestor.ingest(paths)
        
        # 2. استخراج البيانات من كل ملف وتجميعها
        extracted_list = []
        for f in files:
            res = self.extractor.extract(f)
            extracted_list.append({
                'filepath': f['filepath'], 
                'extracted': res
            })
        
        # 3. تجميع البيانات المستخرجة (Variables, Patterns)
        aggregated = self.aggregator.aggregate(extracted_list)
        
        # 4. تحليل البيانات المجمعة والبحث عن الـ Flags
        all_contents = [f['content'] for f in files]
        findings, flags = self.analyzer.analyze(aggregated, raw_contents=all_contents)
        
        # 5. بناء نموذج التحدي النهائي للتقرير
        challenge = CryptoChallenge(name="CTF Challenge Analysis")
        challenge.variables = aggregated['variables']
        challenge.flag_candidates = flags
        
        if findings:
            # نأخذ أول نتيجة مكتشفة كنوع أساسي (مثل RSA)
            challenge.detected_type = findings[0]['type']
            challenge.confidence = findings[0]['confidence']
            
            # دمج كل التفاصيل والاقتراحات
            all_details = []
            for f in findings:
                all_details.append(f['details'])
                if 'suggestions' in f:
                    challenge.suggestions.extend(f['suggestions'])
            
            challenge.details = "\n".join(all_details)
            # إزالة التكرار من الاقتراحات
            challenge.suggestions = list(set(challenge.suggestions))
            
        return challenge
