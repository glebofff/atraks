# -*- coding: utf-8 -*-
#
# Author: Stanislav Glebov <glebofff@gmail.com> 
# Created: 19/11/19

import re
import enum

from django.utils.functional import cached_property


class MSISDNError(Exception):
    pass


class MSISDNValidationError(MSISDNError):
    pass


class MSISDNCountry(enum.Enum):
    RU = '7'


class MSISDN(object):
    _MSG_INVALID_FORMAT = 'Invalid number format'
    _MSG_INVALID_NUMBER = 'Invalid number'
    _valid_re = re.compile("^([1-9])?[0-9]{10,14}$")

    def __init__(self, number):
        self._number = number

    @property
    def length(self):
        return len(self._number)

    @property
    def country(self):
        if self.length == 11 and self._number[0] == '7':
            return MSISDNCountry.RU
        return None

    @property
    def cc(self):
        if self.country is MSISDNCountry.RU:
            return self._number[0]

    @property
    def ndc(self):
        if self.country is MSISDNCountry.RU:
            return self._number[1:4]

    @property
    def sn(self):
        if self.country is MSISDNCountry.RU:
            return self._number[4:]

    @property
    def number(self):
        return f'{self.cc}{self.ndc}{self.sn}'

    @classmethod
    def validate(cls, number: str = None):
        if not isinstance(number, str):
            raise MSISDNValidationError(cls._MSG_INVALID_FORMAT)

        if not cls._valid_re.match(number):
            raise MSISDNValidationError(f"{cls._MSG_INVALID_NUMBER}: {number}")

        # TODO: number validation

        return True

    @property
    def plan_qs(self):
        from rs_plan.models import Plan
        return Plan.objects.filter(
            pfx__exact=self.ndc,
            beg__lte=self.sn,
            end__gte=self.sn
        )

    @property
    def plan(self):
        return self.plan_qs.first()

    @classmethod
    def parse(cls, number: str = None):
        cls.validate(number)

        n = cls(number)

        if not n.country:
            raise MSISDNValidationError('Non-russian numbers are not supported. Yet.')

        return n
