#sumber : http://www.cs.cmu.edu/~bhiksha/courses/10-601/decisiontrees/
#ini merupakan contoh decision tree yang akan kita buat untuk menunjang kita.

#------- Some "Helper" functions ---------------
# Segregating out instances that take a particular value
# attributearray is an N x 1 array.
def segregate(attributearray, value):
    outlist = []
    for i = 1 to length(attributearray):
        if (attributearray[i] == value):
            outlist = [outlist, i]  #  Append "i" to outlist
    return outlist


# Assuming labels take values 1..M.
def computeEntropy(labels):
    entropy = 0
    for i = 1 to M:
        probability_i = length(segregate(labels, i)) / length(labels)
        entropy -= probability_i * log(probability_i)
    return entropy
  
# Find most frequent value. Assuming labels take values 1..M 
def mostFrequentlyOccurringValue(labels):
    bestCount = -inf
    bestId = none
    for i = 1 to M:
        count_i = length(segregate(label,i))
        if (count_i > bestCount):
            bestCount = count_i
            bestId = i
    return bestId

#-------- The Dtree code ------------

#Here "attributes" is an Num-instance x Num-attributes matrix. Each row is
#one training instance.
#"labels" is a Num-instance x 1 array of class labels for the training instances

# Note, we're storing a number of seemingly unnecessary variables, but
# we'll use them later for counting and pruning
class  dtree:
    float @nodeGainRatio
    float @nodeInformationGain
    boolean @isLeaf 
    integer @majorityClass
    integer @bestAttribute
    dtree[] @children
    dtree   @parent

    init(attributes, labels):
        @parent = null
        buildTree (attributes, labels, self)

    buildTree (attributes, labels, self):
        numInstances = length(labels)
        nodeInformation = numInstances * computeEntropy(labels)
        @majorityClass = mostFrequentlyOccurringValue(labels)

        if (nodeinformation == 0):  # This is a "pure" node
            @isLeaf = True
            return

        # First find the best attribute for this node
        bestAttribute = none
        bestInformationGain = -inf
        bestGainRatio = -inf
        for each attribute X:
            conditionalInfo = 0
            attributeEntropy = 0
            for each attributevalue Y:
                ids = segregate(attributes[][X], Y) # get ids of all instances
                                                    # for which attribute X == Y
 
                attributeCount[Y] = length(ids)
                conditionalInfo += attributeCount[Y] * computeEntropy(labels(ids));
            attributeInformationGain =  nodeInformation - conditionalInfo
            gainRatio = attributeInformationGain / computeEntropy(attributeCount)
            if (gainRatio > bestGainRatio):
                bestInformationGain = attributeInformationGain
                bestGainRatio = gainRatio
                bestAttribute = X

        #If no attribute provides andy gain, this node cannot be split further
        if (bestGainRatio == 0):
            @isLeaf = True
            return

        # Otherwise split by the best attribute
        @bestAttribute = bestAttribute
        @nodeGainRatio = bestGainRatio
        @nodeInformationGain = bestInformationGain
        for each attributevalue Y:
            ids = segregate(attributes[][bestAttribute], Y)
            @children[Y] = dtree(attributes[ids], labels[ids])
            @children[Y].@parent = self
        return