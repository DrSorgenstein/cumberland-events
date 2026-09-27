# Cumberland County Events

Free, open source community events calendar for Cumberland County, Pennsylvania. Static HTML/CSS/JavaScript runs on GitHub Pages with no paid service or API key. Published event records are held in `data/events.json`.

## Publish your own copy

1. Create a **public** GitHub repository named `cumberland-events` and upload all files, including `.github`.
2. Set `OWNER` in `config.js` to your GitHub username; if the repository has another name, change `REPO` too. Commit the change.
3. Under **Settings → Pages**, select **Deploy from a branch**, your default branch, and **/(root)**. GitHub displays the published URL, usually `https://USERNAME.github.io/cumberland-events/`.
4. Keep the repository’s default workflow permission at **Read repository contents and packages**. The approval workflow requests `contents: write` for its own run. Issues are enabled under **Settings → General → Features**. If branch protection restricts Actions pushes, allow the workflow’s push or use a separate approval process.
5. Create repository labels `event-submission` and `approved-event` if GitHub has not created them when the first issue is submitted.

## Submission and moderation

Visitors click **Submit an event** and fill out a GitHub Issue form. They need a free GitHub account. The event is not published on submission. A repository maintainer checks the link, date, location, consent, and content and then applies the `approved-event` label. The workflow validates fields and writes the event to `data/events.json`; GitHub Pages republishes the updated site. If validation fails, the maintainer can correct the issue and remove/reapply the label. Note: labels are public, and the workflow can only trigger on a newly applied label. To remove an event, delete its record from JSON and commit. To edit a published event, correct the issue and remove/reapply the approval label.

A malicious or misleading public URL is possible even after automatic validation, so review every link before approval. Issue contents are public from submission onward. Ask submitters not to post personal data. To reduce spam, use GitHub moderation tools. Publishing all event information happens only after maintainer approval.

## Calendar support

Each card offers a Google Calendar link, an Outlook web link, and a downloadable `.ics` file for Apple Calendar, Outlook desktop, and other compatible apps. Times are entered as local Eastern Time. The app converts them using `America/New_York`, including daylight saving transitions. Imported calendars will use the user's own display timezone.

## Development

Run `python3 -m http.server 8000` in the repository and open `http://localhost:8000`. JavaScript uses ES modules, so opening `index.html` directly as a file will not work. No build or dependencies are required.

## License

MIT; see `LICENSE`. Submitted event details remain subject to their respective owners' rights. This repository's code license does not grant permission to reproduce third-party logos, images, or descriptions.
