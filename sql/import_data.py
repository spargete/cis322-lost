def import_acquisitions() :
	#noop
def import_convoy () :
	#TODO
def import_DC_inventory () :
	DC_inventory = open("DC_inventory.csv")
	DC_inventory.readline()
	for i in range(4) :
		s = DC_inventory.readline().strip().split(",")
		print("INSERT INTO products (description) VALUES ({});".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
		print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a WHERE asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 10, 2017', s[0]))
		print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'HQ') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		tag = s[3].split(":")
		level = tag[1]
		compartment = tag[0]
		print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
		print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
		print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))


def import_HQ_inventory () :
	HQ_inventory = open("HQ_inventory.csv")
	HQ_inventory.readline()
	for i in range(3) :
		s = HQ_inventory.readline().strip().split(",")
		print("INSERT INTO products (description) VALUES ({});".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
		print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a WHERE asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 7, 2017', s[0]))
		print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'HQ') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		tag = s[3].split(":")
		level = tag[1]
		compartment = tag[0]
		print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
		print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
		print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))

	s = HQ_inventory.readline().strip().split(",")
	print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
	print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a WHERE asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 7, 2017', s[0]))
	print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'HQ') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))


	HQ_inventory.close()

def import_MB005_inventory () :
	MB005_inventory = open("MB005_inventory.csv")
	MB005_inventory.readline()
	for i in range(2) :
		s = MB005_inventory.readline().strip().split(",")
		print("INSERT INTO products (description) VALUES ({});".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
		print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
		##TODO: Fix arrive date somehow, given data is "Dec-15", not sure how to interpret
		print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December', s[0]))
		print("UPDATE asset_at at SET at.depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2019', s[0]))
		print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'MB005') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))

	MB005_inventory.close()

def import_NC_inventory () :
	NC_inventory = open("NC_inventory.csv")
	NC_inventory.readline()
	s = NC_inventory.readline().strip().split(",")
	print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
	print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at at SET at.depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2020', s[0]))
	print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'NC') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))
	
	s = NC_inventory.readline().strip().split(",")
	print("INSERT INTO products (description) VALUES ({});".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
	print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a where a.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at at SET at.depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2021', s[0]))
	print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'NC') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	
	s = NC_inventory.readline().strip().split(",")
	print("INSERT INTO products (description) VALUES ({});".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
	print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a where a.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at at SET at.depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2017', s[0]))
	print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'NC') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))

	s = NC_inventory.readline().strip().split(",")
	print("INSERT INTO products (description) VALUES ({});".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
	print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a where a.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'NC') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment, s[0]))

	NC_inventory.close()

def import_SPNV_inventory () :
	SPNV_inventory = open("SPNV_inventory.csv")
	SPNV_inventory.readline()
	for i in range(2) :
		s = SPNV_inventory.readline().strip().split(",")
		print("INSERT INTO products (description) VALUES ({});".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ({});".format(s[0]))
		print("UPDATE assets a SET a.product_fk = (SELECT product_pk FROM products p WHERE p.description = '{}') WHERE a.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets a where a.asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at at SET at.facility_fk = (SELECT facility_pk FROM facilities f WHERE f.fcode = 'SPNV') WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		print("UPDATE asset_at at SET at.arrive_dt = '{}' WHERE at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
		if i == 0 :
			tag_list = s[3].strip().split(",")
			for each in tag_list :
				level = each.split(":")[1]
				compartment = each.split(":")[0]
				print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
				print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND t.level_fk = null;".format(level.lower(), s[0]))
				print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND t.compartment_fk = null;".format(compartment.lower(), s[0]))
		else :
			tag = s[3].split(":")
			level = tag[1]
			compartment = tag[0]
			print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets a WHERE a.asset_tag = '{}';".format(s[0]))
			print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level.lower(), s[0]))
			print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}')".format(compartment.lower(), s[0]))

	SPNV_inventory.close()

def import_facilities () :
	print("INSERT INTO facilities (fcode, common_name) VALUES (SPNV, 'Sparks, NV');")
	print("INSERT INTO facilities (fcode, common_name) VALUES (NC, 'National City');")
	print("INSERT INTO facilities (fcode, common_name) VALUES (MB005, MB005);")
	print("INSERT INTO facilities (fcode, common_name) VALUES (HQ, Headquarters);")
	print("INSERT INTO facilities (fcode, common_name) VALUES (DC, 'Washington, D.C.');")
	print("INSERT INTO facilities (fcode, common_name) VALUES (GL, 'Groom Lake');")
	print("INSERT INTO facilities (fcode, common_name) VALUES (LANM, 'Los Alamos, NM');")
	print("INSERT INTO facilities (fcode, common_name) VALUES (S300, 'Site 300');")

def import_product_list () :
	product_list = open("product_list.csv")
	product_list.readline()
	for i in range(5) :
		s = product_list.readline().strip().split(",")
		print("INSERT INTO products (vendor, description, alt_description) VALUES ({}, {}, {});".format(s[4], s[0], s[2]))
	
	print("INSERT INTO security_tags (product_fk) SELECT product_pk FROM products WHERE description = 'unobtainium';")
	print("UPDATE security_tags t SET t.level_fk = (SELECT level_pk FROM levels l WHERE l.abbrv = 'ss') WHERE product_fk = (SELECT product_pk FROM products WHERE description = 'unobtainium');")
	print("UPDATE security_tags t SET t.compartment_fk = (SELECT compartment_pk FROM compartments c WHERE c.abbrv = 'nrg') WHERE product_fk = (SELECT product_pk FROM products WHERE description = 'unobtainium');")

	product_list.close()

def import_security_compartments () :
	compartments = open("security_compartments.csv")
	compartments.readline()
	for i in range(7) :
		s = compartments.readline().strip().split(",")
		print("INSERT INTO compartments (abbrv, comment) VALUES ({}, {});".format(s[0], s[1]))
	compartments.close()

def import_security_levels () :
	levels = open("security_levels.csv")
	levels.readline()
	for i in range(5) :
		s = levels.readline().strip().split(",")
		print("INSERT INTO levels (abbrv, comment) VALUES ({}, {});".format(s[0], s[1]))
	levels.close()

def import_transit () :
	#TODO
def import_vendors () :
	#noop