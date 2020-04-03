#!/usr/bin/python

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils.common.collections import is_sequence

class FilterModule(object):
    def filters(self):
        return {
            'list2list_of_dicts': self.list_of_items_to_list_of_dict_with_same_key
        }

    def list_of_items_to_list_of_dict_with_same_key(self, mylist, key_name='key'):
        """ Convert flat list to list of dicts with fixed key name
            For example:
            input list: list2list_of_dicts(['user1', 'user2'], key_name='username')
            output: [{'username': 'user1'}, {'username': 'user2'}]
        """
        if not is_sequence(mylist):
            raise AnsibleFilterError("list2list_of_dicts requires a list, got {} instead.".format(type(mylist)))

        return list({key_name: item} for item in mylist)
    