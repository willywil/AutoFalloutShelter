"""Strategy package — verified play loop for simulator; live stubs remain unsafe."""

from src.strategy.play import play_to_win, PlayResult

__all__ = ["play_to_win", "PlayResult", "ResourceManager", "DwellerManager", "IncidentHandler"]


class ResourceManager:
    def __init__(self):
        self.thresholds = {"power": 0.8, "food": 0.7, "water": 0.7}

    def should_collect(self, resource_type, current_level):
        return current_level >= self.thresholds.get(resource_type, 0.7)

    def prioritize_production(self, resources):
        return sorted(resources.items(), key=lambda kv: kv[1])


class DwellerManager:
    def __init__(self):
        self.dwellers = []

    def optimal_assignment(self, dweller, rooms):
        raise NotImplementedError("Live SPECIAL assignment not yet verified")

    def should_train(self, dweller):
        return False


class IncidentHandler:
    def detect_incident(self, game_state):
        return None

    def respond_to_incident(self, incident_type, location):
        raise NotImplementedError("Incident response not yet verified")
