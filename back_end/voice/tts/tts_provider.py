from abc import ABC, abstractmethod

class TTSProvider(ABC):
    @abstractmethod
    def synthesize(self, text: str) -> bytes:
        """Return path to generated wav file"""
        pass