import csv

def import_convoy():
	convoy_file = open("convoy.csv")
	convoy = csv.reader(convoy_file, skipinitialspace=True)
	next(convoy)
	for s in convoy:
		print("INSERT INTO convoys (request, depart_dt, arrive_dt) VALUES ('{}', '{}', '{}');".format(s[0], s[1], s[6]))
		vehicles = s[7].strip().split(",")
		for j in range(len(vehicles)):
			print("INSERT INTO assets (asset_tag, description) VALUES ('{}', 'vehicle');".format(vehicles[j].strip()))
			print("INSERT INTO vehicles (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(vehicles[j].strip()))
			print("INSERT INTO used_by (convoy_fk) SELECT convoy_pk FROM convoys WHERE convoys.request = '{}';".format(s[0]))
			print("UPDATE used_by SET vehicle_fk = (SELECT vehicle_pk FROM vehicles WHERE vehicles.asset_fk = (SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}')) WHERE used_by.convoy_fk = (SELECT convoy_pk FROM convoys WHERE convoys.request = '{}');".format(vehicles[j].strip(), s[0]))

	convoy_file.close()

def import_DC_inventory():
	DC_file = open("DC_inventory.csv")
	DC_inventory = csv.reader(DC_file, skipinitialspace=True)
	next(DC_inventory)
	for s in DC_inventory:
		print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
		print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 10, 2017', s[0]))
		print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'HQ') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		tag = s[3].split(":")
		level = tag[1]
		compartment = tag[0]
		print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
		print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
		print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))

	DC_file.close()

def import_HQ_inventory():
	HQ_file = open("HQ_inventory.csv")
	HQ_inventory = csv.reader(HQ_file, skipinitialspace=True)
	next(HQ_inventory)
	for i in range(3):
		s = next(HQ_inventory)
		print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
		print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 7, 2017', s[0]))
		print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'HQ') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		tag = s[3].split(":")
		level = tag[1]
		compartment = tag[0]
		print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
		print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
		print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))

	s = next(HQ_inventory)
	print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
	print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 7, 2017', s[0]))
	print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'HQ') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))


	HQ_file.close()

def import_MB005_inventory():
	MB005_file = open("MB005_inventory.csv")
	MB005_inventory = csv.reader(MB005_file, skipinitialspace=True)
	next(MB005_inventory)
	for s in MB005_inventory:
		print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
		print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 15, 2016', s[0]))
		print("UPDATE asset_at SET depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2019', s[0]))
		print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'MB005') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))

	MB005_file.close()

def import_NC_inventory():
	NC_file = open("NC_inventory.csv")
	NC_inventory = csv.reader(NC_file, skipinitialspace=True)
	next(NC_inventory)
	s = next(NC_inventory)
	print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
	print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at SET depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2020', s[0]))
	print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'NC') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))
	
	s = next(NC_inventory)
	print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
	print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets where assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at SET depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2021', s[0]))
	print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'NC') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	
	s = next(NC_inventory)
	print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
	print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets where assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at SET depart_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('December 31, 2017', s[0]))
	print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'NC') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))

	s = next(NC_inventory)
	print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
	print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
	print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
	print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets where assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
	print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'NC') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
	tag = s[3].split(":")
	level = tag[1]
	compartment = tag[0]
	print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
	print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level, s[0]))
	print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment, s[0]))

	NC_file.close()

def import_SPNV_inventory():
	SPNV_file = open("SPNV_inventory.csv")
	SPNV_inventory = csv.reader(SPNV_file, skipinitialspace=True)
	next(SPNV_inventory)
	for i in range(2):
		s = next(SPNV_inventory)
		print("INSERT INTO products (description) VALUES ('{}');".format(s[1]))
		print("INSERT INTO assets (asset_tag) VALUES ('{}');".format(s[0]))
		print("UPDATE assets SET product_fk = (SELECT product_pk FROM products WHERE products.description = '{}') WHERE assets.asset_tag = '{}';".format(s[1], s[0]))
		print("INSERT INTO asset_at (asset_fk) SELECT asset_pk FROM assets where assets.asset_tag = '{}';".format(s[0]))
		print("UPDATE asset_at SET facility_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'SPNV') WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(s[0]))
		print("UPDATE asset_at SET arrive_dt = '{}' WHERE asset_at.asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format('January 8, 2017', s[0]))
		if i == 0:
			print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
			print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = 'ts') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND security_tags.level_fk = null;".format(s[0]))
			print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = 'et') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND security_tags.compartment_fk = null;".format(s[0]))
			print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
			print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = 's') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND security_tags.level_fk = null;".format(s[0]))
			print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = 'lgm') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}') AND security_tags.compartment_fk = null;".format(s[0]))
		else:
			tag = s[3].split(":")
			level = tag[1]
			compartment = tag[0]
			print("INSERT INTO security_tags (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(s[0]))
			print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(level.lower(), s[0]))
			print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = '{}') WHERE asset_fk = (SELECT asset_pk FROM assets WHERE asset_tag = '{}');".format(compartment.lower(), s[0]))

	SPNV_file.close()

