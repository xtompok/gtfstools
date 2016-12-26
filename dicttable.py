class DictRow(object):
	def __init__(self,dtable,idx):
		self.dtable = dtable
		self.lut = dtable.lut
		self.ilut = dtable.ilut
		self.idx = idx

	def _dict_from_item(self,line):
		itemdict = { (self.ilut[i],itm) for (i,itm) in enumerate(line)}
		return itemdict
	
	
	def to_dict(self):
		line = self.dtable.table[self.idx]
		return self._dict_from_item(line)

	def to_list(self):
		return self.dtable.table[self.idx]

	def __getitem__(self,key):
		return self.dtable.table[self.idx][self.lut[key]]

	def __setitem__(self,key,val):
		self.dtable.table[self.idx][self.lut[key]]=val

	def __len__(self):
		return len(self.lut)

	def __lt__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] < other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")
	
	def __gt__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] > other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")
	
	def __le__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] <= other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __ge__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] >= other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __eq__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] == other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __ne__(self,other):
		if type(other)==DictRow:
			return self.dtable.table[self.idx] != other.dtable.table[other.idx]
		else:
			raise TypeError("Not comparing with DictRow")

	def __repr__(self):
		return repr(self.to_dict())
		
	

class DictTableIterator(object):
	def __init__(self,dtable):
		self.idx = 0
		self.dtable = dtable
	
	def __iter__(self):
		return self
	
	def __next__(self):
		if self.idx >= len(self.dtable.table):
			raise StopIteration
		item = DictRow(self.dtable,self.idx)
		self.idx+= 1
		return item


class DictTable(object):
	def __init__(self,columns):
		self.columns = columns
		# column name : number
		self.lut = {k:v for (v,k) in enumerate(columns)}
		# number : column name
		self.ilut = {k:v for (k,v) in enumerate(columns)}
		self.table = []

	def _item_from_dict(self,adict):
		line = []
		for i in range(len(self.ilut)):
			line.append(adict[self.ilut[i]])
		return line
	
	
	def __getitem__(self,idx):
		return DictRow(self,idx)
	
	def __len__(self):
		return len(self.table)
	
	def __setitem__(self,idx,val):
		if type(val) == list:
			if len(val) != len(self.lut):
				raise TypeError("Trying to insert item with wrong number of columns")
			self.table[idx]=val
		elif type(val) == dict:
			_item_from_dict(self,idx,val)
		elif type(val) == DictRow:
			self.table[idx]=val.to_list()
	def __iter__(self):
		return DictTableIterator(self)
	
	def __repr__(self):
		return "DictTable({} items, columns: {})".format(len(self),self.columns)

	def append(self,item):
		self.table.append([])
		self[-1]=item

