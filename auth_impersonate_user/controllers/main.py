from odoo import http
from odoo.http import request
from odoo.service import security
from odoo.addons.web.controllers.main import Home
import logging
_logger = logging.getLogger(__name__)


class ImpersonateHome(Home):
    @http.route('/web/impersonate', type='http', auth='user', sitemap=False)
    def impersonate_user(self, **kw):
        uid = request.env.user.id
        if request.env.user.can_impersonate_user:
            uid = request.session.uid = int(request.params['uid'])
            request.env['res.users'].clear_caches()
            request.session.session_token = security.compute_session_token(request.session, request.env)

        return http.local_redirect(self._login_redirect(uid))