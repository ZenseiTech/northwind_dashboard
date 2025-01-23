import { server_url } from './server.js'
import { w2grid } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'

let config = {
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
        },
        toolbar: {
            items: [
                { type: 'break' },
                { type: 'button', id: 'add', text: 'Add', icon: 'w2ui-icon-plus' },
                { type: 'button', id: 'edit', text: 'Edit', icon: 'icon-pencil' },
                { type: 'spacer' },
                { type: 'button', id: 'excel', text: 'Excel', icon: 'icon-file-excel' },
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
}

export let customers = new w2grid(config.customers)
