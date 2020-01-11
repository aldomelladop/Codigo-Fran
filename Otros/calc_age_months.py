#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 18:24:21 2019

@author: aldo_mellado
"""
from datetime import datetime
from datetime import timedelta

def calc_age_months(from_date, to_date):
    from_date = datetime.strptime(from_date, "%Y-%m-%d")
    to_date = datetime.strptime(to_date, "%Y-%m-%d")

    age_in_months = (to_date.year- from_date.year )*12 + (to_date.month- from_date.month )

    if to_date.day < from_date.day:
        return age_in_months -1
    else:
        return age_in_months