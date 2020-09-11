import random, math, time, numpy as np
random.seed()
repetition_index = 1.1
number_of_series = 32#int(input('Series in each part/line: '))
number_of_lines = 2#int(input('Number of parts/lines: '))
ttr = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
ttc = []
D,PRM = [[],[]], []
TTM = np.zeros((12,12))
note_conversion = ['c', 'cs', 'd', 'ds', 'e', 'f', 'fs', 'g', 'gs', 'a', 'as', 'b']
conv = []
tone_label = []
used_rows = [0,0,0,0]
savename = 'testing1'#input('save name: ') needs to be written out here for atom
tempo = 100
TRN = 0
f = open(savename + ".ly","w+")

def twelve(n): #Corrects Octave Issues.  ie. if n =-3 12 will be added to n to become n=9 which is a note
    if n < 0:
        return 12
    elif n > 11:
        return -12
    else:
        return 0

def matrix(): #creates Tone Row Matrix (TTM)
    for x in range(11): #creates First Inversion Row (I-0)
        ttc.append(-1 * (ttr[x + 1] - ttr[x]) + ttc[x] + twelve(-1 * (ttr[x + 1] - ttr[x]) + ttc[x]))
    for x in range(12): #fills TTM with Prime and Inversion
        TTM[0][x] = ttr[x]
        TTM[x][0] = ttc[x]
    for i in range(1,12): #Fills in rest of matrix based off of Prime and Inversion
        for x in range (1,12):
            TTM[i][x] = TTM[i][x - 1] - TTM[i-1][x-1] + TTM[i-1][x] + twelve((TTM[i][x - 1] - TTM[i-1][x-1] + TTM[i-1][x]))

def get_series(r): #randomly chooses row/column from matrix and labels it.
    ftr = [] #final tone row which is returned by function
    #   Unforunately <condition> ? <expression1> : <expression2> from C has been deemed non-Pythonic
    col = random.randint(0,1)
    direction = (-1 if (random.randint(0,1) == 1) else 1) #normal or retrograde
    #print(f'{col} t ${direction}')
    element = random.randint(0,11) #number of rows or columns after 0 to obtain
    avg = (used_rows[0] + used_rows[1] + used_rows[2] + used_rows[3]) / 4
    if col == 1: #If statements determine if chosen row/column is part of
        if direction == 1 and used_rows[0] <= avg:
            tone_label.append('I-' + str(int(TTM[0][element] - TTM[0][0] + twelve(TTM[0][element] - TTM[0][0])))) #ID's relationship btw Inversion and chosen column in half steps
            for x in range(0,12):
                ftr.append(int(TTM[x][element]))
            used_rows[0] = used_rows[0] + 1
        elif direction == -1 and used_rows[1] <= avg:
            tone_label.append('RI-' + str(int(TTM[11][element] - TTM[11][0] + twelve(TTM[11][element] - TTM[11][0])))) #ID's relationship btw Retrograde Inversion and chosen column in half steps
            for x in range(11, -1, -1):
                ftr.append(int(TTM[x][element]))
            used_rows[1] = used_rows[1] + 1
        else:
            return 'failed'
    else:
        if direction == 1 and used_rows[2] <= avg:
            tone_label.append('P-' + str(int(TTM[element][0] - TTM[0][0] + twelve(TTM[element][0] - TTM[0][0])))) #ID's relationship btw Prime and chosen row in half steps
            for x in range(0,12):
                ftr.append(int(TTM[element][x]))
            used_rows[2] = used_rows[2] + 1
        elif direction == -1 and used_rows[3] <= avg:
            tone_label.append('R-' + str(int(TTM[element][11] - TTM[0][11] + twelve(TTM[element][11] - TTM[0][11])))) #ID's relationship btw Retrograde and chosen row in half steps
            for x in range(11, -1, -1):
                ftr.append(int(TTM[element][x]))
            used_rows[3] = used_rows[3] + 1
        else:
            return 'failed'
    return ftr

def convert(L): #int to str for tone row
    for i in range(12):
        L[i] = note_conversion[L[i]]
    return L

