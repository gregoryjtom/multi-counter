"""
WORD COUNTER PROGRAM
*used https://docs.python.org/3/library/concurrent.futures.html as a reference
"""

import glob, re, sys, collections
import concurrent.futures

def importStopWords():
    stopwords = set(open('stop_words').read().split(','))
    return stopwords

def importFiles():
    files = []
    for file in glob.glob("*.txt"):
        files.append(file)
    return files

def countWords(file, stopwords):
    words = re.findall('\w{3,}', open(file).read().lower())
    counts = collections.Counter(w for w in words if w not in stopwords)
    return counts

if __name__ == "__main__":
    stopwords = importStopWords()
    files = importFiles()

    #create new thread for each file:
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_file = {executor.submit(countWords, file, stopwords): file for file in files}
        counter = collections.Counter()
        #wait for countWords to complete, then extract data from future
        for future in concurrent.futures.as_completed(future_to_file):
            file = future_to_file[future]
            try:
                data = future.result()
                #append the new counter data to existing counter
                counter += data
            except Exception as exc:
                print('%s generated an exception: %s' % (file, exc))
        executor.shutdown()
    
    print("Most common words:")
    for (w, c) in counter.most_common(40):
        print (w, '-', c)
