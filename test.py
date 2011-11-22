import pickledb

db=pickledb.load('none.json')

print db.get('name')

db.load('db.json')

db.set('name', 'Smith')

print db.get('name')

db.flushdb()

print db.get('name')