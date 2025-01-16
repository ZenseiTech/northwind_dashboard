
import { w2sidebar, w2grid } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { product_details, formProduct } from './products.js'
import { orderdetails, orders } from './orders.js'
import { server_url } from './server.js'
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
    customers: {
        name: 'customers',
        url: server_url + '/customers',
        header: 'Customers',
        // style: grid_style,
        limit: 500,
        show: {
            header: true,
            toolbar: true,
            footer: true,
            // toolbarSave: true,
            toolbarAdd: true
        },
        toolbar: {
            items: [
                { type: 'break' },
                { type: 'button', id: 'cancel', text: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', text: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick: " + target);
                if (target === 'cancel') {
                    customers.reload();
                } else if (target === 'excel') {

                }
            }
        },
        multiSearch: true,
        searches: [

        ],
        // reorderColumns: true,
        columns: [
            { field: 'companyName', text: 'Company Name', size: '170px', searchable: true, sortable: true, info: true, frozen: true, editable: { type: 'text' } },
            { field: 'contactName', text: 'Contact Name', size: '140px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'address', text: 'Address', size: '160px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'city', text: 'City', size: '110px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'contactTitle', text: 'Contact Title', size: '120px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'country', text: 'Country', size: '130px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'fax', text: 'Fax', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'phone', text: 'Phone', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'postalCode', text: 'Postal Code', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'region', text: 'Region', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } }
        ],
        onAdd: function (event) {

        },
        onRequest: function (event) {
            console.log('-- server call --');
            console.log(event);
        },
        onSave: function (event) {
            event.onComplete = function () {
                if (event.status === "success") {
                    console.log('---On save onComplete: ' + event.status);

                }
            }
        },
        onChange: function (event) {
            console.log(event);

        },
        onDblClick: function (event) {
            console.log('Column is: ' + event.column + ' and recid is: ' + event.recid);
            if (event.column === 0) {

            }
        },
        onKeydown: function (event) {

        }
    },
};

let sidebar = new w2sidebar(config.sidebar)
let customers = new w2grid(config.customers)

// initialization
layout.render('#main')
layout.html('left', sidebar)
layout.html('main', layout2)
layout2.html('top', product_details)
layout2.html('main', orderdetails)
