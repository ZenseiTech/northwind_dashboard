import { w2grid, w2form, w2popup, w2field, query } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'
import { server_url } from './server.js'
import { layout2, layoutProduct } from './layout.js'
import { getRegions, getCategories, getSuppliers } from './common.js'

new w2field('money', { el: query('#us-money')[0] })

let suppliers = await getSuppliers()
let regions = await getRegions()
let categories = await getCategories()

function openPopup() {
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


let config = {
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
            { field: 'recid', text: 'Id', size: '80px', searchable: true, sortable: true, frozen: true },
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
                html: { label: 'Supplier', attr: 'style="width: 400px"' },
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
}

export let product_details = new w2grid(config.product_details)
export let formProduct = new w2form(config.productForm)
