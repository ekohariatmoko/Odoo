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

from datetime import datetime, timedelta
import time
from openerp import SUPERUSER_ID
from openerp.osv import fields, osv
from openerp.tools.translate import _
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT
import openerp.addons.decimal_precision as dp
from openerp import workflow
# Memanggil file yang dibuat
from openerp.addons.terbilang import terbilang #Nama folder addons.terbilang, nama file.py

class sale_order(osv.osv):
    _inherit = 'sale.order'

    def _sum_po_voucher(self, cr, uid, ids, name, arg, context=None):
        res = {}
        #import pdb;pdb.set_trace()
    # Menambahkan sum many2many PO & Vucher
        for x in self.browse(cr, uid, ids):
            total_po=0
    # Loping penjumlahan total PO 
            for po in x.po_ids:
                total_po += po.amount_total
    # Loping penjumlahan total voucher 
            total_voucher=0
            for voucher in x.move_ids:
                total_voucher += voucher.amount
    # Penjumlahan Total PO & Voucher
            total_po_voucher=total_po+total_voucher
            res[x.id]=total_po_voucher
        return res

    def _sum_total(self, cr, uid, ids, name, arg, context=None):
        res = {}
        #import pdb;pdb.set_trace()
    # Menambahkan sum many2many PO & Vucher
        for x in self.browse(cr, uid, ids):
    # Penjumlahan Total PO & Voucher
            sum_total=x.amount_total-x.sum_po_voucher
            res[x.id]=sum_total
        return res

    def _sum_total_percent(self, cr, uid, ids, name, arg, context=None):
        res = {}
       # import pdb;pdb.set_trace()
        # Menambahkan sum many2many PO & Vucher
        for x in self.browse(cr, uid, ids):

            # jika pembagi = 0 returnkan
            if x.amount_total == 0 :
                return res

    # Penjumlahan Total PO & Voucher
            sum_total_percent=(x.sum_total/x.amount_total)*100
            res[x.id]=sum_total_percent
        return res

    def _terbilang(self, cr, uid, ids, name, arg, context=None):
        res = {}
        #import pdb;pdb.set_trace()
    # Menambahkan sum many2many PO & Vucher
        for x in self.browse(cr, uid, ids):
    # Penjumlahan Total PO & Voucher
            hasil_terbilang=terbilang.terbilang(x.amount_total, "IDR", "id")#Memanggil file terbilang.py dan fungsinnya terbilang def
            res[x.id]=hasil_terbilang
        return res

    _columns = {
        'x_nasabah'         : fields.char('Debitur'),
        'x_alamat'          : fields.char('Alamat'),
        'x_sj'              : fields.char("Surat Jalan"),
        'x_tgl_order'       : fields.date("Tgl.Kwitansi"),
        'x_angg'            : fields.float("Anggaran"),
        'x_bank'            : fields.many2one("res.partner.bank", "Transfer/Bank"),
#Menambahkan many2many
        'po_ids'            : fields.many2many("purchase.order", "po_so_rel", "order_id", "purchase_id", "Pembelian"), 
#Penulisan Field Harus Dikurung Kurawal (Agar filed Fuction dapat di Sum= tambahkan store=True)
        'move_ids'          : fields.many2many("account.move", "move_so_rel", "order_id", "move_id", "Biaya"),
        'proj_ids'          : fields.many2many("project.task", "proj_so_rel", "order_id", "project_id", "Proses Pekerjaan"),
        'sum_po_voucher'    : fields.function(_sum_po_voucher,type="float",store=True,string="HPP"),
        'sum_total'         : fields.function(_sum_total,type="float",store=True,string="Profit"),
        'sum_total_percent' : fields.function(_sum_total_percent,type="float",store=True,string="Margin",group_operator="avg"),
        'terbilang'         : fields.function(_terbilang,type="text",string="Terbilang"),
        }
