odoo.define('home_background_image.home', function (require) {
    "use strict"

    const session = require('web.session')

    document.addEventListener("DOMContentLoaded",function(){
        const url = session.url('/web/image', {
            id: session.company_id,
            model: 'res.company',
            field: 'background_image',
        })
    
        if (document && document.body && url) {
            document.body.style.backgroundImage = `url(${url})`
        }    
    })
})