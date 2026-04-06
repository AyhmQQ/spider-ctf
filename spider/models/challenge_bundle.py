from dataclasses import dataclass, field
from .input_file import InputFile


@dataclass
class ChallengeBundle:
    files: list[InputFile] = field(default_factory=list)

    def add_file(self, file: InputFile) -> None:
        self.files.append(file)

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_size_bytes(self) -> int:
        return sum(file.size_bytes for file in self.files)