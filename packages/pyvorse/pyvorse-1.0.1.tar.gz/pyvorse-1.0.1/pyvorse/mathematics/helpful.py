__all__ = ["trin", "hexcount"]

def trin(c: int) -> int:
    "returns triangular number of an number"
    return int((c * (c + 1)) / 2)


def hexcount(c: int) -> int:
    "returns count of hexagonal cells by radius, c = 1 means single cell"
    return int(6 * (trin(c) - c) + 1)
