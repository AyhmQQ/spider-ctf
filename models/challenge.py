class CryptoChallenge:
    def __init__(self, name="Unknown"):
        self.name = name
        self.files = []
        self.variables = {}  # لتخزين n, e, c وغيرها
        self.patterns = {"hex": [], "base64": []}
        self.detected_type = None
        self.confidence = "Low"
        self.suggestions = []
        self.flag_candidates = []

    def add_file(self, filepath, file_type):
        self.files.append({"path": filepath, "type": file_type})
