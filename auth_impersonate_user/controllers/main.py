import logging

from odoo import http
from odoo.http import request
from odoo.http import session as http_session

from odoo.addons.web.controllers.home import Home

_logger = logging.getLogger(__name__)


# class ImpersonateHome(Home):
#     @http.route("/web/impersonate", type="http", auth="user", sitemap=False)
#     def impersonate_user(self, **kw):
#         uid = request.env.user.id
#         if request.env.user.can_impersonate_user:
#             _logger.info("User <%s> impersonates user <%s>.", uid, int(request.params["uid"]))

#             # Backup original session info
#             request.session["impersonator_uid"] = request.session.uid
#             request.session["impersonator_login"] = request.session.uid

#             # Set new session info
#             uid = request.session.uid = int(request.params["uid"])
#             request.env["res.users"]._invalidate_cache()
#             request.session.session_token = http_session.update_session_token(request.session, request.env)

#         return request.redirect(self._login_redirect(uid))

#     @http.route("/web/session/logout", type="http", auth="none")
#     def logout(self, redirect="/web"):
#         # Exit impersonation first
#         if request.session.get("impersonator_uid"):
#             _logger.info(
#                 "User <%s> exits impersonation of user <%s>.",
#                 request.session.get("impersonator_uid"),
#                 request.session.uid,
#             )

#             # Restore session info
#             request.session.uid = request.session.get("impersonator_uid")
#             request.session.login = request.session.get("impersonator_login")
#             del request.session["impersonator_uid"]
#             del request.session["impersonator_login"]
#             request.env.registry.clear_cache()
#             request.session.session_token = http_session.update_session_token(request.session, request.env)
#             return request.redirect(self._login_redirect(request.session.uid))
#         request.session.logout(keep_db=True)
#         return request.redirect(redirect, 303)


class ImpersonateHome(Home):
    @http.route("/web/impersonate", type="http", auth="user", sitemap=False)
    def impersonate_user(self, **kw):
        uid = request.env.user.id
        if request.env.user.can_impersonate_user:
            target = request.env["res.users"].sudo().browse(int(kw.get("uid", 0))).exists()
            if not target or not target.can_be_impersonated:
                return request.redirect(self._login_redirect(uid))

            _logger.info("User <%s> impersonates user <%s>.", uid, target.id)

            # Backup original session info
            request.session["impersonator_uid"] = request.session.uid
            request.session["impersonator_login"] = request.session.login

            # Set new session info
            request.session.uid = uid = target.id
            request.session.login = target.login
            request.session.context = dict(target.with_user(target).context_get())
            http_session.update_session_token(request.session, request.env)  # method has no return
            request.session.should_rotate = True

        return request.redirect(self._login_redirect(uid))

    @http.route("/web/session/logout", type="http", auth="none")
    def logout(self, redirect="/web"):
        if request.session.get("impersonator_uid"):
            _logger.info(
                "User <%s> exits impersonation of user <%s>.",
                request.session["impersonator_uid"],
                request.session.uid,
            )
            request.session.uid = request.session.pop("impersonator_uid")
            request.session.login = request.session.pop("impersonator_login")
            user = request.env["res.users"].sudo().browse(request.session.uid)
            request.session.context = dict(user.with_user(user).context_get())
            http_session.update_session_token(request.session, request.env)
            request.session.should_rotate = True
            return request.redirect(self._login_redirect(request.session.uid))

        http_session.logout(request.session, keep_db=True)
        return request.redirect(redirect, 303)
