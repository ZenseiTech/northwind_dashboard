import { server_url } from './server.js'

let regions = []
let categories = []
let suppliers = []
let cities = []
let countries = []

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
