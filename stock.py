# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import date, datetime
from dateutil import relativedelta
import json
import time

from openerp.osv import fields, osv
from openerp.tools.float_utils import float_compare, float_round
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT
from openerp.exceptions import Warning
from openerp import SUPERUSER_ID, api
import openerp.addons.decimal_precision as dp
from openerp.addons.procurement import procurement
import logging


_logger = logging.getLogger(__name__)

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    def _get_kode_barang(self, cr, uid, ids, name, arg, context=None):
        sale_obj=self.pool.get("sale.order")
        res = {}
        #import pdb;pdb.set_trace()
        for x in self.browse(cr, uid, ids):
            origin=x.origin
            so_exist=sale_obj.search(cr, uid, [("name","=",origin)])
            if so_exist:
                so_browse=sale_obj.browse(cr,uid,so_exist[0])
                so_kode_barang=so_browse.kode_barang
                res[x.id]=so_kode_barang
        return res

        
    _columns = {
        'kode_barang': fields.char('Kode Barang', required=False,), 
        'kode_barang2':fields.function(_get_kode_barang,type="char",string="Kode Barang")
        }
