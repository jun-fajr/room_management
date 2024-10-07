from odoo import http
from odoo.http import request, Response
import json
import logging

_logger = logging.getLogger(__name__)

class RuanganBookingController(http.Controller):

    # Token yang valid disimpan secara hardcoded, bisa juga disimpan di DB
    VALID_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MSwiZXhwIjoxNjM4NjY3MjAwfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'

    def _check_bearer_token(self, token):
        """Helper function to check if the Bearer token is valid"""
        return token == self.VALID_TOKEN

    @http.route('/api/pemesanan/<int:pemesanan_id>', type='http', auth='public', methods=['GET'], csrf=False)
    def track_pemesanan_status(self, pemesanan_id):
        # Cek header authorization untuk Bearer Token
        auth_header = request.httprequest.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response(json.dumps({
                'error': 'Missing or invalid Authorization header'
            }), status=401, mimetype='application/json')

        token = auth_header.split(" ")[1]
        if not self._check_bearer_token(token):
            return Response(json.dumps({
                'error': 'Invalid or expired token'
            }), status=403, mimetype='application/json')

        # Lanjutkan ke logika pemesanan jika token valid
        try:
            pemesanan = request.env['pemesanan.ruangan'].sudo().search([('id', '=', pemesanan_id)], limit=1)
            if not pemesanan:
                return Response(json.dumps({
                    'error': 'Pemesanan tidak ditemukan'
                }), status=404, mimetype='application/json')

            result = {
                'nomor_pemesanan': pemesanan.nomor_pemesanan,
                'ruangan': pemesanan.ruangan_id.name,
                'nama_pemesanan': pemesanan.nama_pemesanan,
                'tanggal_pemesanan': pemesanan.tanggal_pemesanan.strftime('%Y-%m-%d'),
                'status_pemesanan': pemesanan.status_pemesanan,
                'catatan_pemesanan': pemesanan.catatan_pemesanan or ''
            }
            return Response(json.dumps(result), status=200, mimetype='application/json')

        except Exception as e:
            _logger.error("Error tracking pemesanan: %s", str(e))  # Logging error
            return Response(json.dumps({
                'error': 'Terjadi kesalahan: %s' % str(e)
            }), status=500, mimetype='application/json')
