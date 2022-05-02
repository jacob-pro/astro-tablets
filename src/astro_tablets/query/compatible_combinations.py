from typing import Generic, List, TypeVar


class CanBeFollowedBy:
    def can_be_followed_by(self, potential2) -> bool:
        pass


P = TypeVar("P", bound=CanBeFollowedBy)


class Result(Generic[P]):
    potentials: List[P]


R = TypeVar("R", bound=Result)


def generate_compatible_combinations(
    yrs: List[R],
) -> List[List[P]]:
    paths: List[List[P]] = []
    for idx, y in enumerate(yrs):
        if idx == 0:
            for potential in y.potentials:
                paths.append([potential])
        else:
            new_paths = []
            for path in paths:
                for potential in y.potentials:
                    path_tail = path[len(path) - 1]
                    if path_tail.can_be_followed_by(potential):
                        new_path = path.copy()
                        new_path.append(potential)
                        new_paths.append(new_path)
            paths = new_paths
    return paths
