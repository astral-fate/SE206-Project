document.addEventListener('DOMContentLoaded', function() {
    // Function to adjust notification panel position if it overflows the viewport
    function adjustNotificationPanelPosition() {
        const notificationsPanel = document.querySelector('.notifications-panel:not(.hidden)');
        if (!notificationsPanel) return;

        const rect = notificationsPanel.getBoundingClientRect();
        const viewportWidth = window.innerWidth;

        // Reset position first
        notificationsPanel.style.left = 'auto';
        notificationsPanel.style.right = '0'; // Default position

        // Recalculate rect after reset
        const currentRect = notificationsPanel.getBoundingClientRect();

        // Check right overflow
        if (currentRect.right > viewportWidth) {
            const overflow = currentRect.right - viewportWidth;
            // Move panel left by the overflow amount plus some padding
            notificationsPanel.style.right = `${overflow + 10}px`;
            notificationsPanel.style.left = 'auto';
        }

        // Check left overflow (might happen on very small screens or if right adjustment pushes it too far)
        if (currentRect.left < 0) {
            notificationsPanel.style.left = '10px'; // Position with padding from left edge
            notificationsPanel.style.right = 'auto';
        }
    }

    // Call this function whenever the notification panel is shown
    const notificationBtn = document.getElementById('notification-btn');
    if (notificationBtn) {
        notificationBtn.addEventListener('click', function() {
            // Use setTimeout to allow the panel to become visible before calculating position
            setTimeout(adjustNotificationPanelPosition, 10);
        });
    }

    // Adjust on window resize
    window.addEventListener('resize', function() {
        // Adjust only if the panel is currently visible
        const notificationsPanel = document.querySelector('.notifications-panel:not(.hidden)');
        if (notificationsPanel) {
            adjustNotificationPanelPosition();
        }
    });

    // ...existing code...
});
