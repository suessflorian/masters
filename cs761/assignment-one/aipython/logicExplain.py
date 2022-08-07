# logicExplain.py - Explaining Proof Procedure for Definite Clauses
# AIFCA Python3 code Version 0.9.5 Documentation at http://aipython.org
# Download the zip file and read aipython.pdf for documentation

# Artificial Intelligence: Foundations of Computational Agents http://artint.info
# Copyright David L Poole and Alan K Mackworth 2017-2022.
# This work is licensed under a Creative Commons
# Attribution-NonCommercial-ShareAlike 4.0 International License.
# See: http://creativecommons.org/licenses/by-nc-sa/4.0/deed.en

from logicProblem import yes  # for asking the user

def prove_atom(kb, atom, indent=""):
    """returns a pair (atom,proofs) where proofs is the list of proofs 
       of the elements of a body of a clause used to prove atom.
    """
    kb.display(2,indent,'proving',atom)
    if atom in kb.askables:
        if yes(input("Is "+atom+" true? ")):
            return (atom,"answered")
        else:
            return "fail"
    else:
        for cl in kb.clauses_for_atom(atom):
            kb.display(2,indent,"trying",atom,'<-',' & '.join(cl.body))
            pr_body = prove_body(kb, cl.body, indent)
            if pr_body != "fail":
                return (atom, pr_body)
        return "fail"

def prove_body(kb, ans_body, indent=""):
    """returns proof tree if kb |- ans_body or "fail" if there is no proof 
    ans_body is a list of atoms in a body to be proved
    """
    proofs = []
    for atom in ans_body:
        proof_at = prove_atom(kb, atom, indent+"  ")
        if proof_at == "fail":
            return "fail"  # fail if any proof fails
        else:
            proofs.append(proof_at)
    return proofs

from logicProblem import triv_KB
def test():
    a1 = prove_atom(triv_KB,'i_am')
    assert a1, "triv_KB proving i_am gave "+str(a1)
    a2 = prove_atom(triv_KB,'i_smell')
    assert a2=="fail", "triv_KB proving i_smell gave "+str(a2)
    print("Passed unit tests")
if __name__ == "__main__":
    test()   
# try
from logicProblem import elect, elect_bug
# elect.max_display_level=3  # give detailed trace
# prove_atom(elect, 'live_w6')
# prove_atom(elect, 'lit_l1')

helptext = """Commands are:
ask atom     ask is there is a proof for atom (atom should not be in quotes)
how          show the clause that was used to prove atom
how n        show the clause used to prove the nth element of the body
up           go back up proof tree to explore other parts of the proof tree
kb           print the knowledge base
quit         quit this interaction (and go back to Python)
help         print this text
"""

def interact(kb):
    going = True
    ups = []    # stack for going up
    proof="fail"  # there is no proof to start
    while going:
        inp = input("logicExplain: ")
        inps = inp.split(" ")
        try:
            command = inps[0]
            if command == "quit":
                going = False
            elif command == "ask":
                proof = prove_atom(kb, inps[1])
                if proof == "fail":
                    print("fail")
                else:
                    print("yes")
            elif command == "how":
                if proof=="fail":
                    print("there is no proof")
                elif len(inps)==1:
                   print_rule(proof)
                else:
                    try:
                        ups.append(proof)
                        proof = proof[1][int(inps[1])] #nth argument of rule
                        print_rule(proof)
                    except:
                        print('In "how n", n must be a number between 0 and',len(proof[1])-1,"inclusive.")
            elif command == "up":
                if ups:
                    proof = ups.pop()
                else:
                    print("No rule to go up to.")
                print_rule(proof)
            elif command == "kb":
                 print(kb)
            elif command == "help":
                print(helptext)
            else:
                print("unknown command:", inp)
                print("use help for help")
        except:
            print("unknown command:", inp)
            print("use help for help")
                
def print_rule(proof):
    (head,body) = proof
    if body == "answered":
        print(head,"was answered yes")
    elif body == []:
             print(head,"is a fact")
    else:
            print(head,"<-")
            for i,a in enumerate(body):
                print(i,":",a[0])

# try
# interact(elect)
# Which clause is wrong in elect_bug? Try:
# interact(elect_bug)
# logicExplain: ask lit_l1

