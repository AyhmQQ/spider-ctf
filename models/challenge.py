class CryptoChallenge:
    def __init__(self, name="Unknown"):
        self.name = name
        self.files = []
        self.variables = {}
        self.patterns = {"hex": [], "base64": []}
        self.detected_type = None
        self.confidence = "Low"
        self.details = ""
        self.suggestions = []
        self.flag_candidates = []

    def add_file(self, filepath, file_type):
        self.files.append({"path": filepath, "type": file_type})
