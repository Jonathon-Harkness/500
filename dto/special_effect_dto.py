
class SpecialEffectDto:

    def __init__(self, name: str, description: str, points_required: int):
        self.name = name
        self.description = description
        self.points_required = bool(points_required)

