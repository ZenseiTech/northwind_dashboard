
import { w2sidebar, w2grid } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { product_details } from './products.js'
import { orderdetails, orders } from './orders.js'
import { customers } from './customers.js'
import { layout, layout2 } from './layout.js'

let pstyle = 'border: 1px solid #dfdfdf; padding: 5px; font-size:11px;';
let grid_style = 'font-size:16px;color:black';


let config = {
    sidebar: {
        name: 'sidebar',
        flatButton: false,
        nodes: [
            {
                id: 'general', text: 'General', group: true, expanded: true, nodes: [
                    { id: 'customers_grid', text: 'Customers', icon: 'icon-address-book' },
                    { id: 'product_details_grid', text: 'Product Details', icon: "icon-table", selected: true },
                    { id: 'orders_grid', text: 'Orders', icon: 'icon-office' },
                ]
            }
        ],
        onFlat: function (event) {
            $('#sidebar').css('width', (event.goFlat ? '25px' : '200px'));
        },
        onClick: function (event) {
            switch (event.target) {
                case 'customers_grid':
                    layout2.html('top', customers)
                    break;
                case 'orders_grid':
                    layout2.html('top', orders)
                    break;
                case 'product_details_grid':
                    layout2.html('top', product_details)
                    break;
            }
        }
    },
};

let sidebar = new w2sidebar(config.sidebar)

// initialization
layout.render('#main')
layout.html('left', sidebar)
layout.html('main', layout2)
layout2.html('top', product_details)
layout2.html('main', orderdetails)
