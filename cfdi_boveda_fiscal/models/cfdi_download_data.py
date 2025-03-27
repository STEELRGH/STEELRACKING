# -*- encoding: utf-8 -*-
from base64 import b64decode, b64encode
from zipfile import ZipFile
from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CfdiDownloadData(models.Model):
    _name = "cfdi.download.data"
    _description = "CFDI Download Data"
    _rec_name = 'uuid'

    request_id = fields.Many2one(comodel_name='cfdi.download.request', string="Solicitud", required=True, ondelete='cascade')
    pack_id = fields.Many2one(comodel_name='cfdi.download.pack', string="Paquete", required=True, ondelete='cascade')
    uuid = fields.Char(string="UUID", required=True)    
    filename = fields.Char(string="Archivo XML", required=True)    
    emisor = fields.Char(string="RFC emisor", required=True)
    rs_emisor = fields.Char(string="Razón social emisor", required=True)
    fecha = fields.Char(string="Fecha", required=True)
    tipo = fields.Char(string="Tipo", required=True)
    serie = fields.Char(string="Serie")
    folio = fields.Char(string="Folio")
    total = fields.Char(string="Total", required=True)
    conceptos = fields.Text(string="Conceptos")
    invoice_id = fields.Many2one(comodel_name='account.move', string="Factura")
    invoice_payment_state = fields.Selection(related='invoice_id.payment_state')
    company_id = fields.Many2one(comodel_name="res.company", string="Compañia", default=lambda self: self.env.company, copy=True)

    def view_invoice(self):
        """Retorna la acción para visualizar la factura creada."""
        action_id = self.env["ir.actions.actions"]._for_xml_id("account.action_move_in_invoice_type")
        action_id.update({'domain': "[('id', '=', %s)]" % str(self.invoice_id.id)})
        return action_id     

    def create_invoice(self):
        """Crea una factura a partir de los datos descargados del CFDI."""
        for rec in self:
            if rec.invoice_id:
                continue  # Si ya tiene factura, se omite.

            # Buscar o crear el partner
            partner_id = self.env['res.partner'].search([('name', '=', rec.rs_emisor)], limit=1)
            if not partner_id:
                partner_id = self.env['res.partner'].create({'name': rec.rs_emisor})

            # Crear la factura
            invoice_vals = {
                'partner_id': partner_id.id,
                'move_type': 'in_invoice',
                'state': 'draft',
                'invoice_date': rec.fecha.split('T')[0],
                'ref': rec.folio if rec.folio else 'SIN_FOLIO',  # Corrección aquí                
            }
            invoice_id = self.env['account.move'].create(invoice_vals)

            # Procesar los conceptos
            try:
                conceptos = eval(rec.conceptos)
            except Exception:
                raise UserError("Error al evaluar los conceptos del XML.")

            for c in conceptos:
                traslados = c.get('Traslados', [])
                tax_ids = []
                total_concepto = 0.0

                for traslado in traslados:
                    base = traslado.get('Base', '0')
                    importe = traslado.get('Importe', '0')
                    tasa_o_cuota = traslado.get('TasaOCuota', '0') or '0'  # Evita valores None o vacíos

                    try:
                        base = float(base)
                        importe = float(importe)
                        tasa_o_cuota = float(tasa_o_cuota)  # Convierte a float de forma segura
                    except ValueError:
                        base, importe, tasa_o_cuota = 0.0, 0.0, 0.0  # Valores por defecto si hay error
                        
                    total_concepto += base + importe

                    tax_id = self.env['account.tax'].search([
                        ('active', '=', True),
                        ('type_tax_use', '=', 'purchase'),
                        ('amount', '=', 100 * tasa_o_cuota)  # Multiplicamos por 100 solo si tasa_o_cuota es válido
                        #('amount', '=', 100 * float(traslado.get('TasaOCuota', 0)))
                    ], limit=1)

                    if not tax_id:
                        raise UserError(
                            "No se ha configurado el impuesto tipo {} con tasa {}".format(
                                traslado.get('Impuesto'),
                                traslado.get('TasaOCuota')
                            )
                        )

                    tax_ids.append((4, tax_id.id, 0))

                    tax_repartition_line_id = self.env['account.tax.repartition.line'].search([
                        ('tax_id', '=', tax_id.id),
                        ('company_id', '=', self.env.company.id),
                        ('repartition_type', '=', 'tax')
                    ], limit=1)

                    tax_line = {
                        'move_id': invoice_id.id,
                        'account_id': tax_id.cash_basis_transition_account_id.id,
                        'quantity': 1,
                        'name': tax_id.name,
                        'price_unit': importe,           
                        'debit': importe,
                        'tax_line_id': tax_id.id,
                        'tax_group_id': tax_id.tax_group_id.id,
                        'tax_base_amount': base,
                        'tax_repartition_line_id': tax_repartition_line_id.id if tax_repartition_line_id else False,
                    }
                    self.env['account.move.line'].with_context(check_move_validity=False).create(tax_line)

                valor_unitario = float(c.get('ValorUnitario', 0))
                if c.get('Descuento') not in (None, 'None'):
                    valor_unitario -= float(c.get('Descuento'))

                debit_line = {
                    'move_id': invoice_id.id,
                    'account_id': invoice_id.journal_id.default_account_id.id,
                    'quantity': float(c.get('Cantidad', 1)),
                    'price_unit': valor_unitario,
                    'debit': valor_unitario * float(c.get('Cantidad', 1)),
                    'name': c.get('Descripcion'),
                    'tax_ids': tax_ids if tax_ids else False
                }
                self.env['account.move.line'].with_context(check_move_validity=False).create(debit_line)

                credit_line = {
                    'move_id': invoice_id.id,
                    'account_id': invoice_id.partner_id.property_account_payable_id.id,
                    'quantity': float(c.get('Cantidad', 1)),
                    'credit': total_concepto,
                    'tax_ids': tax_ids if tax_ids else False
                }
                self.env['account.move.line'].with_context(check_move_validity=False).create(credit_line)

            # Adjuntar XML al registro de factura
            if rec.pack_id.id_paquete:
                zip_path = f'./{rec.pack_id.id_paquete}'
                with open(zip_path, "wb") as zip_file:
                    zip_file.write(b64decode(rec.pack_id.paquete_b64))

                with ZipFile(zip_path) as zf:
                    for file in zf.namelist():
                        if file.endswith('.xml') and file == rec.filename:
                            with zf.open(file) as f:
                                self.env['ir.attachment'].create({
                                    'name': file,
                                    'type': 'binary',
                                    'datas': b64encode(f.read()),
                                    'res_model': 'account.move',
                                    'res_id': invoice_id.id,
                                    'mimetype': 'application/xml'
                                })
                            break

            rec.invoice_id = invoice_id.id
        return True
