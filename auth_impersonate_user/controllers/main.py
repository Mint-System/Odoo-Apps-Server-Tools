import logging

from odoo import http
from odoo.http import request

from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


class ImpersonateHome(Home):
    @http.route(
        "/web/impersonate", type="http", auth="user", sitemap=False, readonly=True
    )
    def impersonate_user(self, **kw):
        uid = request.env.user.id
        if request.env.user.can_impersonate_user:
            target_uid = int(request.params["uid"])
            _logger.info("User <%s> impersonates user <%s>.", uid, target_uid)

            # Backup original session info
            request.session["impersonator_uid"] = request.session.uid
            request.session["impersonator_login"] = request.session.login

            # Switch session to the target user
            uid = request.session.uid = target_uid
            target_user = request.env["res.users"].sudo().browse(target_uid)
            request.session.login = target_user.login
            request.session.context = dict(
                request.env["res.users"].with_user(target_uid).context_get()
            )

            # Invalidate all ormcaches — _compute_session_token is keyed
            # by session id (not uid), so switching users requires a
            # fresh computation.
            request.env.registry.clear_cache()

            # Force a hard session rotation: generates a completely new
            # session ID and deletes the old session file.  This prevents
            # concurrent requests (bus polls, pending RPCs) that still
            # hold the old session data from overwriting the impersonated
            # session.  rotate() also recomputes session_token for the
            # new uid/sid automatically.
            request.session.should_rotate = True

        return request.redirect(self._login_redirect(uid))

    @http.route("/web/session/logout", type="http", auth="none", readonly=True)
    def logout(self, redirect="/odoo"):
        # Exit impersonation first
        if request.session.get("impersonator_uid"):
            _logger.info(
                "User <%s> exits impersonation of user <%s>.",
                request.session.get("impersonator_uid"),
                request.session.uid,
            )

            # Restore original session info
            original_uid = request.session.pop("impersonator_uid")
            original_login = request.session.pop("impersonator_login")

            request.session.uid = original_uid
            request.session.login = original_login
            request.session.context = dict(
                request.env["res.users"].sudo().with_user(original_uid).context_get()
            )

            request.env.registry.clear_cache()

            # Hard-rotate the session for the same reason as above:
            # isolate the restored admin session from any in-flight
            # requests that still reference the impersonated user's
            # session data.
            request.session.should_rotate = True
            return request.redirect(self._login_redirect(request.session.uid))
        request.session.logout(keep_db=True)
        return request.redirect(redirect, 303)
