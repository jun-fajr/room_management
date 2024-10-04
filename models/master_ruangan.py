from odoo import models, fields, api
from odoo.exceptions import ValidationError

class MasterRuangan(models.Model):
    _name = 'master.ruangan'
    _description = 'Master Ruangan'
    
    name = fields.Char(string='Nama Ruangan', required=True)
    tipe_ruangan = fields.Selection([
        ('small_meeting', 'Meeting Room Kecil'),
        ('large_meeting', 'Meeting Room Besar'),
        ('aula', 'Aula')
    ], string='Tipe Ruangan', required=True)
    
    lokasi_ruangan = fields.Selection([
        ('1a', '1A'),
        ('1b', '1B'),
        ('1c', '1C'),
        ('2a', '2A'),
        ('2b', '2B'),
        ('2c', '2C'),
    ], string='Lokasi Ruangan', required=True)
    
    foto_ruangan = fields.Binary(string='Foto Ruangan', required=True)
    kapasitas_ruangan = fields.Integer(string='Kapasitas Ruangan', required=True)
    keterangan = fields.Text(string='Keterangan')

    _sql_constraints = [
        ('name_unique', 'unique(name)', 'Nama Ruangan tidak boleh sama!'),
    ]
