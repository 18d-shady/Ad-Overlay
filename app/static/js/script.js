function toggleOverlay() {
    const checkbox = document.querySelector('input[type="checkbox"]');
    const currentState = checkbox.checked ? 'on' : 'off';  // Determine the current state

    fetch('/toggle_overlay', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ state: currentState })  // Send the current state
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        // Optionally, you can update the UI based on the response
    });
}