# -*- coding: utf-8 -*-

import logging
from os import path

import textract
from odoo import _, api, fields, models
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class Document(models.Model):

    _name = 'tmc.document'
    _inherit = 'tmc.document'

    indexed_content = fields.Text(
        readonly=True
    )

    pdf_url = fields.Char(
        compute='_get_pdf_url',
        readonly=True
    )

    def _get_path_and_url(self):
        try:
            repository_path = self.env['ir.config_parameter'].get_param(
                'tmc.document.repository_path')
            repository_url = self.env['ir.config_parameter'].get_param(
                'tmc.document.repository_url')
            file_name = str(self.number).zfill(6) + '.pdf'
            return {
                'file_path': repository_path + file_name,
                'url': repository_url + repository_path + file_name
            }
        except Exception:
            return None

    @api.one
    @api.depends('document_type_id',
                 'dependence_id',
                 'number',
                 'period')
    def _get_pdf_url(self):
        res = self._get_path_and_url()
        if res and path.isfile(res['file_path']):
            self.pdf_url = res['url']

    def _get_pdf_ocr(self, file_path):
        return textract.process(file_path,
                                method='tesseract',
                                language='spa')

    @api.one
    @api.depends('pdf_url')
    def search_and_index_pdf(self):
        res = self._get_path_and_url()
        force_ocr = self.env.context['force_ocr']
        if res and self.pdf_url:
            text = None
            if not self.indexed_content or force_ocr:
                try:
                    text = textract.process(res['file_path'])
                    if not text or force_ocr:
                        text = self._get_pdf_ocr(
                            file_path=res['file_path'])
                except Exception:
                    raise UserError(
                        _('Error processing OCR for document.'))
                finally:
                    self.indexed_content = text.replace(
                        '\n', ' ').replace('\r', '')

    @api.multi
    def open_pdf(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': self.pdf_url,
            'target': 'new',
        }
