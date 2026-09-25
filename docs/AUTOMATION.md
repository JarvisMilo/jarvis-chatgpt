# Automation Architecture

Automation is distinct from reactive conversation. It owns scheduled jobs, recurring workflows, background tasks, reminders and notifications.

A background Task has an ID, objective, priority, state, owner agent(s), dependencies, progress, timestamps, cancellation token, retry policy, logs and result/verification record.

Scheduler and NotificationManager are future Level 5 contracts. Background work must respect the same policy and permission gates as foreground work.
