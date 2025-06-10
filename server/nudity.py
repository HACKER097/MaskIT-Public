from nudenet import NudeDetector 

def nudityCheck(path):
    classifier = NudeDetector()
    c = classifier.classify(path)
    if c[path]['unsafe']>0.95:
        # True means unsafe
        return True
    else:
        return False
