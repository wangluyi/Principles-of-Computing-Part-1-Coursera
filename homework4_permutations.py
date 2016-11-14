def gen_all_sequences(outcomes, length):
    """
    Iterative function that enumerates the set of all sequences of
    outcomes of given length
    """
    
    ans = set([()])
    for dummy_idx in range(length):
        temp = set()
        for seq in ans:
            for item in outcomes:
                new_seq = list(seq)
                new_seq.append(item)
                temp.add(tuple(new_seq))
        ans = temp
    return ans

# example for digits
def run_example1():
    """
    Example of all sequences
    """
    outcomes = set([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
    #outcomes = set(["Red", "Green", "Blue"])
    #outcomes = set(["Sunday", "Mondy", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"])
    
    length = 2
    seq_outcomes = gen_all_sequences(outcomes, length)
    print "Computed", len(seq_outcomes), "sequences of", str(length), "outcomes"
    print "Sequences were", seq_outcomes
    
    test1 = gen_permutations(outcomes, length)
    print test1


def gen_permutations(outcomes, length):
    """
    Iterative function that generates set of permutations of
    outcomes of length num_trials
    No repeated outcomes allowed
    """
    ans = set([()])
    ans = gen_all_sequences(outcomes, length)
    
    ans_no_repetition_list=[]
    
    for e in ans:
        set_e = set(e)
        if (len(set_e)==4):
            ans_no_repetition_list.append(e)    
    
    # add code here
    
    return ans_no_repetition_list







outcome = set(["a", "b", "c", "d", "e", "f"])
#
permutations = gen_permutations(outcome, 4)
#permutation_list = list(permutations)
#permutation_list.sort()
print permutations
#print "Answer is", permutation_list[100]


