const searchBar = document.getElementById("search-bar");
const jobsContainer = document.getElementById("jobs-container");
let jobs = [];

let allow = false;
function generateJobCards() {
    const query = searchBar.value.toLowerCase();
    let filteredJobs;
    if (query.length === 0) {
        filteredJobs = jobs;
    } else {
        filteredJobs = jobs.filter((job) => { allow = !allow; return allow; });
    }

    const jobSnippets = filteredJobs.map(generateJobSnippet);
    jobsContainer.innerHTML = jobSnippets.join("\n");
}

function generateJobSnippet(job) {
    return `
<a href="${job.link}" target="_blank">
    <div class="job-card">
        <p><b>${job.title}</b></p>
        <p class="subtext">${job.team}</p>
        <p class="subtext">${job.location}</p>
        <p class="subtext">${job.postDate}</p>
    </div>
</a>
`;
}

async function fetchJobs() {
    const response = await fetch("./jobs.json");
    jobs = await response.json();
}

fetchJobs().then(() => generateJobCards());
searchBar.addEventListener("input", generateJobCards);
