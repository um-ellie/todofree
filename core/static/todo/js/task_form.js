// task_form.js
function getCookie(name){
    let cookieValue = null;
    document.cookie.split(';').forEach(c => {
        c = c.trim();
        if(c.startsWith(name+'=')) cookieValue = decodeURIComponent(c.slice(name.length+1));
    });
    return cookieValue;
}

// Show new category input
document.getElementById('show-add-category').addEventListener('click', () => {
    document.getElementById('new-category-wrapper').classList.remove('hidden');
    document.getElementById('new-category-input').focus();
});

// Add new category via AJAX
document.getElementById('add-category-btn').addEventListener('click', () => {
    const name = document.getElementById('new-category-input').value.trim();
    if(!name) return alert("Please enter category name.");

    fetch("/todo/category/add/", {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken'),
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name })
    })
    .then(res => res.json())
    .then(data => {
        if(data.success){
            const select = document.getElementById('category-select');
            const option = document.createElement('option');
            option.value = data.pk;
            option.textContent = data.name;
            option.selected = true;
            select.appendChild(option);

            const list = document.getElementById('category-list');
            const li = document.createElement('li');
            li.dataset.id = data.pk;
            li.className = 'flex justify-between items-center border px-2 py-1 rounded';
            li.innerHTML = `<span>${data.name}</span>
                            <button type="button" class="delete-category-btn text-red-500 hover:text-red-700 text-sm">❌</button>`;
            list.appendChild(li);
            attachDelete(li.querySelector('.delete-category-btn'));

            // Reset
            document.getElementById('new-category-input').value = '';
            document.getElementById('new-category-wrapper').classList.add('hidden');
        } else {
            alert("Error adding category.");
        }
    });
});

// Attach delete event
function attachDelete(btn){
    btn.addEventListener('click', () => {
        const li = btn.closest('li');
        const catId = li.dataset.id;
        if(!confirm('Are you sure you want to delete this category?')) return;

        fetch("/todo/category/delete/", {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ id: catId })
        })
        .then(res => res.json())
        .then(data => {
            if(data.success){
                // Remove option from select
                const select = document.getElementById('category-select');
                const option = select.querySelector(`option[value='${catId}']`);
                if(option) option.remove();
                li.remove();
            } else {
                alert(data.error || 'Error deleting category.');
            }
        });
    });
}

// Attach delete buttons initially
document.querySelectorAll('.delete-category-btn').forEach(attachDelete);
