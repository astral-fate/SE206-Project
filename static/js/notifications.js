document.addEventListener('DOMContentLoaded', function() {
    // Notifications Toggle
    const notificationBtn = document.getElementById('notification-btn');
    const notificationsPanel = document.getElementById('notifications-panel');
    const markAllReadBtn = document.getElementById('mark-all-read'); // Moved definition here
    const notificationBadge = document.getElementById('notification-badge'); // Get badge element

    if (notificationBtn && notificationsPanel) {
        // Toggle notifications panel when bell icon is clicked
        notificationBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            const isHidden = notificationsPanel.classList.toggle('hidden');

            // If opening the panel, potentially trigger position adjustment (handled in dashboard-notifications.js)
            if (!isHidden) {
                console.log('Notifications panel opened');
                // Optional: Mark as read on open (or keep server-side logic)
            }
        });

        // Close panel when clicking outside
        document.addEventListener('click', function(e) {
            // Check if the click is outside the panel AND outside the button
            if (!notificationsPanel.contains(e.target) && e.target !== notificationBtn && !notificationBtn.contains(e.target)) {
                notificationsPanel.classList.add('hidden');
            }
        });

        // Mark all notifications as read
        if (markAllReadBtn) { // Check if the button exists
            markAllReadBtn.addEventListener('click', function() {
                fetch('/mark_notifications_read', {
                    method: 'POST',
                    headers: {
                        'X-Requested-With': 'XMLHttpRequest',
                        // Ensure CSRF token is included if needed by your backend setup
                        'X-CSRFToken': document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || ''
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Update UI: remove 'unread' class from items and hide badge
                        document.querySelectorAll('.notification-item.unread').forEach(item => {
                            item.classList.remove('unread');
                        });
                        if (notificationBadge) { // Check if badge exists
                            notificationBadge.style.display = 'none'; // Hide badge
                        }
                        // Optionally update the count visually if needed, though hiding is usually sufficient
                    } else {
                        console.error('Failed to mark notifications as read:', data.message);
                    }
                })
                .catch(error => console.error('Error marking notifications as read:', error));
            });
        } else {
            console.warn('Mark all read button not found.');
        }
    } else {
        console.warn('Notification button or panel not found.');
    }
});
