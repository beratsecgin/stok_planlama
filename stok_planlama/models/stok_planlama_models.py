from odoo import models, fields, api

class SalesKPI(models.Model):
    _name = 'sales.kpi'
    _description = 'Sales KPI'

    tarih_araligi = fields.Date(string='Tarih Aralığı')
    urun_adi = fields.Char(string='Ürün Adı')
    cinsiyet = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female')
    ], string='Cinsiyet')
    urun_grubu = fields.Char(string='Ürün Grubu')
    urun_tipi = fields.Char(string='Ürün Tipi')
    satis_miktari = fields.Integer(string='Satış Miktarı')
    envanter_tl = fields.Float(string='Envanter TL')
    satis_yuzde = fields.Float(string='Satış %', compute='_compute_satis_yuzde', store=True)
    envanter_yuzde = fields.Float(string='Envanter TL %', compute='_compute_envanter_yuzde', store=True)
    brut_kar = fields.Float(string='Brüt Kar (TL)')
    indirim_orani = fields.Float(string='İndirim Oranı %')
    markup = fields.Float(string='Mark-Up')
    cover = fields.Float(string='Cover')
    str_orani = fields.Float(string='STR%')
    gmroi = fields.Float(string='GMROI')
    ilk_fiyattan_satis_orani = fields.Float(string='İlk Fiyattan Satış Oranı %')

    @api.depends('satis_miktari', 'envanter_tl')
    def _compute_satis_yuzde(self):
        for record in self:
            if record.satis_miktari and record.envanter_tl:
                record.satis_yuzde = (record.satis_miktari / record.envanter_tl) * 100
            else:
                record.satis_yuzde = 0

    @api.depends('envanter_tl')
    def _compute_envanter_yuzde(self):
        total_envanter = sum(self.envanter_tl for self in self.search([]))
        for record in self:
            record.envanter_yuzde = (record.envanter_tl / total_envanter) * 100 if total_envanter else 0
