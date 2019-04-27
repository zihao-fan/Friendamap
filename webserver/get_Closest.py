
def get_closest(list_of_nearby, favorite_place):
	""" score = 0 + no. pf duplicates in categories * 5 - price dollar sign digits difference * 2 - rating difference * 10 """
	ref_rating = float(favorite_place["rating"]) # this is a float
	ref_price_len = len(favorite_place["price"]) # this is the length of the dollar sign - an int
	ref_categ = favorite_place["categories"] # this is a string!

	for item in list_of_nearby:
		score = 0
		list_of_cat_words = item[categories].split()
		for word in list_of_cat_words:
			if word in ref_categ:
				score += 1
		score = score * 5
		score = score - 2 * abs(len(item["price"]) - ref_price_len)
		score = score - 10 * abs(float(item["rating"]) - ref_rating)
		item["score"] = score

	for item in list_of_nearby:
		return_list = []
		return_list.append({"id": item["id"], "score": item["score"]})

	return_list = sorted(return_list, key = lambda i: i["score"])
	return return_list




