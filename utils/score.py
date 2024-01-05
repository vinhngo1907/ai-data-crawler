import json
import copy


class Score:
    def make_hash(self, o):
        if isinstance(o, (set, tuple, list)):
            return tuple([self.make_hash(e) for e in o])
        elif not isinstance(o, dict):
            return hash(o)
        new_o = copy.deepcopy(o)
        for k, v in new_o.items():
            new_o[k] = self.make_hash(o)
        return hash(tuple(frozenset(sorted(new_o.items()))))
