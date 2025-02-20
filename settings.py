class SafeLightSettings:
    exposure: float
    threshold: float
    blurRadius: float
    strength: float
    
    def __init__(self):
        self.exposure = 1.0
        self.threshold = 0.5
        self.blurRadius = 1.0
        self.strength = 1.0