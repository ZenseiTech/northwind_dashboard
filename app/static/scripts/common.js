import { server_url } from './server.js'

let regions = []
let categories = []
let suppliers = []
let cities = []
let countries = []

export function disableElement(elementId, isNotAllowed) {
    if (isNotAllowed) {
        const element = document.getElementById(elementId);
        if (element !== null) {
            const classes = 'w2ui-tb-button w2ui-eaction disabled';
            classes.split(' ').forEach(className => {
                element.classList.add(className);
            });
        }
    }
}

export function removeElement(elementId, isNotAllowed) {
    if (isNotAllowed) {
        const element = document.getElementById(elementId);
        if (element !== null) {
            element.remove();
        }
    }
}

export async function hasPermission(server_endpoint) {
    let result = ""
    await fetch(server_endpoint, {
        method: 'GET', // or 'POST', 'PUT', etc.
    })
        .then(response => {
            if (response.status === 403) {
                // throw new Error('Access forbidden - you do not have permission to access this resource');
                result = response
            }
            if (!response.ok) {
                // throw new Error(`HTTP error! status: ${response.status}`);
                result = response.status
            }
            // return response.json();
        })
        .catch(error => {
            console.error('Error:', error.message);
            if (error.message.includes('forbidden')) {
                // Handle forbidden access specifically
                // alert('You need proper permissions to access this content');
                // response = error.message
                result = 403
            } else {
                // Handle other errors
                console.log("Other error: " + error.message)
            }
        });
    return result
}

export async function getCities() {
    console.log("Calling cities ....")
    await fetch(server_url + '/shipcities')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            cities = data;
        })
    return cities
};


export async function getCountries() {
    console.log("Calling countries ....")
    await fetch(server_url + '/shipcountries')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            countries = data;
        })
    return countries
};


export async function getRegions() {
    console.log("Calling regions ....")
    await fetch(server_url + '/shipregions')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            regions = data;
        })
    return regions
};


export async function getCategories() {
    console.log("Calling categories ....")
    await fetch(server_url + '/categories')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            categories = data;
        })
    return categories
};


export async function getSuppliers() {
    console.log("Calling suppliers ....")
    await fetch(server_url + '/suppliers')
        .then((response) => {
            return response.json();
        })
        .then((data) => {
            suppliers = data;
        })
    return suppliers
};
