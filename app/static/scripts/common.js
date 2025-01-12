import { server_url } from '../scripts/server.js'

let regions = []
let categories = []

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
