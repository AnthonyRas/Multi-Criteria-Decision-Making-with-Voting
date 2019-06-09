#multi-criteria decision problem

class attribute:
    def __init__(self, name = '', weight = 1.0, prefs = {}):
        self.name = name    # name of attribute
        self.weight = weight    # weight importance of attribute
        if len(prefs) > 0:
            self.prefs = prefs  # rank decisions by this attribute
        else:
            self.prefs = dict()

class contest:
    # takes two candidates and determines who wins in a head-to-head match
    def winner(self, ci, cj, voters):
        score = [0,0]
        for v in voters:
            if v.prefs[ci] < v.prefs[cj]:
                score[0] = score[0] + v.weight
            if v.prefs[ci] > v.prefs[cj]:
                score[1] = score[1] + v.weight
        if score[0] > score[1]:
            return [ci]
        elif score[0] < score[1]:
            return [cj]
        else:
            return []
    # constructs the head-to-head contest graph
    def __init__(self, candidates, voters):
        beats = dict()
        for c in candidates:
            beats.update({c : []})
        for i in range(len(candidates)):
            for j in range(len(candidates)):
                if i < j:
                    ci = candidates[i]
                    cj = candidates[j]
                    w = self.winner(ci, cj, voters)
                    participants = [ci, cj]
                    for k in participants:
                        if k in w:
                            l = participants.copy()
                            l.remove(k)
                            beats[k] = beats[k] + l
        self.graph = beats
        self.candidates = candidates
        self.voters = voters
    # applies the Floyd–Warshall algorithm to compute the schwartz set of the election
    def schwartz(self):
        maximal = {c : True for c in self.candidates}
        path = dict()
        for ci in self.candidates:
            for cj in self.candidates:
                if ci != cj:
                    path.update({(ci, cj) : cj in self.graph[ci]})
        for ci in self.candidates:
            for cj in self.candidates:
                for ck in self.candidates:
                    if ci != cj and cj != ck:
                        if path[(ci,cj)] and path[(cj,ck)]:
                            path.update({(ci,ck) : True})
        for ci in self.candidates:
            for cj in self.candidates:
                if ci != cj:
                    if path[(ci,cj)] and not(path[cj,ci]):
                        maximal.update({cj : False})
        return {c for c in self.candidates if maximal[c]}

class MCDP:
    def __init__(self, attributes):
        self.attributes = attributes
    # computes the schwartz set of the alternatives
    def solve(self):
        options = list(set().union(*[set(i.prefs.keys()) for i in self.attributes]))
        options = contest(options, self.attributes).schwartz()
        return set(options)