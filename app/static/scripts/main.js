
import { w2layout, w2sidebar, w2grid, query, w2form, w2popup } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { product_details } from '../scripts/products.js'
import { server_url } from '../scripts/server.js'
import { layout, layout2 } from '../scripts/layout.js'

let pstyle = 'border: 1px solid #dfdfdf; padding: 5px; font-size:11px;';
let grid_style = 'font-size:16px;color:black';

let countries = ['USA', 'Canada', 'France', 'Ireland', 'Belgium', 'Venezuela', 'Norway', 'UK', 'Spain', 'Switzerland', 'Argentina', 'Portugal', 'Austria', 'Germany', 'Brazil', 'Mexico', 'Finland', 'Italy', 'Denmark', 'Poland', 'Sweden'];

let regions = []

let categories = []

let suppliers = []

let cities = ['Aachen', 'Albuquerque', 'Anchorage', 'Barcelona', 'Barquisimeto', 'Bergamo', 'Berlin', 'Bern', 'Boise', 'Brandenburg', 'Bruxelles', 'Bräcke', 'Buenos Aires', 'Butte', 'Campinas', 'Caracas', 'Charleroi', 'Colchester', 'Cork', 'Cowes', 'Cunewalde', 'Elgin', 'Eugene', 'Frankfurt a.M.', 'Genève', 'Graz', 'Helsinki', 'I. de Margarita', 'Kirkland', 'Kobenhavn', 'Köln', 'Lander'];


function getOrderRecord(recid) {
    for (let i = 0; i < orders.records.length; ++i) {
        if (orders.records[i].recid === recid) {
            return orders.records[i]
        }
    }
    return [];
}


function getRegions() {
    console.log("Calling regions ....")
    fetch(server_url + '/shipregions')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            regions = data;
        })
};


function getCategories() {
    console.log("Calling categories ....")
    fetch(server_url + '/categories')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            categories = data;
        })
};

async function getOrderDetails(orderId) {
    fetch(server_url + '/orderdetails/' + orderId)
        .then((response) => {
            return response.json();
        }).then((data) => {
            return data;
        }).then((data) => {
            console.log(data)
            orderdetails.clear();
            orderdetails.add(data.records)
            if (layout_layout2_panel_main.style.opacity === '0') {
                layout2.toggle('main', window.instant)
            }
        })
}


