from node import Node


class Clock:
    # The CLOCK (second-chance) replacement policy.
    #
    # Frames are kept in a list. A "clock hand" sweeps the list: a frame whose
    # reference bit is set gets a second chance (bit cleared, hand advances); the
    # first frame found with an unset reference bit is the victim. Its position
    # in the list is returned so the caller can evict it.
    def __init__(self, maxSize) -> None:
        self.clockHand: int = 0
        self.maxSize = maxSize

    def findVictim(self, framePool: list[Node]) -> int:
        size = len(framePool)
        assert size > 0, "cannot evict from an empty frame pool"

        while True:
            self.clockHand %= size
            node = framePool[self.clockHand]
            if node.referenceBit:
                # second chance: clear the bit and move on
                node.referenceBit = False
                self.clockHand += 1
            else:
                # victim found; leave the hand here so that after this frame is
                # popped the hand naturally points at the following frame
                return self.clockHand
