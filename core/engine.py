from spider.ingest.ingestor import Ingestor
from spider.extractors.base import Extractor
from spider.aggregation.aggregator import Aggregator
from spider.analyzers.engine import Analyzer
from spider.models.challenge import CryptoChallenge

class SpiderEngine:
    def __init__(self, flag_format=r"flag\{.*?\}"):
        self.ingestor = Ingestor()
        self.extractor = Extractor()
        self.aggregator = Aggregator()
        self.analyzer = Analyzer(flag_format=flag_format)

    def run_full_analysis(self, paths):
        # 1. Ingest
        files = self.ingestor.ingest(paths)
        
        # 2. Extract & Aggregate
        extracted_list = []
        for f in files:
            res = self.extractor.extract(f)
            extracted_list.append({'filepath': f['filepath'], 'extracted': res})
        
        aggregated = self.aggregator.aggregate(extracted_list)
        
        # 3. Analyze
        all_contents = [f['content'] for f in files]
        findings, flags = self.analyzer.analyze(aggregated, raw_contents=all_contents)
        
        # 4. Create Challenge Model
        challenge = CryptoChallenge(name="CTF Challenge")
        challenge.variables = aggregated['variables']
        challenge.flag_candidates = flags
        
        if findings:
            challenge.detected_type = findings[0]['type']
            challenge.confidence = findings[0]['confidence']
            challenge.suggestions = findings[0]['suggestions']
            
        return challenge
