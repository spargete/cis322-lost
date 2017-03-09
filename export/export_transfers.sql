SELECT a.asset_tag, ur.username, r.request_dt, ua.username, r.approval_dt, fs.facility_fcode, fd.facility_fcode, t.load_dt, t.unload_dt FROM 
transfer_requests AS r INNER JOIN users AS ur ON r.requester_fk=ur.user_pk INNER JOIN transfers AS t ON t.request_fk=r.request_pk INNER JOIN 
users AS ua ON r.approver_fk=ua.user_pk INNER JOIN assets AS a ON r.asset_fk=a.asset_pk INNER JOIN facilities AS fs ON r.source_fk=fs.facility_pk 
INNER JOIN facilities AS fd ON r.dest_fk=fd.facility_pk;