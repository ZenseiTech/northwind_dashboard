import { server_url } from '../scripts/server.js'
import { w2grid } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { layout2 } from '../scripts/layout.js'

let categories = []

let config_products = {
    product_details: {
        name: 'product_details',
        url: server_url + '/productdetails',
        header: 'Product Details',
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
                // { type: 'button', id: 'cancel', text: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', text: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick target: " + target);
                if (target === 'cancel') {
                    product_details.reload();
                } else if (target === 'excel') {
                    console.log("--- onClick Products excel: " + target);
                }
            }
        },
        multiSearch: true,
        searches: [
            { field: 'unitPrice', label: 'Unit Price', type: 'money' },
            { field: 'unitsInStock', label: 'Units In Stock', type: 'int' },
            { field: 'unitsOnOrder', label: 'Units In Order', type: 'int' },
            { field: 'reorderLevel', label: 'Reorder Level', type: 'int' },
            { field: 'discontinued', label: 'Discontinued', type: 'list', options: { items: ['Y', 'N'] } },
            { field: 'categoryName', label: 'Category Name', type: 'list', options: { items: categories } },
        ],
        // reorderColumns: true,
        columns: [
            { field: 'productName', text: 'Product Name', size: '170px', searchable: true, sortable: true, info: true, frozen: true },
            { field: 'quantityPerUnit', text: 'Qty Per Unit', size: '140px', searchable: true, sortable: true },
            { field: 'unitPrice', text: 'Unit Price', size: '160px', searchable: true, sortable: true, render: 'money' },
            { field: 'unitsInStock', text: 'Units In Stock', size: '110px', searchable: true, sortable: true, render: 'int' },
            { field: 'unitsOnOrder', text: 'Units On Order', size: '120px', searchable: true, sortable: true, render: 'int' },
            { field: 'reorderLevel', text: 'Reorder Level', size: '130px', searchable: true, sortable: true, render: 'int' },
            { field: 'discontinued', text: 'Discontinued', size: '150px', searchable: true, sortable: true },
            { field: 'categoryName', text: 'Category Name', size: '150px', searchable: true, sortable: true },
            { field: 'supplierName', text: 'Supplier Name', size: '150px', searchable: true, sortable: true },
            { field: 'supplierRegion', text: 'Supplier Region', size: '150px', searchable: true, sortable: true }
        ],
        onAdd: function (event) {
            console.log('-- Product onAdd--');
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
            console.log('Column is: ' + event.detail.column + ' and recid is: ' + event.detail.recid);
            event.onComplete = function () {
                openPopup();
            }
        },
        onKeydown: function (event) {

        },
        onLoad: function (event) {
            console.log("Loading products ...");
            product_details.searches[5].options.items = categories

            event.onComplete = function () {
                if (layout_layout2_panel_main.style.opacity === '1' || layout_layout2_panel_main.style.opacity === '') {
                    layout2.toggle('main', window.instant)
                }
            }
        },
    },
}

export let product_details = new w2grid(config_products.product_details)
