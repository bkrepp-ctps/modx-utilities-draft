# TAZ-related functions and backing data structure for MoDX.
import csv
import pydash

class tazManager():
    _instance = None
    _base = r'./csv/'
    _csv_fn = 'taz_info.csv'
    _fq_csv_fn = _base + _csv_fn
    _taz_table = []
    
    def __init__(self):
        # print('Creating the tazManager object.')
        with open(self._fq_csv_fn, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                new = {}
                new['id'] = int(row['id'])
                new['taz'] = int(row['taz'])
                new['type'] = int(row['type'])
                new['town'] = row['town']
                new['state'] = row['state']
                new['town_state'] = row['town_state']
                new['in_mpo'] = int(row['in_mpo'])
                new['subregion'] = row['subregion']
                self._taz_table.append(new)
            # end_for
        # end_with
        # print('Length of _taz_table is ' + str(len(self._taz_table)))
        return self._instance
    # end_def __init__()
    
    # For debugging during development:
    def _get_tt_item(self, index):
        return self._taz_table[index]

    def mpo_tazes(self):
        retval = retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_mpo'] == 1)
        return retval

    def mpo_town_to_tazes(self, mpo_town):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['in_mpo'] == 1 and x['town'] == mpo_town)
        return retval

    def mpo_subregion_to_tazes(self, mpo_subregion):
        # We have to be careful as some towns are in two subregions,
        # and for these the 'subregion' field of the table contains
        # an entry of the form 'SUBREGION_1/SUBREGION_2'.
        retval = []
        if subregion == 'ICC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('ICC') != -1)
        elif subregion == 'TRIC':
            retval = pydash.collections.filter_(self._taz_table, 
                                                lambda x: x['subregion'].find('TRIC') != -1)
        elif subregion == 'SWAP':
            retval = pydash.collections.filter_(self.taz_table,
                                                lambda x: x['subregion'].find('SWAP') != -1)
        else:
            retval = pydash.collections.filter_(self._taz_table, lambda x: x['subregion'] == mpo_subregion)
        # end_if
        return retval
    # def_def mpo_subregion_to_tazes()
    
    # Note: Returns TAZes in town _regardless_ of state.
    def town_to_tazes(self, town):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['town'] == town)
        return retval

    def town_state_to_tazes(self, town, state):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state and x['town'] == town)
        return retval

    def state_to_tazes(self, state):
        retval = pydash.collections.filter_(self._taz_table, lambda x: x['state'] == state)
        return retval
# end_class tazManager
