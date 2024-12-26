
var pstyle = 'border: 1px solid #dfdfdf; padding: 5px; font-size:11px;';
var pstyle2 = 'border: 1px solid #dfdfdf; padding: 5px;  text-align: center;';
var grid_style = 'font-size:16px;color:black';

var countries = ['USA', 'Canada', 'France', 'Ireland', 'Belgium', 'Venezuela', 'Norway', 'UK', 'Spain', 'Switzerland', 'Argentina', 'Portugal', 'Austria', 'Germany', 'Brazil', 'Mexico', 'Finland', 'Italy', 'Denmark', 'Poland', 'Sweden'];

var regions = []

var cities = ['Aachen', 'Albuquerque', 'Anchorage', 'Barcelona', 'Barquisimeto', 'Bergamo', 'Berlin', 'Bern', 'Boise', 'Brandenburg', 'Bruxelles', 'Bräcke', 'Buenos Aires', 'Butte', 'Campinas', 'Caracas', 'Charleroi', 'Colchester', 'Cork', 'Cowes', 'Cunewalde', 'Elgin', 'Eugene', 'Frankfurt a.M.', 'Genève', 'Graz', 'Helsinki', 'I. de Margarita', 'Kirkland', 'Kobenhavn', 'Köln', 'Lander'];


const server_url = 'http://localhost:5000/api/v1';

function get_regions() {
    console.log("Calling regions ....")
    fetch(server_url + '/shipregions')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            regions = data;
        })
};


