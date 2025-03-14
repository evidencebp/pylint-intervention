# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2014-2015 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emmanuel Mathier, Loic Hausammann <loic_hausammann@hotmail.com>
#
#    The licence is in the file __openerp__.py
#
##############################################################################
"""
This module reads a zip file containing scans of mail and finds the relation
between the database and the mail.
"""
import logging
import base64
import zipfile

from io import BytesIO
from ..tools import import_letter_functions as func
from openerp import api, fields, models, _, exceptions

from openerp.addons.connector.queue.job import job, related_action
from openerp.addons.connector.session import ConnectorSession

logger = logging.getLogger(__name__)


class ImportLettersHistory(models.Model):
    """
    Keep history of imported letters.
    This class allows the user to import some letters (individually or in a
    zip file) in the database by doing an automatic analysis.
    The code is reading QR codes in order to detect child and partner codes
    for every letter, using the zxing library for code detection.
    """
    _name = "import.letters.history"
    _inherit = 'import.letter.config'
    _description = _("""History of the letters imported from a zip
    or a PDF/TIFF""")
    _order = "create_date desc"

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################

    state = fields.Selection([
        ("draft", _("Draft")),
        ("pending", _("Analyzing")),
        ("open", _("Open")),
        ("ready", _("Ready")),
        ("done", _("Done"))], compute="_compute_state", store=True)
    import_completed = fields.Boolean()
    nber_letters = fields.Integer(
        'Number of letters', readonly=True, compute="_count_nber_letters")
    data = fields.Many2many('ir.attachment', string="Add a file")
    import_line_ids = fields.One2many(
        'import.letter.line', 'import_id', 'Files to process',
        ondelete='cascade')
    letters_ids = fields.One2many(
        'correspondence', 'import_id', 'Imported letters',
        readonly=True)
    config_id = fields.Many2one(
        'import.letter.config', 'Import settings')

    ##########################################################################
    #                             FIELDS METHODS                             #
    ##########################################################################
    @api.multi
    @api.depends("import_line_ids", "import_line_ids.status",
                 "letters_ids", "data", "import_completed")
    def _compute_state(self):
        """ Check in which state self is by counting the number of elements in
        each Many2many
        """
        for import_letters in self:
            if import_letters.letters_ids:
                import_letters.state = "done"
            elif import_letters.import_completed:
                check = True
                for i in import_letters.import_line_ids:
                    if i.status != "ok":
                        check = False
                if check:
                    import_letters.state = "ready"
                else:
                    import_letters.state = "open"
            elif import_letters.import_line_ids:
                import_letters.state = "pending"
            else:
                import_letters.state = "draft"

    @api.one
    @api.onchange("data")
    def _count_nber_letters(self):
        """
        Counts the number of scans. If a zip file is given, the number of
        scans inside is counted.
        """
        self.ensure_one()

        if self.state in ("open", "pending", "ready"):
            self.nber_letters = len(self.import_line_ids)
        elif self.state == "done":
            self.nber_letters = len(self.letters_ids)
        elif self.state is False or self.state == "draft":
            # counter
            tmp = 0
            # loop over all the attachments
            for attachment in self.data:
                # pdf or tiff case
                if func.check_file(attachment.name) == 1:
                    tmp += 1
                # zip case
                elif func.isZIP(attachment.name):
                    # create a tempfile and read it
                    zip_file = BytesIO(base64.b64decode(
                        attachment.with_context(bin_size=False).datas))
                    # catch ALL the exceptions that can be raised
                    # by class zipfile
                    try:
                        zip_ = zipfile.ZipFile(zip_file, 'r')
                        list_file = zip_.namelist()
                        # loop over all files in zip
                        for tmp_file in list_file:
                            tmp += (func.check_file(tmp_file) == 1)
                    except zipfile.BadZipfile:
                        raise exceptions.Warning(
                            _('Zip file corrupted (' +
                              attachment.name + ')'))
                    except zipfile.LargeZipFile:
                        raise exceptions.Warning(
                            _('Zip64 is not supported(' +
                              attachment.name + ')'))

            self.nber_letters = tmp
        else:
            raise exceptions.Warning(
                _("State: '{}' not implemented".format(self.state)))

    ##########################################################################
    #                             VIEW CALLBACKS                             #
    ##########################################################################
    @api.multi
    def button_import(self):
        """
        Analyze the attachment in order to create the letter's lines
        """
        for letters_import in self:
            if letters_import.data:
                letters_import.state = 'pending'
                if self.env.context.get('async_mode', True):
                    session = ConnectorSession.from_env(self.env)
                    import_letters_job.delay(
                        session, self._name, letters_import.id)
                else:
                    letters_import._run_analyze()
        return True

    @api.multi
    def button_save(self):
        """
        save the import_line as a correspondence
        """
        # check if all the imports are OK
        for letters_h in self:
            if letters_h.state != "ready":
                raise exceptions.Warning(_("Some letters are not ready"))
        # save the imports
        for letters in self:
            ids = letters.import_line_ids.get_letter_data()
            # letters_ids should be empty before this line
            letters.write({'letters_ids': ids})
            letters.mapped('import_line_ids.letter_image').unlink()
            letters.import_line_ids.unlink()
        return True

    @api.multi
    def button_review(self):
        """ Returns a form view for import lines in order to browse them """
        self.ensure_one()
        return {
            'name': _('Review Imports'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'import.letters.review',
            'context': self.with_context(
                line_ids=self.import_line_ids.ids).env.context,
            'target': 'current',
        }

    @api.onchange('config_id')
    @api.one
    def onchange_config(self):
        config = self.config_id
        if config:
            for field, val in config.get_correspondence_metadata().iteritems():
                setattr(self, field, val)

    ##########################################################################
    #                             PRIVATE METHODS                            #
    ##########################################################################
    def _run_analyze(self):
        """
        Analyze each attachment:
        - check for duplicate file names and skip them
        - decompress zip file if necessary
        - call _analyze_attachment for every resulting file
        """
        self.ensure_one()
        # keep track of file names to detect duplicates
        file_name_history = []
        logger.info("Imported letters analysis started...")
        progress = 1
        for attachment in self.data:
            if attachment.name not in file_name_history:
                file_name_history.append(attachment.name)
                file_data = base64.b64decode(attachment.with_context(
                    bin_size=False).datas)
                # check for zip
                if func.check_file(attachment.name) == 2:
                    zip_file = BytesIO(file_data)
                    zip_ = zipfile.ZipFile(zip_file, 'r')
                    for f in zip_.namelist():
                        logger.info(
                            "Analyzing letter {}/{}".format(
                                progress, self.nber_letters))
                        self._analyze_attachment(zip_.read(f), f, True)
                        progress += 1
                # case with normal format (PDF,TIFF)
                elif func.check_file(attachment.name) == 1:
                    logger.info("Analyzing letter {}/{}".format(
                        progress, self.nber_letters))
                    self._analyze_attachment(file_data, attachment.name)
                    progress += 1
                else:
                    raise exceptions.Warning(
                        'Only zip/pdf/tiff files are supported.')
            else:
                raise exceptions.Warning(_('Two files are the same'))

        # remove all the files (now they are inside import_line_ids)
        self.data.unlink()
        self.import_completed = True
        logger.info("Imported letters analysis completed.")

    def _analyze_attachment(self, file_data, file_name, is_zipfile=False):
        line_vals, document_vals = func.analyze_attachment(
            self.env, file_data, file_name, self.template_id)
        for i in xrange(0, len(line_vals)):
            line_vals[i]['import_id'] = self.id
            letters_line = self.env['import.letter.line'].create(line_vals[i])
            document_vals[i].update({
                'res_id': letters_line.id,
                'res_model': 'import.letter.line'
            })
            letters_line.letter_image = self.env['ir.attachment'].create(
                document_vals[i])
            # self.import_line_ids += letters_line


##############################################################################
#                            CONNECTOR METHODS                               #
##############################################################################
def related_action_imports(session, job):
    import_model = job.args[1]
    import_id = job.args[2]
    action = {
        'type': 'ir.actions.act_window',
        'res_model': import_model,
        'view_type': 'form',
        'view_mode': 'form',
        'res_id': import_id,
    }
    return action


@job(default_channel='root.sbc_compassion')
@related_action(action=related_action_imports)
def import_letters_job(session, model_name, import_id):
    """Job for importing letters."""
    import_history = session.env[model_name].browse(import_id)
    import_history._run_analyze()
