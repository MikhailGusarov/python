class ContFromBy:
    def __init__(self,val: int = 0,incr: int = 1) -> None:
        self.val = val
        self.incr = incr
    def __repr__(self) -> str:
        return str(self.val)
    def increase(self) -> None:
        self.val += self.incr
