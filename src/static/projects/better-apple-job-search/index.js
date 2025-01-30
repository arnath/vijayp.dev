const jobsContainer = document.getElementById("jobs-container");

function addJobCard(job) {
    jobsContainer.insertAdjacentHTML('beforeend', `
<a href="${job.link}" target="_blank">
    <div class="job-card">
        <p><b>${job.title}</b></p>
        <p class="subtext">${job.team}</p>
        <p class="subtext">${job.location}</p>
        <p class="subtext">${job.postDate}</p>
    </div>
</a>
`
    );
}

async function fetchJobs() {
    const response = await fetch("./jobs.json");
    const json = await response.json();

    return json;
}

const jobs = fetchJobs();
