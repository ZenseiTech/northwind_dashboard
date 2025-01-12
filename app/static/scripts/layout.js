
import { w2layout } from 'https://rawgit.com/vitmalina/w2ui/master/dist/w2ui.es6.min.js'

let pstyle = 'border: 1px solid #dfdfdf; padding: 5px; font-size:11px;';
let pstyle2 = 'border: 1px solid #dfdfdf; padding: 5px;  text-align: center;';

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
    }
}

export let layout = new w2layout(config.layout)
export let layout2 = new w2layout(config.layout2)
export let layoutProduct = new w2layout(config.layoutProduct)
