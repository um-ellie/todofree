document.addEventListener('DOMContentLoaded', () => {
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            document.cookie.split(';').forEach(c => {
                c = c.trim();
                if (c.startsWith(name + '=')) cookieValue = decodeURIComponent(c.slice(name.length + 1));
            });
        }
        return cookieValue;
    }
    const csrftoken = getCookie('csrftoken');

    const taskList = document.getElementById('task-list');

    // Toggle task done
    taskList.querySelectorAll('.toggle-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const url = btn.dataset.url;
            const taskId = btn.dataset.task;

            fetch(url, {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    const taskLi = document.getElementById(`task-${taskId}`);
                    const icon = taskLi.querySelector('.toggle-icon');
                    const title = taskLi.querySelector('.task-title');

                    if(data.is_done){
                        icon.textContent = "✔";
                        taskLi.classList.add('done');
                        title.classList.add('line-through', 'text-gray-400', 'text-1xl');
                    } else {
                        icon.textContent = "○";
                        taskLi.classList.remove('done');
                        title.classList.remove('line-through', 'text-gray-400', 'text-5xl');
                    }

                    // Move done tasks to bottom
                    taskList.appendChild(taskLi);
                } else {
                    alert("Error toggling task!");
                }
            });
        });
    });

    // Delete task
    taskList.querySelectorAll('.delete-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            if(!confirm("Are you sure you want to delete this task?")) return;

            const url = btn.dataset.url;
            const taskId = btn.dataset.task;

            fetch(url, {
                method: 'POST',
                headers: {'X-CSRFToken': csrftoken},
            })
            .then(res => res.json())
            .then(data => {
                if(data.success){
                    const taskLi = document.getElementById(`task-${taskId}`);
                    taskLi.remove();
                } else {
                    alert("Error deleting task!");
                }
            });
        });
    });
});
