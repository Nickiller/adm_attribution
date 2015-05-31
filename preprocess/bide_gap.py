from __future__ import division
'''
Python implementation of the Gap-Bide algorithm.
Based on
Chun Li,Jianyong Wang.
Efficiently Mining Closed Subsequences with Gap Constraints.
Siam SDM 2008.

Usage:
from pygapbide import *
sdb = [[1,2,3,4], [1,4,2,3,5],[1,2,4,3,1,2,3,1],[1,2,4,3,1],[1,3,5],[2,3,4],[2,1,5],[3,5,3,1],[2,4,1,5,2,3,3]]
g = Gapbide(sdb,3,0,2)
g.run()
'''
class Gapbide:
    def __init__(self, sdb, sup, m, n, border):
        '''
        sdb: a list of sequences,
        sup: the minimum threshold of support,
        m,n: the gap [m,n]
        border: sid <= border, conv seq; sid > border, non-conv seq
        '''
        self.sdb = sdb
        self.sup = sup
        self.m = m
        self.n = n
        self.border = border
        self.count_closed = 0
        self.count_non_closed = 0
        self.count_pruned = 0
        self.pdb_list = []

    def run(self):
        l1_patterns= self.gen_l1_patterns()
        for pattern,sup,pdb in l1_patterns:
            self.span(pattern,sup,pdb)
        return self.pdb_list

    def output(self, pattern, sup , pdb):
        '''
        overide this function to output patterns to files.
        '''
        # print pattern, sup, pdb
        cnt_conv = len(set(sid[0] for sid in pdb if sid[0] <= self.border))
        assert (sup - cnt_conv) >= 0
        likelihood = float('%.4f' % (cnt_conv * 1.0 / (sup - cnt_conv))) if (sup - cnt_conv) > 0 else sup
        self.pdb_list.append((pattern,sup,likelihood))
        # print pattern,sup,likelihood

    def gen_l1_patterns(self):
        '''
        generate length-1 patterns
        '''
        pdb_dict = {}
        for sid in range(len(self.sdb)):
            seq = self.sdb[sid]
            for pos in range(len(seq)):
                if pdb_dict.has_key( seq[pos] ):
                    pdb_dict[seq[pos]].append((sid,pos,pos))
                else:
                    pdb_dict[seq[pos]] = [ (sid, pos, pos) ]
        patterns = []
        for item, pdb in pdb_dict.items():
            # print item,pdb
            sup = len(set([i[0] for i in pdb]))
            if sup >= self.sup:
                patterns.append(([item],sup,pdb))
        return patterns

    def span(self, pattern, sup, pdb):
        (backward,prune) = self.backward_check( pattern, sup, pdb)
        if prune:
            self.count_pruned += 1
            return
        forward = self.forward_check(pattern, sup, pdb)
        if not (backward or forward):
            self.count_closed += 1
            self.output(pattern, sup, pdb)
        else:
            self.count_non_closed += 1
        pdb_dict = {}
        for (sid, begin, end) in pdb:
            seq = self.sdb[sid]
            new_begin = end + 1 + self.m
            new_end = end + 2 + self.n
            if new_begin >= len(seq): continue
            if new_end > len(seq): new_end = len(seq)
            for pos in range(new_begin, new_end):
                if pdb_dict.has_key( seq[pos] ):
                    pdb_dict[seq[pos]].append( (sid, begin, pos) )
                else:
                    pdb_dict[seq[pos]] = [ (sid, begin, pos) ]
        for item, new_pdb in pdb_dict.items():
            sup = len(set([i[0] for i in new_pdb]))
            if sup >= self.sup:
                #add new pattern
                new_pattern = pattern[:]
                new_pattern.append(item)
                self.span(new_pattern, sup, new_pdb)

    def forward_check(self, pattern, sup, pdb):
        sids = {}
        forward = False
        for (sid, begin, end) in pdb:
            seq = self.sdb[sid]
            new_begin = end + 1 + self.m
            new_end = end + 2 + self.n
            if new_begin >= len(seq):
                continue
            if new_end > len(seq):
                new_end = len(seq)
            for pos in range(new_begin, new_end):
                if sids.has_key( seq[pos] ):
                    sids[ seq[pos] ].append( sid )
                else:
                    sids[ seq[pos] ] = [sid]
        for item,sidlist in sids.items():
            seq_sup = len(set(sidlist))
            if seq_sup == sup:
                forward = True
                break
        return forward

    def backward_check(self, pattern, sup, pdb):
        sids = {}
        backward = False
        prune = False
        for (sid, begin, end) in pdb:
            seq = self.sdb[sid]
            new_begin = begin - self.n - 1
            new_end = begin - self.m - 1
            if new_end < 0:
                continue
            if new_begin < 0:
                new_begin = 0
            for pos in range(new_begin, new_end):
                if sids.has_key(seq[pos]):
                    sids[ seq[pos] ].append( sid )
                else:
                    sids[ seq[pos] ] = [sid]
        for item,sidlist in sids.items():
            seq_sup = len(set(sidlist))
            uni_sup = len(sidlist)
            if uni_sup == len(pdb):
                prune = True
            if seq_sup == sup:
                backward = True
            if backward and prune:
                break
        return (backward, prune)
