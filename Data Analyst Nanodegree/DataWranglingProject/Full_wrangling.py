import codecs
import re
import json
import pprint
import xml.etree.cElementTree as ET



lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
			"Trail", "Parkway", "Commons"]

mapping = { "St": "Street",
			"St.": "Street",
			"Ave": "Avenue",
			"Ave.": "Avenue",
			"Av": "Avenue",
			"Blvd": "Boulevard",
			"Blvd.": "Boulevard",
			"blvd": "Boulevard",
			"Dr": "Drive",
			"dr": "Drive",
			"Dr.": "Drive",
			"E": "Ease",
			"Expy": "Expressway",
			"Ln.": "Lane",
			"N": "North",
			"P": "Park",
			"Pkwy": "Parkway",
			"St": "Street",
			"St.": "Street",
			"Rd": "Road",
			"Rd.": "Road"
			}
uniqname = {}


def corrected_name(name):
	m = street_type_re.search(name)
	if m:
		m = m.group()
		if m not in expected:
			if m in mapping:
				return mapping[m]
	return name
	pass

def shape_element(element):
	node = {}
	if element.tag == "node" or element.tag == "way" :
		if element.tag == "node":
			node['created'] = {}
			pos = []
			pos.append(float(element.attrib['lat']))
			pos.append(float(element.attrib['lon']))
			node['pos'] = pos
			node['type'] = "node"
			for k,v in element.attrib.items():
				if k in CREATED:
					node['created'][k] = v
				elif k=="lat" or k == "lon":
					continue
				else:
					node[k] = v
					
		
		if element.tag == "way":
			node['created'] = {}
			node['type'] = "way"
			for k,v in element.attrib.items():
				if k in CREATED:
					node['created'][k] = v
				else:
					node[k] = v
			nd = []
			for n in element.findall('nd'):
				nd.append(n.attrib['ref'])
			if len(nd)>0:
				node["node_refs"] = nd
			
			
		addr = {}
		for t in element.findall('tag'):
			if t.attrib['k'].count(':') == 1:
				_m,v = t.attrib['k'].split(':')
				if _m == "addr":
					cname = corrected_name(t.attrib['v'])
					addr[v] = cname
			# elif t.attrib['k'].count(':') == 2:
			#     continue
			# else:
			#     node[t.attrib['k']] = t.attrib['v']
		if len(addr)>0:
			node['address'] = {}
			node['address'] = addr
			
		# print pprint.pprint(node)
		# print "---"
		return node
	else:
		return None



def analysedata(filename, pretty=False):

	data = []
	file_out = "{0}.json".format(filename)
	with codecs.open(file_out, 'w') as fo:
		for _, element in ET.iterparse(filename):
			el = shape_element(element)
			if el:
				data.append(el)
				if pretty:
					fo.write(json.dumps(el, indent=2)+"\n")
				else:
					fo.write(json.dumps(el) + "\n")
	return data
	pass


def main():
	data = analysedata('Dallas.osm')
	pass


if __name__ == '__main__':
	main()