from django.shortcuts import render
import sys, string


result = []
result1 = []

# Create your views here.
def index(request):
	return render(request, 'info/benlukasboysen.com/audiovisuals/index.html')


def cb(request):
	return render(request, 'info/benlukasboysen.com/audiovisuals/computational_biology/index.html')

def genomics(request):
	return render(request, 'info/benlukasboysen.com/audiovisuals/genomics/index.html')

def proteinomics(request):
	return render(request, 'info/benlukasboysen.com/audiovisuals/proteinomics/index.html')

def geninfo(request):
	query = request.GET.get("q")
	seq2 = request.GET.get("q1")
	if query:
		seq1 = query
		#query1 = request.GET.get("q1")
		#Logic here
		#query = query + query1
		del result1[:]
		data = water(seq1, seq2)
		datastr = ' >>> '.join(str(x) for x in data)
		query = datastr
		
		return render(request, 'info/benlukasboysen.com/audiovisuals/cbinfo.html',{
			'query': query
			})
	return render(request, 'info/benlukasboysen.com/audiovisuals/cbinfo.html')

def cbinfo(request):
	query = request.GET.get("q")
	seq2 = request.GET.get("q1")
	if query:
		seq1 = query
		#query1 = request.GET.get("q1")
		#Logic here
		#query = query + query1
		del result[:]
		data = needle(seq1, seq2)
		datastr = ' >>> '.join(str(x) for x in data)
		query = datastr
		
		return render(request, 'info/benlukasboysen.com/audiovisuals/cbinfo.html',{
			'query': query
			})
	return render(request, 'info/benlukasboysen.com/audiovisuals/cbinfo.html')


def proteininfo(request):
	query = request.GET.get("q")
	if query:
		return render(request, 'info/benlukasboysen.com/audiovisuals/proteininfo.html',{
			'query': query
			})
	return render(request, 'info/benlukasboysen.com/audiovisuals/proteininfo.html')



def needle(seq1, seq2):

    m, n = len(seq1), len(seq2)  # length of two sequences

    # Generate DP table and traceback path pointer matrix
    score = zeros((m+1, n+1))      # the DP table

    # Calculate DP table
    for i in range(0, m + 1):
        score[i][0] = gap_penalty * i
    for j in range(0, n + 1):
        score[0][j] = gap_penalty * j
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            match = score[i - 1][j - 1] + match_score(seq1[i-1], seq2[j-1])
            delete = score[i - 1][j] + gap_penalty
            insert = score[i][j - 1] + gap_penalty
            score[i][j] = max(match, delete, insert)
    result.append(score[m][n])
    # Traceback and compute the alignment
    align1, align2 = '', ''
    i,j = m,n # start from the bottom right cell
    while i > 0 and j > 0: # end toching the top or the left edge
        score_current = score[i][j]
        score_diagonal = score[i-1][j-1]
        score_up = score[i][j-1]
        score_left = score[i-1][j]

        if score_current == score_diagonal + match_score(seq1[i-1], seq2[j-1]):
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif score_current == score_left + gap_penalty:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1
        elif score_current == score_up + gap_penalty:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1

    # Finish tracing up to the top left cell
    while i > 0:
        align1 += seq1[i-1]
        align2 += '-'
        i -= 1
    while j > 0:
        align1 += '-'
        align2 += seq2[j-1]
        j -= 1

    finalize(align1, align2)
    return result


def finalize(align1, align2):
    align1 = align1[::-1]    #reverse sequence 1
    align2 = align2[::-1]    #reverse sequence 2

    i,j = 0,0

    #calcuate identity, score and aligned sequeces
    symbol = ''
    found = 0
    score = 0
    identity = 0
    for i in range(0,len(align1)):
        # if two AAs are the same, then output the letter
        if align1[i] == align2[i]:
            symbol = symbol + align1[i]
            identity = identity + 1
            score += match_score(align1[i], align2[i])

        # if they are not identical and none of them is gap
        elif align1[i] != align2[i] and align1[i] != '-' and align2[i] != '-':
            score += match_score(align1[i], align2[i])
            symbol += ' '
            found = 0

        #if one of them is a gap, output a space
        elif align1[i] == '-' or align2[i] == '-':
            symbol += ' '
            score += gap_penalty

    identity = float(identity) / len(align1) * 100

    print 'Identity =', "%3.3f" % identity, 'percent'
    result.append(identity)
    result.append(align1)
    #result.append(symbol)
    result.append(align2)
    result1.append(identity)
    result1.append(align1)
    #result.append(symbol)
    result1.append(align2)

def zeros(shape):
    retval = []
    for x in range(shape[0]):
        retval.append([])
        for y in range(shape[1]):
            retval[-1].append(0)
    return retval

match_award      = 1
mismatch_penalty = -1
gap_penalty      = -1 # both for opening and extanding

def match_score(alpha, beta):
    if alpha == beta:
        return match_award
    elif alpha == '-' or beta == '-':
        return gap_penalty
    else:
        return mismatch_penalty



def water(seq1, seq2):
    m, n = len(seq1), len(seq2)  # length of two sequences

    # Generate DP table and traceback path pointer matrix
    score = zeros((m+1, n+1))      # the DP table
    pointer = zeros((m+1, n+1))    # to store the traceback path

    max_score = 0        # initial maximum score in DP table
    # Calculate DP table and mark pointers
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            score_diagonal = score[i-1][j-1] + match_score(seq1[i-1], seq2[j-1])
            score_up = score[i][j-1] + gap_penalty
            score_left = score[i-1][j] + gap_penalty
            score[i][j] = max(0,score_left, score_up, score_diagonal)
            if score[i][j] == 0:
                pointer[i][j] = 0 # 0 means end of the path
            if score[i][j] == score_left:
                pointer[i][j] = 1 # 1 means trace up
            if score[i][j] == score_up:
                pointer[i][j] = 2 # 2 means trace left
            if score[i][j] == score_diagonal:
                pointer[i][j] = 3 # 3 means trace diagonal
            if score[i][j] >= max_score:
                max_i = i
                max_j = j
                max_score = score[i][j];
            result1.append(max_score)
    align1, align2 = '', ''    # initial sequences

    i,j = max_i,max_j    # indices of path starting point

    #traceback, follow pointers
    while pointer[i][j] != 0:
        if pointer[i][j] == 3:
            align1 += seq1[i-1]
            align2 += seq2[j-1]
            i -= 1
            j -= 1
        elif pointer[i][j] == 2:
            align1 += '-'
            align2 += seq2[j-1]
            j -= 1
        elif pointer[i][j] == 1:
            align1 += seq1[i-1]
            align2 += '-'
            i -= 1

    finalize(align1, align2)
    return result1