def played_rows(r):
    PRM = np.zeros((r,12), dtype = np.dtype('U4'))
    x = 1
    while x <= r:
        l = get_series(range(r))
        if l == 'failed':
            x = x - 1
        else:
            for i in range(12):
                l[i] = note_conversion[l[i]]
            for i in range(0,12):
                PRM[x-1][i] = str(l[i])
        x = x + 1
    return PRM

def rhythm(A):
    n = round(len(A[0]) * repetition_index,0) #number of beats
    rhythm = []
    for i in range(len(A)):
        a = []
        b = 0
        while b < n:
            r = random.randint(1, 100)
            if 0 < r and r < 23: #half notes
                a.append(2)
                b = b + 2
            elif 23 <= r and r < 68: #quarters and dotted quarter combos
                if 23 <= r and r < 60:
                    a.append(4)
                    b = b + 1
                elif 60 <= r and r < 64:
                    a.append(float(4.))
                    a.append(8)
                    b = b + 2
                else:
                    a.append(8)
                    a.append(float(4.))
                    b = b + 2
            elif 68 <= r and r < 93:  #eighth and dotted eighth combos
                b = b + 1
                if 68 <= r and r < 87:
                    a.append(8)
                    a.append(8)
                elif 87 <= r and r < 90:
                    a.append(16)
                    a.append(float(8.))
                else:
                    a.append(float(8.))
                    a.append(16)
            elif 93 <= r and r <= 100:  #16th combos
                b = b + 1
                if 93 <= r and r < 95:
                    a.append(16)
                    a.append(8)
                    a.append(16)
                elif 95 <= r and r < 97:
                    a.append(16)
                    a.append(16)
                    a.append(8)
                elif 97 <= r and r <99:
                    a.append(8)
                    a.append(16)
                    a.append(16)
                else:
                    a.append(16)
                    a.append(16)
                    a.append(16)
                    a.append(16)
            if n - b <= 6: #Will conclude in a way that makes 4/4 possible
                if b%4 == 1: #5 beats remaining
                    for x in range(3):
                        a.append(4)
                    a.append(2)
                    b = b + 5
                elif b%4 == 2: #6 beats remaining
                    for x in range(3):
                        a.append(2)
                    b = b + 6
                elif b%4 == 3: #3 beats remaining
                    a.append(4)
                    a.append(2)
                    b = b + 3
                else:  #4 beats remaining
                    for x in range(2):
                        a.append(4)
                    a.append(2)
                    b = b + 4
                b = n + 1
        rhythm.append(a)
    return rhythm

def repeater(A,B): #A is Notes, B is Rhythms
    C = []         #Rests do not currently exist
    for x in range(len(A)):
        n = math.floor(len(B[x]) / number_of_series) #avg number of rhythms per series, rounded down
        d = int(((len(B[x]) / number_of_series) - n) * number_of_series) # number of notes to add in randomly
        l = A[x]
        l = np.array_split(l,(number_of_series))
        h = []
        for g in range(number_of_series):
            h.append(g)
        random.shuffle(h)
        h = h[0:d]
        for y in range(len(l)): #should run for the number of series l[y] is current 12 note sequence
            e = 12
            j = 0
            for g in range(len(h)):
                if h[g] == y:
                     e = e - 1
            used_notes = [0,0,0,0,0,0,0,0,0,0,0,0]
            while n - 1 >= e: #while there are more rhythms left than notes
                for w in range(len(used_notes)):
                    j = used_notes[w] + j
                avg = j/12
                r = random.randint(0,11)
                if used_notes[r] <= 1.1 * avg:
                    used_notes[r] = used_notes[r] + 1
                    e = e + 1
                #print(used_notes)
                #print(e)
            l[y] = list(l[y])
            v,w,a = 0,0,0
            while w <= 11:
                for z in range(used_notes[w]):
                    l[y].insert(v + z, l[y][v+z])
                if w >= 1:
                    used_notes[w] = used_notes[w] + used_notes[w - 1]
                v = used_notes[w] + 1 + w
                w = w + 1
        C.append(np.concatenate(l[:], axis = 0))
    return [list(C[0][:]),list(C[1][:])]

