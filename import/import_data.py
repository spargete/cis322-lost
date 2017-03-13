import csv

def import_assets():
	with open("assets.csv") as f:
		assets = csv.reader(f, skipinitialspace=True)
		next(assets)
		for s in assets:
			print("INSERT INTO assets (asset_tag, description, intake_dt, disposed_dt) VALUES (%s, %s, %s, %s);", (s[0], s[1], s[3], s[4]))
			print("INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=%s), (SELECT facility_pk FROM facilities WHERE facility_fcode=%s), %s);", (s[0], s[2], s[3]))

def import_facilities():
	with open("facilities.csv") as f:
		facilities = csv.reader(f, skipinitialspace=True)
		next(facilities)
		for s in facilities:
			print("INSERT INTO facilities (facility_fcode, facility_common_name) VALUES (%s, %s);", (s[0], s[1]))

def import_transfers():
	with open("transfers.csv") as f:
		transfers = csv.reader(f, skipinitialspace=True)
		next(transfers)
		for s in transfers:
			print("""INSERT INTO transfer_requests (requester_fk, request_dt, approver_fk, approval_dt, source_fk, dest_fk, asset_fk) VALUES 
				((SELECT user_pk FROM users WHERE username=%s), %s, (SELECT user_pk FROM users WHERE username=%s), 
				%s, (SELECT facility_pk FROM facilities WHERE facility_fcode=%s), 
				(SELECT facility_pk FROM facilities WHERE facility_fcode=%s), (SELECT asset_pk FROM assets WHERE asset_tag=%s));
				""", (s[1], s[2], s[3], s[4], s[5], s[6], s[0]))
			print("""INSERT INTO transfers (request_fk, asset_fk, load_dt, unload_dt) VALUES ((SELECT request_pk FROM transfer_requests WHERE asset_tag=%s 
				AND request_dt=(SELECT max(request_dt) FROM transfer_requests WHERE asset_tag=%s)), (SELECT asset_pk FROM assets WHERE asset_tag=%s), %s, %s)""", (s[0], s[0], s[0], s[7], s[8]))
			print("UPDATE asset_at SET depart_dt=%s WHERE asset_fk=(SELECT asset_pk FROM assets WHERE asset_tag=%s) AND depart_dt IS NULL", (s[0], s[7]))
			print("""INSERT INTO asset_at (asset_fk, facility_fk, arrive_dt) VALUES ((SELECT asset_pk FROM assets WHERE asset_tag=%s), 
				(SELECT facility_pk FROM facilities WHERE facility_fcode=%s), %s)""", (s[0], s[6], s[8]))

def import_users():
	with open("users.csv") as f:
		users = csv.reader(f, skipinitialspace=True)
		next(users)
		for s in users:
			print("INSERT INTO users (username, password, active) VALUES (%s, %s, %s);", (s[0], s[1], s[3]))
			print("INSERT INTO user_is (user_fk, role_fk) VALUES ((SELECT user_pk FROM users WHERE username=%s), (SELECT role_pk FROM roles WHERE role_name=%s))", (s[0], s[2]))

if __name__ == "__main__":
	import_facilities()
	import_assets()
	import_users()
	import_transfers()