from fitparse import FitFile
from pprint import pprint

fitfile = FitFile('./3881862937.fit')


sum_level = 0
count_level = 0
for lap in fitfile.get_messages('lap'):
    pprint(lap.as_dict())

    import ipdb
    ipdb.set_trace()

for record in fitfile.get_messages('lap'):

    myset.add(record.header.local_mesg_num)

    # Go through all the data entries in this record
    for record_data in record:

        # Print the records name and value (and units if it has any)
        if record_data.units:
            print(" * %s: %s %s" % (
                record_data.name, record_data.value, record_data.units,
            ))
        else:
            print(" * %s: %s" % (record_data.name, record_data.value))
    print('\n')

myset = set()
for msg in fitfile.messages:
    myset.add(msg.header.local_mesg_num)


print(myset)

# print(list(myset))

