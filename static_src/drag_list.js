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
        handle: ".handle",

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


$('.toggle-comment-form, .update_note [name=cancel]').on('click', function(event) {
    let candidate = event.target.closest("candidate")

    let stored_comment = candidate.querySelector(".stored_comment");
    let comment_form = candidate.querySelector(".update_note");

    stored_comment.classList.toggle('d-block');
    stored_comment.classList.toggle('d-none');

    comment_form.classList.toggle('d-none');
    comment_form.classList.toggle('d-block');
});


$('.update_note').on('submit', function(event) {
    event.preventDefault();
    let comment_form = event.currentTarget;
    let form_data = new FormData(comment_form);

    const response = fetch(comment_form.action, {
        method: comment_form.method,
        credentials: 'same-origin',
        headers: {
            'X-CSRFToken': Cookies.get('csrftoken'),
            'X-Requested-With': 'XMLHttpRequest'
        },
        body: form_data
    });

    let stored_comment = comment_form.closest("candidate").querySelector(".stored_comment");
    stored_comment.classList.add('d-block');
    stored_comment.classList.remove('d-none');
    stored_comment.innerText = form_data.get('comment');

    comment_form.classList.add('d-none');
    comment_form.classList.remove('d-block');
});
