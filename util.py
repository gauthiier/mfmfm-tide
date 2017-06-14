def next(d, db):
	prev = None
	for x in sorted(db):
		if d < x:
			return (prev, x)
		prev = x
	return None
