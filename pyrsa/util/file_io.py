#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:59:29 2020

@author: heiko
"""

import h5py
import pickle
import numpy as np


def write_dict_hdf5(file, dictionary):
    """ writes a nested dictionary containing strings & arrays as data into 
    a hdf5 file

    Args:
        file: a filename or opened writable file
        dictionary(dict): the dict to be saved 

    """
    file = h5py.File(file, 'a')
    _write_to_group(file, dictionary)
    
    
def _write_to_group(group, dictionary):
    """ writes a dictionary to a hdf5 group, which can recurse"""
    for key in dictionary.keys():
        value = dictionary[key]
        if isinstance(value, str):
            group.attrs[key] = value
        elif isinstance(value, np.ndarray):
            if value.dtype == '<U2':
                group[key] = value.astype('S')
            else:
                group[key] = value
        elif isinstance(value, dict):
            subgroup = group.create_group(key)
            _write_to_group(subgroup, value)
        elif value is None:
            group[key] = h5py.Empty("f")
        else:
            group[key] = value


def read_dict_hdf5(file):
    """ reads a nested dictionary containing strings & arrays as data from 
    a hdf5 file

    Args:
        file: a filename or opened readable file

    Returns:
        dictionary(dict): the loaded dict

    """
    file = h5py.File(file, 'r')
    return _read_group(file)


def _read_group(group):
    """ reads a group from a hdf5 file into a dict, which allows recursion"""
    dictionary = {}
    for key in group.keys():
        if isinstance(group[key], h5py.Group):
            dictionary[key] = _read_group(group[key])
        elif group[key].shape is None:
            dictionary[key] = None
        else:
            dictionary[key] = np.array(group[key])
            if dictionary[key].dtype.type is np.string_:
                dictionary[key] = np.array(group[key]).astype('unicode')
            # if (len(dictionary[key].shape) == 1 
            #     and dictionary[key].shape[0] == 1):
            #     dictionary[key] = dictionary[key][0]
    for key in group.attrs.keys():
        dictionary[key] = group.attrs[key]
    return dictionary


def write_dict_pkl(file, dictionary):
    """ writes a nested dictionary containing strings & arrays as data into 
    a pickle file

    Args:
        file: a filename or opened writable file
        dictionary(dict): the dict to be saved 

    """
    if isinstance(file, str):
        file = open(file, 'wb')
    pickle.dump(dictionary, file, protocol=-1)


def read_dict_pkl(file):
    """ writes a nested dictionary containing strings & arrays as data into 
    a pickle file

    Args:
        file: a filename or opened readable file

    Returns:
        dictionary(dict): the loaded dict


    """
    if isinstance(file, str):
        file = open(file, 'rb')
    data = pickle.load(file)
    return data