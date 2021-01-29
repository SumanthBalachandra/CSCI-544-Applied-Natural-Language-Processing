import sys
from fst import FST
from fsmutils import composewords

kFRENCH_TRANS = {0: "zero", 1: "un", 2: "deux", 3: "trois", 4:
                 "quatre", 5: "cinq", 6: "six", 7: "sept", 8: "huit",
                 9: "neuf", 10: "dix", 11: "onze", 12: "douze", 13:
                 "treize", 14: "quatorze", 15: "quinze", 16: "seize",
                 20: "vingt", 30: "trente", 40: "quarante", 50:
                 "cinquante", 60: "soixante", 100: "cent"}

kFRENCH_AND = 'et'

def prepare_input(integer):
    assert isinstance(integer, int) and integer < 1000 and integer >= 0, \
      "Integer out of bounds"
    return list("%03i" % integer)

def french_count():
    f = FST('french')

    f.add_state('start')
    f.add_state('q1')
    f.add_state('q2')
    f.add_state('q3')
    f.add_state('q4')
    f.add_state('q5')
    f.add_state('q6')
    f.add_state('q7')
    f.add_state('q8')
    f.add_state('q9')
    f.add_state('q10')
    f.add_state('q11')
    f.add_state('q12')

    f._set_initial_state('start')

    f.set_final('q2')
    f.set_final('q4')
    f.set_final('q5')
    f.set_final('q7')
    f.set_final('q8')
    f.set_final('q9')
    f.set_final('q10')
    f.set_final('q11')
    f.set_final('q12')

    f.add_arc('start', 'q1', ['0'], [])
    f.add_arc('q1', 'q2', ['0'], [])
    for i in range(10):
        f.add_arc('q2', 'q2', [str(i)], [kFRENCH_TRANS[i]])

    for i in range(2, 10):
        f.add_arc('start', 'q3', [str(i)], [kFRENCH_TRANS[i] + " " + kFRENCH_TRANS[100]])
    f.add_arc('start', 'q3', ['1'], [kFRENCH_TRANS[100]])
    f.add_arc('q3', 'q4', ['0'], [])
    for i in range(1, 10):
        f.add_arc('q4', 'q4', [str(i)], [kFRENCH_TRANS[i]])
    f.add_arc('q4', 'q4', ['0'], [])

    f.add_arc('q3', 'q5', ['1'], [])
    for i in range(0, 7):
        f.add_arc('q5', 'q5', [str(i)], [kFRENCH_TRANS[i + 10]])
    f.add_arc('q5', 'q5', ['7'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[7]])
    f.add_arc('q5', 'q5', ['8'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[8]])
    f.add_arc('q5', 'q5', ['9'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[9]])

    f.add_arc('q1', 'q5', ['1'], [])

    for i in range(2, 7):
        f.add_arc('q3', 'q6', [str(i)], [kFRENCH_TRANS[i * 10]])
        f.add_arc('q1', 'q6', [str(i)], [kFRENCH_TRANS[i * 10]])
    f.add_arc('q6', 'q7', ['1'], ["et" + " " + kFRENCH_TRANS[1]])

    f.add_arc('q1', 'q8', ['7'], [kFRENCH_TRANS[60]])
    f.add_arc('q3', 'q8', ['7'], [kFRENCH_TRANS[60]])
    f.add_arc('q8', 'q12', ['1'], ["et" + " " + kFRENCH_TRANS[11]])

    for i in [0, 2, 3, 4, 5, 6]:
        f.add_arc('q8', 'q8', [str(i)], [kFRENCH_TRANS[i + 10]])
    f.add_arc('q8', 'q8', ['7'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[7]])
    f.add_arc('q8', 'q8', ['8'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[8]])
    f.add_arc('q8', 'q8', ['9'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[9]])

    f.add_arc('q1', 'q9', ['8'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    f.add_arc('q3', 'q9', ['8'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    f.add_arc('q1', 'q10', ['9'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])
    f.add_arc('q3', 'q10', ['9'], [kFRENCH_TRANS[4] + " " + kFRENCH_TRANS[20]])

    for i in range(1, 10):
        f.add_arc('q9', 'q9', [str(i)], [kFRENCH_TRANS[i]])
    f.add_arc('q9', 'q9', ['0'], [])

    for i in range(0, 7):
        f.add_arc('q10', 'q10', [str(i)], [kFRENCH_TRANS[i + 10]])
    f.add_arc('q10', 'q10', ['7'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[7]])
    f.add_arc('q10', 'q10', ['8'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[8]])
    f.add_arc('q10', 'q10', ['9'], [kFRENCH_TRANS[10] + " " + kFRENCH_TRANS[9]])

    for i in range(2, 10):
        f.add_arc('q6', 'q11', [str(i)], [kFRENCH_TRANS[i]])
    f.add_arc('q6', 'q11', ['0'], [])

    return f


if __name__ == '__main__':
    string_input = raw_input()
    user_input = int(string_input)
    f = french_count()
    if string_input:
        print user_input, '-->',
        print " ".join(f.transduce(prepare_input(user_input)))