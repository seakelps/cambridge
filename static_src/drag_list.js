/*
 * for resorting/ordering someone's list of candidates
 */
import Sortable from 'sortablejs';
import "core-js/stable";
import "regenerator-runtime/runtime";
import Cookies from 'js-cookie'


window.addEventListener('DOMContentLoaded', (event) => {
    var el = document.getElementById('ranked_list');
    var sortable = Sortable.create(el, {
        sort: true,

        onUpdate: async function (evt) {
            let slugs = Array.from(document.querySelectorAll('candidate')).map(x => x.dataset.slug);
            postCandidates(slugs);
        },

    });
});


async function postCandidates(candidates) {
    let form_data = new FormData();
    form_data.append('candidates', candidates.join());

    const response = await fetch('', {
        method: 'POST',
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: form_data
    });
    return await response.json();
}
