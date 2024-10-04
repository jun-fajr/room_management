from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PemesananRuangan(models.Model):
    _name = 'pemesanan.ruangan'
    _description = 'Pemesanan Ruangan'
    _order = 'tanggal_pemesanan desc'

    name = fields.Char(string='Nomor Pemesanan', required=True, copy=False, readonly=True, index=True, default=lambda self: 'New')
    ruangan_id = fields.Many2one('master.ruangan', string='Ruangan', required=True)
    nama_pemesanan = fields.Char(string='Nama Pemesanan', required=True)
    tanggal_pemesanan = fields.Date(string='Tanggal Pemesanan', required=True)
    status_pemesanan = fields.Selection([
        ('draft', 'Draft'),
        ('on_going', 'On Going'),
        ('done', 'Done')
    ], string='Status Pemesanan', default='draft', required=True)
    catatan_pemesanan = fields.Text(string='Catatan Pemesanan')

    _sql_constraints = [
        ('nama_pemesanan_unique', 'unique(nama_pemesanan)', 'Nama Pemesanan tidak boleh sama!'),
    ]

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pemesanan.ruangan') or 'New'
        return super(PemesananRuangan, self).create(vals)
    
    @api.constrains('ruangan_id', 'tanggal_pemesanan')
    def _check_pemesanan(self):
        for record in self:
            existing_pemesanans = self.search([
                ('ruangan_id', '=', record.ruangan_id.id),
                ('tanggal_pemesanan', '=', record.tanggal_pemesanan),
                ('id', '!=', record.id)
            ])
            if existing_pemesanans:
                raise ValidationError('Ruangan ini sudah dipesan pada tanggal yang sama.')

    def action_proses_pemesanan(self):
        for record in self:
            if record.status_pemesanan == 'draft':
                record.status_pemesanan = 'on_going'
            elif record.status_pemesanan == 'on_going':
                record.status_pemesanan = 'done'
