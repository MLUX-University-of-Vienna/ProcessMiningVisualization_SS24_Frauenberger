from ui.heuristic_miner_ui.heuristic_miner_controller import HeuristicMinerController
from ui.fuzzy_miner_ui.fuzzy_miner_controller import FuzzyMinerController
from ui.inductive_miner_ui.inductive_miner_controller import InductiveMinerController


# ALGORITHM CONFIGURATIONS
# ------------------------

# Maps the algorithm names to the route names.
algorithm_mappings = {
    "Heuristic Mining": "heuristic",
    "Fuzzy Mining": "fuzzy",
    "Inductive Mining": "inductive",
}
# Maps the algorithm routes to the paths of the documentation files.
docs_path_mappings = {
    "heuristic": "docs/algorithms/heuristic_miner.md",
    "fuzzy": "docs/algorithms/fuzzy_miner.md",
    "inductive": "docs/algorithms/inductive_miner.md",
}

# Maps the algorithm routes to the controllers.
algorithm_routes = {
    "heuristic": HeuristicMinerController,
    "fuzzy": FuzzyMinerController,
    "inductive": InductiveMinerController,
}
