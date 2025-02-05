function showScreen(screenId) {
    // Remove 'active' class from all screens
    document.querySelectorAll('.screen').forEach(screen => screen.classList.remove('active'));

    // Remove 'active' class from all tabs
    document.querySelectorAll('.tab-button').forEach(button => button.classList.remove('active'));

    // Add 'active' class to the clicked screen
    document.getElementById(screenId).classList.add('active');

    // Add 'active' class to the clicked tab (event.target refers to the clicked tab)
    event.target.classList.add('active');

    // If switching to the File Storage tab, refresh the file list
    if (screenId === 'files-screen') {
        refreshFileList();
    }
}

function refreshFileList() {
    fetch('/file-list')
        .then(response => response.json())
        .then(files => {
            let tableBody = document.querySelector('.files-table tbody');
            tableBody.innerHTML = ''; // Clear old table rows

            files.forEach(file => {
                let row = document.createElement('tr');
                row.innerHTML = `
                    <td>${file.name}</td>
                    <td>${file.size}</td>
                    <td>
                        <form action="/delete_file/${file.name}" method="post">
                            <button type="submit" class="delete-button">Delete</button>
                        </form>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching files:', error));
}

// Refresh file list every 30 seconds
setInterval(refreshFileList, 30000);