let config = {
    layout: {
        name: 'layout',
        padding: 0,
        panels: [
            { type: 'left', size: 150, resizable: true, style: pstyle, minSize: 50 },
        ]
    },
    layout2: {
        name: 'layout2',
        padding: 6,
        panels: [
            { type: 'top', minSize: 650, resizable: true, style: pstyle, overflow: 'hidden' },
            { type: 'bottom', minSize: 120, resizable: true, style: pstyle, overflow: 'hidden' }
        ]
    },
    layoutProduct: {
        name: 'layoutProduct',
        padding: 0,
        panels: [
            { type: 'main', size: 150, resizable: true, style: pstyle, minSize: 50 },
        ]
    },
    sidebar: {
        name: 'sidebar',
        flatButton: false,
        nodes: [
            {
                id: 'general', text: 'General', group: true, expanded: true, nodes: [
                    { id: 'customers_grid', text: 'Customers', icon: 'fa fa-pencil-square-o' },
                    { id: 'product_details_grid', text: 'Product Details', icon: 'fa fa-pencil-square-o', selected: true },
                    { id: 'orders_grid', text: 'Orders', icon: 'fa fa-pencil-square-o' },
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
    orders: {
        name: 'orders',
        url: server_url + '/orders',
        header: 'Orders',
        // style: grid_style,
        limit: 500,
        show: {
            header: true,
            toolbar: true,
            footer: true,
            // toolbarSave: true,
            // toolbarAdd: true
        },
        toolbar: {
            items: [
                { type: 'break' },
                // { type: 'button', id: 'cancel', text: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', text: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick Orders: " + target);
                if (target === 'cancel') {
                    orders.reload();
                } else if (target === 'excel') {
                    console.log("onClick Excel " + target)
                }
            }
        },
        multiSearch: true,
        searches: [
            // { field: 'customerId', label: 'Customer Id', type: 'int' },
            { field: 'freight', label: 'Freight', type: 'money' },
            { field: 'shipCountry', label: 'Ship Country', type: 'list', options: { items: countries } },
            { field: 'shipRegion', label: 'Ship Region', type: 'list', options: { items: regions } },
            { field: 'shipCity', label: 'Ship City', type: 'list', options: { items: cities } },
            { field: 'orderDate', label: 'Order Date', type: 'date' },
            { field: 'requiredDate', label: 'Required Date', type: 'date' },
            { field: 'shippedDate', label: 'Shipped Date', type: 'date' },
        ],
        columns: [
            // { field: 'customerId', text: 'Customer Id', size: '80px', searchable: true, sortable: true, frozen: true },
            { field: 'customerName', text: 'Customer Name', size: '160px', searchable: true, sortable: true, info: true, frozen: true },
            { field: 'employeeName', text: 'Employee Name', size: '160px', searchable: true, sortable: true },
            { field: 'freight', text: 'Freight', size: '110px', searchable: true, sortable: true, render: 'money' },
            { field: 'orderDate', text: 'Order Date', size: '120px', searchable: true, sortable: true },
            { field: 'requiredDate', text: 'Required Date', size: '130px', searchable: true, sortable: true },
            { field: 'shippedDate', text: 'Ship Date', size: '150px', searchable: true, sortable: true },
            { field: 'shipAddress', text: 'Shipped Address', size: '150px', searchable: true, sortable: true },
            { field: 'shipCity', text: 'Ship City', size: '150px', searchable: true, sortable: true },
            { field: 'shipCountry', text: 'Ship Country', size: '150px', searchable: true, sortable: true },
            { field: 'shipperName', text: 'Shipper Name', size: '150px', searchable: true, sortable: true },
            { field: 'shipPostalCode', text: 'Ship Postal Code', size: '150px', searchable: true, sortable: true },
            { field: 'shipRegion', text: 'Ship Region', size: '150px', searchable: true, sortable: true },
            { field: 'shipperName', text: 'Shipper Name', size: '150px', searchable: true, sortable: true }
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
            console.log('Column is: ' + event.detail.column + ' and recid is: ' + event.detail.recid);
        },
        onKeydown: function (event) {

        },
        onClick(event) {
            event.onComplete = function () {
                const record = orders.records[this.getSelection(true)]
                console.log("Order onClick ... ")
                let recid = event.detail.recid
                getOrderDetails(recid);
            }
        },
        onLoad: function (event) {
            console.log("Loading orders ...");
            orders.searches[2].options.items = regions
            event.onComplete = function () {
                console.log("onComplete orders Loading ...");
                if (layout_layout2_panel_main.style.opacity === '1' || layout_layout2_panel_main.style.opacity === '') {
                    layout2.toggle('main', window.instant)
                }
            }
        }
    },
    orderdetails: {
        name: 'orderdetails',
        header: 'Order Details',
        limit: 500,
        show: {
            toolbar: true,
            toolbarSave: true,
            header: true,
            footer: true,
        },
        columns: [
            // { field: 'customerId', text: 'Customer Id', size: '80px', searchable: true, sortable: true, frozen: true },
            { field: 'productName', text: 'Product Name', size: '180px', searchable: true, sortable: true, info: true, frozen: true },
            { field: 'unitPrice', text: 'Unit Price', size: '160px', searchable: true, sortable: true, render: 'money', editable: { type: 'money' } },
            { field: 'quantity', text: 'Quantity', size: '110px', searchable: true, sortable: true, render: 'int', editable: { type: 'int', min: 0, max: 32756 } },
            { field: 'discount', text: 'Discount', size: '120px', searchable: true, sortable: true, render: 'money', editable: { type: 'money' } },
        ],
        onSave: function (event) {
            console.log("OrderDetails onSave... " + event.detail.changes);
        },
        onDblClick: function (event) {
            console.log("OrderDetails double click...: " + event.detail.recid);
            let record = getOrderRecord(event.detail.recid);
            if (typeof record.shippedDate !== 'undefined') {
                event.preventDefault();
            }

            event.onComplete = function () {
                const record = orders.records[this.getSelection(true)]
                console.log("Order Detail status ... " + record.orderStatus)
                let recid = event.detail.recid
            }
        },
    },
    productForm: {
        header: 'Edit Product',
        name: 'prooductForm',
        style: 'border: 1px solid #efefef',
        fields: [
            { field: 'recid', type: 'text', html: { label: 'ID', attr: 'size="10" readonly' } },
            { field: 'productName', type: 'text', required: true, html: { label: 'Product Name', attr: 'size="40" maxlength="64"' } },
            { field: 'quantityPerUnit', type: 'text', required: true, html: { label: 'Qty Per Unit', attr: 'size="40" maxlength="64"' } },
            { field: 'unitPrice', type: 'money', html: { label: 'Unit Price' } },
            { field: 'unitsInStock', type: 'int', html: { label: 'Units In Stock' } },
            { field: 'unitsOnOrder', type: 'int', html: { label: 'Units On Order' } },
            { field: 'reorderLevel', type: 'int', html: { label: 'Reorder Level' } },
            {
                field: 'discontinued', type: 'toggle', html: { label: 'Discontinued' }
            },
            {
                field: 'categoryName', type: 'list',
                html: { label: 'Category' },
                options: { items: categories }
            },
            {
                field: 'supplierName', type: 'list',
                html: { label: 'Supplier' },
                options: { items: suppliers }
            },
            {
                field: 'supplierRegion', type: 'list',
                html: { label: 'Supplier Region' },
                options: { items: regions }
            }
        ],
        actions: {
            reset() {
                formProduct.reload();
            },
            save() {
                let errors = this.validate()
                if (errors.length > 0) return
                formProduct.save();
            }
        }
    },
};

getRegions()
getCategories()

// let layout = new w2layout(config.layout)
// let layout2 = new w2layout(config.layout2)

let sidebar = new w2sidebar(config.sidebar)
let customers = new w2grid(config.customers)
// let product_details = new w2grid(config_products.product_details)
let orders = new w2grid(config.orders)
let orderdetails = new w2grid(config.orderdetails)
let formProduct = new w2form(config.productForm)

// initialization
layout.render('#main')
layout.html('left', sidebar)
layout.html('main', layout2)
layout2.html('top', product_details)
layout2.html('main', orderdetails)


let layoutProduct = new w2layout(config.layoutProduct)

window.openPopup = function () {
    formProduct.recid = product_details.getSelection()[0];
    formProduct.url = server_url + "/product"

    w2popup.open({
        // title: 'Popup',
        width: 600,
        height: 650,
        showMax: true,
        body: '<div id="main" style="position: absolute; left: 2px; right: 2px; top: 0px; bottom: 3px;"></div>'
    })
        .then(e => {
            layoutProduct.render('#w2ui-popup #main')
            formProduct.fields[8].options.items = categories
            formProduct.fields[9].options.items = suppliers
            formProduct.fields[10].options.items = regions
            layoutProduct.html('main', formProduct)
        })
    formProduct.reload();
}
