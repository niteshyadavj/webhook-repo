function fetchEvents() {
    fetch('/get-events')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('events-container');
            container.innerHTML = '';  // Clear existing content
            data.forEach(event => {
                const div = document.createElement('div');
                div.className = 'event';
                div.innerHTML = `<p>${event.author} ${event.action} to ${event.to_branch} on ${event.timestamp}</p>`;
                container.appendChild(div);
            });
        })
        .catch(err => console.error('Error fetching events:', err));
}

// Fetch events on page load and every 15 seconds
fetchEvents();
setInterval(fetchEvents, 15000);