def combo(A,B): #A is notes, B is rhythm
    C = [[0],[0]]
    for x in range(len(A)):
        for i in range(len(A[x])):
            for q in range(len(note_conversion)):
                if note_conversion[q] == A[x][i]:
                    D[x].append(q) #C = 0, B = 11, 7 half steps = fifth
    for x in range(len(D)):
        c = 0
        #for i in range(len(D[x])-c):
        while c < len(D[x]):
            k = 0
            i = c
            if len(D) == 2: #in case not piano music
                while D[x][i] == D[x][i + k]: #checks for repeats
                    k = k + 1
                    if i + k == len(D[x]):
                        break
                c = k + c
                if x == 0: #treble
                    octave( ("\'\'") if (D[x][i] <= 4) else ("\'"), x, i, k)
                elif x == 1: #bass
                    octave( ("") if (D[x][i] <= 7) else (","), x, i, k)
    E = row_check(A)
    for x in range(len(A)):
        l = []
        for i in range(len(A[x])):
            if type(B[x][i]) == float: #for dotted rhythms
                a = str(B[x][i])
                B[x][i] = a[0:-1] #gets rid of 0 after dot
            l.append(str(A[x][i]) + str(D[x][i]) + str(B[x][i]) + str(E[x][i]))
        C[x] = l
    return C

def row_check(A):
    E = np.full((len(A),len(A[0])), "", dtype = np.dtype('U8'))
    E[0][0] = '^"' + tone_label[0] + '" '
    E[1][0] = '^"' + tone_label[1] + '" '
    a,b = 0,0
    for w in range(2,len(PRM)):
        if w%2 == 0:
            for y in range(12):
                while PRM[w-2][y] == A[0][a]:
                    a = a + 1
            E[0][a] = '^"' + tone_label[w] + '" '
        else:
            for y in range(12):
                while PRM[w-2][y] == A[1][b]:
                    b = b + 1
            E[1][b] = '^"' + tone_label[w] + '" '
        #print(E)
        #input('')
    return E

def octave(octa,x,i,k):
    for o in range(k):
        D[x][i+o] = octa

def writefile(A):
    top_notes = ""
    low_notes = ""
    for i in range(len(A[0])):
        top_notes = top_notes + str(A[0][i]) + ' '
    for i in range(len(A[1])):
        low_notes = low_notes + str(A[1][i]) + ' '
    f.write('\\version "2.18.2"\n\\language "english"\n\\header{') #Version & Language Statements
    f.write("\n"+'  title = ' + savename + "\n" + '  subtitle = "DP2 Music"\n'+'  composer = "Matthew Priskorn"\n'+'}\n\n') #Header
    f.write('\\score {  \\new PianoStaff <<\n  \\new Staff = "up" {\n') #set up both staves
    f.write("    \\tempo 4 = " + str(tempo) + "\n  {\n  ")
    f.write(top_notes)
    f.write('\n  }\n  }\n    \\new Staff = "down" {\n    \\clef bass \n  \\tempo 4 = ' + str(tempo) + '\n  {\n  ')
    f.write(low_notes)
    f.write('\n  }\n  }\n>>\n  \\layout {')
    f.write('}\n  \\midi{')
    f.write('}\n}')

random.shuffle(ttr)
ttc.append(ttr[0])
matrix()
A = played_rows(number_of_lines * number_of_series) #note matrix
PRM = A
A = np.concatenate(np.vsplit(A, len(A)/number_of_lines), axis = 1)
NM = [list(A[0][:]),list(A[1][:])] #from array to list
RM = rhythm(NM)#rhythm lists
NM = repeater(NM,RM)
#print(len(NM[0]),len(NM[1]))
#print(len(RM[0]),len(RM[1]))
FINALLY = combo(NM,RM)
#print(FINALLY[0])
#print(FINALLY[1])
if number_of_lines == 2:
    writefile(FINALLY)
else:
    print('no functionality has been added to support this feature yet.')
print(tone_label)
f.close()