var config = {
    layout: {
        name: 'layout',
        padding: 0,
        panels: [
            { type: 'left', size: 150, resizable: true, style: pstyle, minSize: 50 },
            { type: 'main', minSize: 550, style: pstyle, overflow: 'hidden' }
        ]
    },
    sidebar: {
        name: 'sidebar',
        flatButton: false,
        nodes: [
            {
                id: 'general', text: 'General', group: true, expanded: true, nodes: [
                    { id: 'customers_grid', text: 'Customers', img: 'icon-page' },
                    { id: 'product_details_grid', text: 'Product Details', img: 'icon-page' },
                    { id: 'orders_grid', text: 'Orders', img: 'icon-page' },
                ]
            }
        ],
        onFlat: function (event) {
            $('#sidebar').css('width', (event.goFlat ? '25px' : '200px'));
        },
        onClick: function (event) {
            switch (event.target) {
                case 'customers_grid':
                    w2ui.layout.content('main', w2ui.customers);
                    break;
                case 'orders_grid':
                    w2ui.layout.content('main', w2ui.orders);
                    break;
                case 'product_details_grid':
                    w2ui.layout.content('main', w2ui.product_details);
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
            toolbarSave: true,
            toolbarAdd: true
        },
        toolbar: {
            items: [
                { type: 'break' },
                { type: 'button', id: 'cancel', caption: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', caption: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick: " + target);
                if (target === 'cancel') {
                    w2ui.customers.reload();
                } else if (target === 'excel') {

                }
            }
        },
        multiSearch: true,
        searches: [

        ],
        // reorderColumns: true,
        columns: [
            { field: 'companyName', caption: 'Company Name', size: '170px', searchable: true, sortable: true, info: true, frozen: true, editable: { type: 'text' } },
            { field: 'contactName', caption: 'Contact Name', size: '140px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'address', caption: 'Address', size: '160px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'city', caption: 'City', size: '110px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'contactTitle', caption: 'Contact Title', size: '120px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'country', caption: 'Country', size: '130px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'fax', caption: 'Fax', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'phone', caption: 'Phone', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'postalCode', caption: 'Postal Code', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'region', caption: 'Region', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } }
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
            toolbarSave: true,
            toolbarAdd: true
        },
        toolbar: {
            items: [
                { type: 'break' },
                { type: 'button', id: 'cancel', caption: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', caption: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick: " + target);
                if (target === 'cancel') {
                    w2ui.product_details.reload();
                } else if (target === 'excel') {

                }
            }
        },
        multiSearch: true,
        searches: [
            { field: 'unitPrice', caption: 'Unit Price', type: 'money' },
            { field: 'unitsInStock', caption: 'Units In Stock', type: 'int' },
            { field: 'unitsOnOrder', caption: 'Units In Order', type: 'int' },
            { field: 'reorderLevel', caption: 'Reorder Level', type: 'int' },
            { field: 'discontinued', caption: 'Discontinued', type: 'list', options: { items: ['Y', 'N'] } },
        ],
        // reorderColumns: true,
        columns: [
            { field: 'productName', caption: 'Product Name', size: '170px', searchable: true, sortable: true, info: true, frozen: true, editable: { type: 'text' } },
            { field: 'quantityPerUnit', caption: 'Qty Per Unit', size: '140px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'unitPrice', caption: 'Unit Price', size: '160px', searchable: true, sortable: true, render: 'money', editable: { type: 'money' } },
            { field: 'unitsInStock', caption: 'Units In Stock', size: '110px', searchable: true, sortable: true, render: 'int', editable: { type: 'int' } },
            { field: 'unitsOnOrder', caption: 'Units On Order', size: '120px', searchable: true, sortable: true, render: 'int', editable: { type: 'int' } },
            { field: 'reorderLevel', caption: 'Reorder Level', size: '130px', searchable: true, sortable: true, render: 'int', editable: { type: 'int' } },
            { field: 'discontinued', caption: 'Discontinued', size: '150px', searchable: true, sortable: true, editable: { type: 'checkbox', style: 'text-align: center' } },
            { field: 'categoryName', caption: 'Category Name', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'supplierName', caption: 'Supplier Name', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } },
            { field: 'supplierRegion', caption: 'Supplier Region', size: '150px', searchable: true, sortable: true, editable: { type: 'text' } }
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
        url: server_url + '/orderdetails',
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
                { type: 'button', id: 'cancel', caption: 'Cancel', icon: 'w2ui-icon-cross' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', caption: 'Excel', icon: 'w2ui-icon-plus' },
            ],
            onClick: function (target, data) {
                console.log("--- onClick: " + target);
                if (target === 'cancel') {
                    w2ui.orders.reload();
                } else if (target === 'w2ui-search-advanced') {
                    w2ui.orders.searches[5].options.items = regions
                } else if (target === 'excel') {

                }
            }
        },
        multiSearch: true,
        searches: [
            { field: 'orderDate', caption: 'Order Date', type: 'date' },
            { field: 'requiredDate', caption: 'Required Date', type: 'date' },
            { field: 'shippedDate', caption: 'Shipped Date', type: 'date' },
            { field: 'freight', caption: 'Freight', type: 'money' },
            { field: 'shipCountry', caption: 'Ship Country', type: 'list', options: { items: countries } },
            { field: 'shipRegion', caption: 'Ship Region', type: 'list', options: { items: regions } },
            { field: 'shipCity', caption: 'Ship City', type: 'list', options: { items: cities } },
        ],
        columns: [
            { field: 'customerId', caption: 'Customer Id', size: '80px', searchable: true, sortable: true, frozen: true },
            { field: 'customerName', caption: 'Customer Name', size: '160px', searchable: true, sortable: true, info: true, frozen: true },
            { field: 'employeeName', caption: 'Employee Name', size: '160px', searchable: true, sortable: true },
            { field: 'freight', caption: 'Freight', size: '110px', searchable: true, sortable: true, render: 'money' },
            { field: 'orderDate', caption: 'Order Date', size: '120px', searchable: true, sortable: true },
            { field: 'requiredDate', caption: 'Required Date', size: '130px', searchable: true, sortable: true },
            { field: 'shippedDate', caption: 'Ship Date', size: '150px', searchable: true, sortable: true },
            { field: 'shippedAddress', caption: 'Shipped Address', size: '150px', searchable: true, sortable: true },
            { field: 'shipCity', caption: 'Ship City', size: '150px', searchable: true, sortable: true },
            { field: 'shipCountry', caption: 'Ship Country', size: '150px', searchable: true, sortable: true },
            { field: 'shipperName', caption: 'Shipper Name', size: '150px', searchable: true, sortable: true },
            { field: 'shipPostalCode', caption: 'Ship Postal Code', size: '150px', searchable: true, sortable: true },
            { field: 'shipRegion', caption: 'Ship Region', size: '150px', searchable: true, sortable: true },
            { field: 'shipperName', caption: 'Shipper Name', size: '150px', searchable: true, sortable: true }
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

        },
        onClick(event) {
            console.log("On click...: " + event.recid);
        },
        onLoad: function (event) {
            console.log("Loading ...");
            event.onComplete = function () {
                console.log("onComplete Loading ...");
            }
        }
    },
};

$(function () {

    get_regions()

    // initialization
    // w2utils.settings.dataType = 'HTTP';
    w2utils.settings.dateFormat = 'yyyy-mm-dd';
    $('#main').w2layout(config.layout);
    w2ui.layout.content('left', $().w2sidebar(config.sidebar));

    // in memory initialization
    $().w2grid(config.customers);
    $().w2grid(config.product_details);
    $().w2grid(config.orders);

});
