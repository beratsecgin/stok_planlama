from odoo import fields, models, api


class StokPlanlamaRaporu(models.Model):
    _name = "stok.planlama.raporu"
    _description = "Stok Planlama Raporu"
    _auto = False
    _order = 'tarih desc, brut_kar desc'

   
    tarih = fields.Datetime('Tarih', readonly=True)
    depo_id = fields.Many2one('stock.warehouse', string='Depo', readonly=True)
    sezon = fields.Many2one('product.template', string='Sezon', readonly=True)
    cinsiyet = fields.Many2one('product.template', string='Cinsiyet', readonly=True)
    urun_grubu = fields.Many2one('product.template', string='Ürün Grubu', readonly=True)
    urun_tipi = fields.Many2one('product.template', string='Ürün Tipi', readonly=True)
    ic_referans = fields.Char(string='İç Referans', readonly=True)
    urun_adi = fields.Char(string='Ürün Adı', readonly=True)
    varyant_ic_referans = fields.Char(string='Varyant İç Referans', readonly=True)
    urun_renk = fields.Char(string='Ürün Renk', readonly=True)
    renk = fields.Char(string='Renk', readonly=True)
    numara_beden = fields.Char(string='Numara/Beden', readonly=True)
    envanter = fields.Float(string='Envanter', readonly=True)
    brut_satis_vd = fields.Float(string='Brüt Satış (VD)', readonly=True)
    satis_iadesi_vd = fields.Float(string='Satış İadesi (VD)', readonly=True)
    net_satis_vd = fields.Float(string='Net Satış (VD)', readonly=True)
    envanter_maliyet_tl = fields.Float(string='Envanter Maliyet TL', readonly=True)
    envanter_ort_satis_tl = fields.Float(string='Envanter Ort. Satış TL', readonly=True)
    satis_miktari = fields.Float(string='Satış Miktarı', readonly=True)
    iade_miktari = fields.Float(string='İade Miktarı', readonly=True)
    net_miktar = fields.Float(string='Net Miktar', readonly=True)
    satis_fiyati = fields.Float(string='Satış Fiyatı', readonly=True)
    smm = fields.Float(string='SMM', readonly=True)
    brut_kar = fields.Float(string='Brüt Kâr (TL)', readonly=True)
    brut_kar_yuzde = fields.Float(string='Brüt Kâr (%)', readonly=True)
    indirim_orani = fields.Float(string='İndirim Oranı (%)', readonly=True)
    mark_up = fields.Float(string='Mark-Up', readonly=True)
    cover = fields.Float(string='Cover', readonly=True)
    str_orani = fields.Float(string='STR (%)', readonly=True)
    gmroi = fields.Float(string='GMROI', readonly=True)
    raf_omru = fields.Integer(string='Raf Ömrü', readonly=True)
    urun_yasi = fields.Integer(string='Ürün Yaşı (Yıl)', readonly=True)
    kalite_segmenti = fields.Many2one('product.template', string='Kalite Segmenti', readonly=True)
    zaman_segmenti = fields.Many2one('product.template', string='Zaman Segmenti', readonly=True)
    yas_segmenti = fields.Many2one('product.template', string='Yaş Segmenti', readonly=True)
    satis_durumu = fields.Char(string='Satış Durumu', readonly=True)
    tedarikci = fields.Many2one('product.supplierinfo', string='Tedarikçi', readonly=True)
    ortalama_satis_fiyati = fields.Float(string='Ortalama Satış Fiyatı', readonly=True)
    rpt_durumu = fields.Integer(string='RPT Durumu', readonly=True)
    ilk_fiyattan_satis_orani = fields.Float(string='İlk Fiyattan Satış Oranı (%)', readonly=True)

    @property
    def _table_query(self):
        
        return '%s %s %s %s' % (self._select(), self._from(), self._where(), self._group_by())

    def _select(self):
        select_str = """
            SELECT
                sm.id AS id,
                sm.date AS tarih,
                sm.warehouse_id AS depo_id,
                pt.season_id AS sezon,
                pt.gender AS cinsiyet,
                pt.group_id AS urun_grubu,
                pt.type_id AS urun_tipi,
                pt.km_code AS ic_referans,
                pt.name AS urun_adi,
                pp.default_code AS varyant_ic_referans,
                pp.pcolor_name AS urun_renk,
                pp.vcolor_id AS renk,
                pp.vsize_id AS numara_beden,
                pp.qty_available AS envanter,
                sr.price_total AS brut_satis_vd,
                sr.price_total_neg AS satis_iadesi_vd,
                sr.price_total AS net_satis_vd,
                svl.value AS envanter_maliyet_tl,
                (pp.qty_available * sr.price_total / sr.product_uom_qty) AS envanter_ort_satis_tl,
                sr.product_uom_qty AS satis_miktari,
                sr.product_uom_qty_neg AS iade_miktari,
                sr.product_uom_qty AS net_miktar,
                pp.list_price AS satis_fiyati,
                pp.standard_price AS smm,
                (sr.price_total - pp.standard_price) AS brut_kar,
                ((sr.price_total - pp.standard_price) / sr.price_total) * 100 AS brut_kar_yuzde,
                ((pp.list_price - (sr.price_total / sr.product_uom_qty)) / pp.list_price) * 100 AS indirim_orani,
                ((sr.price_total - pp.standard_price) / pp.standard_price) * 100 AS mark_up,
                (pp.qty_available / sr.product_uom_qty) AS cover,
                (sr.product_uom_qty / (pp.qty_available + sr.product_uom_qty)) AS str_orani,
                ((sr.price_total / sr.product_uom_qty) - pp.standard_price) / ((pp.qty_available + pp.qty_available) / 2 * pp.standard_price) AS gmroi,
                DATE_PART('day', NOW() - sm.date) AS raf_omru,
                DATE_PART('year', NOW() - pt.create_date) AS urun_yasi,
                pt.quality_id AS kalite_segmenti,
                pt.time_id AS zaman_segmenti,
                pt.prage_id AS yas_segmenti,
                pt.psale_statu AS satis_durumu,
                ps.partner_id AS tedarikci,
                (sr.price_total / sr.product_uom_qty) AS ortalama_satis_fiyati,
                COUNT(po.order_id) AS rpt_durumu,
                CASE
                    WHEN pp.list_price = sr.price_total THEN (sr.product_uom_qty / SUM(sr.product_uom_qty)) * 100
                    ELSE 0
                END AS ilk_fiyattan_satis_orani
        """
        return select_str

    def _from(self):
        from_str = """
            FROM
                stock sm,
                product_product pp,
                product_template pt,
                stock_valuation_layer svl,
                sale_report sr,
                purchase_report po,
                product_supplierinfo ps
            WHERE
                sm.product_id = pp.id
                AND pp.product_tmpl_id = pt.id
                AND pp.id = svl.product_id
                AND sr.product_id = pp.id
                AND po.product_id = pp.id
                AND ps.product_tmpl_id = pt.id
        """
        return from_str

    def _where(self):
        return """
            WHERE
                sm.state = 'done'
        """

    def _group_by(self):
        group_by_str = """
            GROUP BY
                sm.date,
                sm.warehouse_id,
                pt.season_id,
                pt.gender,
                pt.group_id,
                pt.type_id,
                pt.km_code,
                pt.name,
                pp.default_code,
                pp.pcolor_name,
                pp.vcolor_id,
                pp.vsize_id,
                pp.qty_available,
                sr.price_total,
                sr.price_total_neg,
                sr.product_uom_qty,
                pp.list_price,
                pp.standard_price,
                svl.value,
                pt.quality_id,
                pt.time_id,
                pt.prage_id,
                pt.psale_statu,
                ps.partner_id,
                po.order_id
        """
        return group_by_str