def import_facilities():
	print("INSERT INTO facilities (fcode, common_name) VALUES ('SPNV', 'Sparks, NV');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('NC', 'National City');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('MB005', 'MB005');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('HQ', 'Headquarters');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('DC', 'Washington, D.C.');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('GL', 'Groom Lake');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('LANM', 'Los Alamos, NM');")
	print("INSERT INTO facilities (fcode, common_name) VALUES ('S300', 'Site 300');")

def import_product_list():
	product_list_file = open("product_list.csv")
	product_list = csv.reader(product_list_file, skipinitialspace=True)
	next(product_list)
	for s in product_list:
		print("INSERT INTO products (vendor, description, alt_description) VALUES ('{}', '{}', '{}');".format(s[4], s[0], s[2]))
	
	print("INSERT INTO security_tags (product_fk) SELECT product_pk FROM products WHERE description = 'unobtainium';")
	print("UPDATE security_tags SET level_fk = (SELECT level_pk FROM levels WHERE levels.abbrv = 'ss') WHERE product_fk = (SELECT product_pk FROM products WHERE description = 'unobtainium');")
	print("UPDATE security_tags SET compartment_fk = (SELECT compartment_pk FROM compartments WHERE compartments.abbrv = 'nrg') WHERE product_fk = (SELECT product_pk FROM products WHERE description = 'unobtainium');")

	product_list_file.close()

def import_security_compartments():
	compartments = open("security_compartments.csv")
	compartments.readline()
	for i in range(7):
		s = compartments.readline().strip().split(",")
		print("INSERT INTO compartments (abbrv, comment) VALUES ('{}', '{}');".format(s[0], s[1]))

	compartments.close()

def import_security_levels():
	levels = open("security_levels.csv")
	levels.readline()
	for i in range(5):
		s = levels.readline().strip().split(",")
		print("INSERT INTO levels (abbrv, comment) VALUES ('{}', '{}');".format(s[0], s[1]))

	levels.close()

def import_transit():
	transit_file = open("transit.csv")
	transit = csv.reader(transit_file, skipinitialspace=True)
	next(transit)
	for i in range(7):
		s = next(transit)
		a = s[0].strip().split(",")
		for j in range(len(a)):
			print("INSERT INTO asset_on (asset_fk) SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}';".format(a[j].strip()))
			print("UPDATE asset_on SET convoy_fk = (SELECT convoy_pk FROM convoys WHERE convoys.request = '{}') WHERE asset_on.asset_fk = (SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}');".format(s[5], a[j].strip()))
			print("UPDATE asset_on SET load_dt = '{}' WHERE asset_on.asset_fk = (SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}');".format(s[3], a[j].strip()))
			print("UPDATE asset_on SET unload_dt = '{}' WHERE asset_on.asset_fk = (SELECT asset_pk FROM assets WHERE assets.asset_tag = '{}');".format(s[4],a[j].strip()))

		if i == 0:
			print("UPDATE convoys SET source_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'MB005') WHERE convoys.request = '{}';".format(s[5]))
			print("UPDATE convoys SET dest_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'HQ') WHERE convoys.request = '{}';".format(s[5]))
		
		elif i == 1:
			print("UPDATE convoys SET source_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'S300') WHERE convoys.request = '{}';".format(s[5]))
			print("UPDATE convoys SET dest_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'NC') WHERE convoys.request = '{}';".format(s[5]))

		elif i == 2:
			print("UPDATE convoys SET source_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'GL') WHERE convoys.request = '{}';".format(s[5]))
			print("UPDATE convoys SET dest_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'SPNV') WHERE convoys.request = '{}';".format(s[5]))

		else:
			print("UPDATE convoys SET source_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'LANM') WHERE convoys.request = '{}';".format(s[5]))
			print("UPDATE convoys SET dest_fk = (SELECT facility_pk FROM facilities WHERE facilities.fcode = 'DC') WHERE convoys.request = '{}';".format(s[5]))
		
	transit_file.close()

def main():
	import_facilities()
	import_security_compartments()
	import_security_levels()
	import_product_list()
	import_SPNV_inventory()
	import_DC_inventory()
	import_NC_inventory()
	import_MB005_inventory()
	import_HQ_inventory()
	import_convoy()
	import_transit()

if __name__ == "__main__":
	main()