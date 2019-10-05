/*
 * for resorting/ordering someone's list of candidates
 */
import Sortable from 'sortablejs';


window.addEventListener('DOMContentLoaded', (event) => {
    var el = document.getElementById('ranked_list');
    var sortable = Sortable.create(el, {
        sort: true,

        onUpdate: function (evt) {
            var itemEl = evt.item;  // dragged HTMLElement
            evt.to;    // target list
            evt.from;  // previous list
            console.log(evt.to);
        },

    });
});
