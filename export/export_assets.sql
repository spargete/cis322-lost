SELECT a.asset_tag, a.description, f.facility_fcode, a.intake_dt, a.disposed_dt FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk 
INNER JOIN facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt=a.intake_dt AND disposed_dt IS NOT NULL;
SELECT a.asset_tag, a.description, f.facility_fcode, a.intake_dt, concat('NULL', a.disposed_dt) AS disposed_dt FROM assets AS a INNER JOIN asset_at AS aa ON a.asset_pk=aa.asset_fk 
INNER JOIN facilities AS f ON f.facility_pk=aa.facility_fk WHERE aa.arrive_dt=a.intake_dt AND disposed_dt IS NULL;