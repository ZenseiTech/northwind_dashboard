
import { w2grid, w2form, w2popup } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { server_url } from './server.js'
import { getRegions } from './common.js'
import { layout2, layoutOrder } from './layout.js'

let countries = ['USA', 'Canada', 'France', 'Ireland', 'Belgium', 'Venezuela', 'Norway', 'UK', 'Spain', 'Switzerland', 'Argentina', 'Portugal', 'Austria', 'Germany', 'Brazil', 'Mexico', 'Finland', 'Italy', 'Denmark', 'Poland', 'Sweden'];

let cities = ['Aachen', 'Albuquerque', 'Anchorage', 'Barcelona', 'Barquisimeto', 'Bergamo', 'Berlin', 'Bern', 'Boise', 'Brandenburg', 'Bruxelles', 'Bräcke', 'Buenos Aires', 'Butte', 'Campinas', 'Caracas', 'Charleroi', 'Colchester', 'Cork', 'Cowes', 'Cunewalde', 'Elgin', 'Eugene', 'Frankfurt a.M.', 'Genève', 'Graz', 'Helsinki', 'I. de Margarita', 'Kirkland', 'Kobenhavn', 'Köln', 'Lander'];

let regions = await getRegions()


function getOrderRecord(recid) {
    for (let i = 0; i < orders.records.length; ++i) {
        if (orders.records[i].recid === recid) {
            return orders.records[i]
        }
    }
    return [];
}


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


function openPopup() {
    formOrder.recid = orders.getSelection()[0];
    formOrder.url = server_url + "/order"

    w2popup.open({
        // title: 'Popup',
        width: 600,
        height: 650,
        showMax: true,
        body: '<div id="main" style="position: absolute; left: 2px; right: 2px; top: 0px; bottom: 3px;"></div>'
    })
        .then(e => {
            layoutOrder.render('#w2ui-popup #main')
            // formOrder.fields[8].options.items = categories
            // formOrder.fields[9].options.items = suppliers
            // formOrder.fields[10].options.items = regions
            layoutOrder.html('main', formOrder)
        })
    formOrder.reload();
}


let config = {
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
            { field: 'recid', text: 'Id', size: '80px', searchable: true, sortable: true, frozen: true },
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
            event.onComplete = function () {
                openPopup();
            }
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
            // toolbar: true,
            // toolbarSave: true,
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
    orderForm: {
        header: 'Edit Order',
        name: 'orderForm',
        style: 'border: 1px solid #efefef',
        fields: [

            { field: 'recid', type: 'text', html: { label: 'ID', attr: 'size="10" readonly' } },
            { field: 'customerName', type: 'text', required: true, html: { label: 'Customer Name', attr: 'size="40" maxlength="64"' } },
            { field: 'employeeName', type: 'text', required: true, html: { label: 'Employee Name', attr: 'size="40" maxlength="64"' } },
            { field: 'freight', type: 'money', required: true, html: { label: 'Freight', attr: 'size="40" maxlength="64"' } },
            { field: 'orderDate', type: 'date', required: true, html: { label: 'Order Date', attr: 'size="20" maxlength="40"' } },
            { field: 'requiredDate', type: 'date', required: false, html: { label: 'Required Date', attr: 'size="20" maxlength="40"' } },
            { field: 'shipperName', type: 'text', required: true, html: { label: 'Shipper Name', attr: 'size="40" maxlength="64"' } },
            { field: 'shippedDate', type: 'date', required: false, html: { label: 'Shipped Date', attr: 'size="20" maxlength="40"' } },
            { field: 'shipAddress', type: 'text', required: true, html: { label: 'Ship Address', attr: 'size="40" maxlength="64"' } },
            {
                field: 'shipCity', type: 'list',
                html: { label: 'Ship City' },
                options: { items: cities },
                required: true,
            },
            {
                field: 'shipCountry', type: 'list',
                html: { label: 'Ship Country' },
                options: { items: countries },
                required: true,
            },
            { field: 'shipPostalCode', type: 'text', required: true, html: { label: 'Ship Post Code', attr: 'size="40" maxlength="64"' } },
            {
                field: 'shipRegion', type: 'list',
                html: { label: 'Shipper Region' },
                options: { items: regions },
                required: true,
            },
        ],
        actions: {
            reset() {
                formOrder.reload();
            },
            save() {
                let errors = this.validate()
                if (errors.length > 0) return
                formOrder.save();
            }
        }
    },
}

export let orders = new w2grid(config.orders)
export let orderdetails = new w2grid(config.orderdetails)
export let formOrder = new w2form(config.orderForm)
