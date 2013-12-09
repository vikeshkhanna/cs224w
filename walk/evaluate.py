def getYList(Gcollab_base, Gcollab_delta, u):
	unode = Gcollab_delta.GetNI(u)
	return [v for v in unode.GetOutEdges() if Gcollab_base.IsNode(v)]

def getAccuracy(top, actual, k):
	topk = top[:k]
 
	preck = set(actual).intersection(topk)	
	num_common = len(preck)
	num_actual = len(actual)
	recall = float(num_common)/num_actual

	indices = []

	for a in actual:
		index = top.index(a)
		indices.append(index)

	# Diagnostic
	print("Actual - %s"%str(actual))
	print("Indices - %s"%str(indices))

	average_rank = sum(indices)/float(len(indices))

	return (recall, preck, average_rank)


