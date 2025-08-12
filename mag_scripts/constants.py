import os
# Global registries for triggers and module statuses
TRIGGER_REGISTRY = {}
MODULE_STATUS_REGISTRY = {}
MODULE_STATUS_FILE = os.path.join(os.path.dirname(__file__), 'Submods', 'Monika-Afterworld-Gateway', 'module_status.pkl')