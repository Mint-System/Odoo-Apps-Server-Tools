import logging

from odoo import http
from odoo.http import request
from odoo.service import security

from odoo.addons.web.controllers.main import Home

_logger = logging.getLogger(__name__)


class ImpersonateHome(Home):
    @http.route("/web/impersonate", type="http", auth="user", sitemap=False)
    def impersonate_user(self, **kw):
        uid = request.env.user.id
        if request.env.user.can_impersonate_user:
            # Backup original session info
            request.session.impersonator_uid = request.session.uid
            request.session.impersonator_login = request.session.login
             # Set new session info
            uid = request.session.uid = int(request.params["uid"])
            request.env["res.users"].clear_caches()
            request.session.session_token = security.compute_session_token(
                request.session, request.env
            )

        return http.local_redirect(self._login_redirect(uid))

    @http.route("/web/session/logout", type="http", auth="none")
    def logout(self, redirect="/web"):

        # Exit impersonation first
        if request.session.impersonator_uid:
            # Restore session info
            request.session.uid = request.session.impersonator_uid
            request.session.login = request.session.impersonator_login
            del request.session["impersonator_uid"]
            del request.session["impersonator_login"]
            request.env["res.users"].clear_caches()
            request.session.session_token = security.compute_session_token(
                request.session, request.env
            )

            return http.local_redirect(self._login_redirect(request.session.uid))

        request.session.logout(keep_db=True)
        return http.local_redirect(redirect)
