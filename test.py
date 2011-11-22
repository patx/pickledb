import pickledb

db=pickledb.load('db.json')

db.set('name', 'Smith')

print db.get('name')