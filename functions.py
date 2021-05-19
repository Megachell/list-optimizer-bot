import numpy as np
import pandas as pd
from typing import Union


def check_value(name:str, navec:dict) -> bool: # Check if there is an embedding for the word
	succ = 0
	for i in name.split(' '):
		try: 
			vec = navec[i.lower()]
			succ += 1
		except:
			pass
	return succ > 0

def _inp_to_name(shop: pd.DataFrame) -> Union[dict, list]: # Returns dict that connects ancor to group and a list of ancors
	input_to_name = {}
	points = []
	for j,i in shop[1::].iterrows():
	  points += i['Вход'].split(',')
	  for j in i['Вход'].split(','):
	    input_to_name[j] = i['Имя']
	return input_to_name, points

def _get_point(name: str, points_list: list, navec: dict) -> str: # Returns the closest ancor
	n = []
	for i in points_list:
		distances = []
		for j in name.split(' '):
			try:
				distances += [np.linalg.norm(navec[i]-navec[j.lower()])]
			except:
				pass
		n += [min(distances)] 
	return points_list[np.argmin(n)]

def get_groups(shopping_list: list, shop: pd.DataFrame, navec: dict) -> Union[pd.DataFrame, dict]: 
# Deletes unnecessary rows from the 'shop' df, and groups items from the shopping list with respect to departments
	groups = {}
	input_to_name, points = _inp_to_name(shop)
	for item in shopping_list:
	  a =  input_to_name[_get_point(item, points, navec)]
	  if a in groups.keys():
	    groups[a] += [item]
	  else:
	    groups[a] = [item]
	parts_presented = shop['Имя'].isin(groups.keys())
	parts_presented[0] = 1
	shop = shop[parts_presented]
	shop = shop.reset_index()
	return shop, groups

 
def _get_mask(n: int) -> list: # Converts row number into a bit mask
	b = bin(n)[2:]
	mask = [x == '1' for x in b]
	for i in range(0, N-len(mask)): mask.insert(False, 0)
	return mask
 
def _int_from_mask(mask: list) -> int: # Converts bit mask into a row number
	res = 0
	for i in range(0, len(mask)):
		res += mask[i]*2**(len(mask) - i-1)
	return res
 
def _not_in_mask(n: int, mask: list) -> bool: # Checks if a point is not in a bit mask 
	return not _get_mask(mask)[n]
 
def _path(n: int, ans: pd.DataFrame, M: np.array, shop: pd.DataFrame) -> list: # Calculates the shortest path
	mask = _get_mask(2**N-1)
	path = []
	prev = n if n in shop['Имя'] else ans[2**N-1].argmin()
	l = 0
	for i in range(0, N):
		path += [prev]
		l += ans.loc[prev,_int_from_mask(mask)]
		mask[prev] = False
		row = _int_from_mask(mask)
		transition_col = pd.Series(data = [M[k][prev] for k in range(0, N)])
		prev = (ans.loc[:,row] + transition_col).argmin()
		l -= ans.loc[prev, _int_from_mask(mask)]
	return list(reversed(path)), l
 
def sort_list(shop: pd.DataFrame, groups: dict) -> list: # sorts the list in order to match the shortest path
	M = []
	global N
	N = shop.shape[0]

	for num, row in shop.iterrows():
	  col = []
	  x0 = row['x']
	  y0 = row['y']
	  for i in shop.index:
	    x = shop.loc[i,'x']
	    y = shop.loc[i,'y']
	    dist = np.sqrt((x - x0)**2+(y - y0)**2)
	    col += [dist]
	  M = np.vstack((M, col)) if num != shop.index[0] else col
	 
	bit_mask = [False for i in range(0,N)]

	d = [[np.inf for i in range(0,2**N)] for j in range(0,N)]
	d[0][0] = 0
	for mask in range(0,2**N):
	    for i in range(0,N):
	      if d[i][mask] == np.inf:
	        continue
	      for j in range(0,N):
	        if _not_in_mask(j, mask):
	          m = _get_mask(mask)
	          m[j] = True
	          m = _int_from_mask(m)
	          d[j][m] = min(d[j][m], d[i][mask] + M[j][i])
	ans = pd.DataFrame(data = d)
	 
	finish = 13
	route = [shop.index[i] for i in _path(finish, ans, M, shop)[0]]
	sorted_list = []
	for i in route[1:] :
		for j in groups[shop['Имя'].loc[i]]:
			sorted_list += [j]
			
	return sorted_list

if __name__ == '__main__':
	print('functions live here')