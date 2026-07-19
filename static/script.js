let votesLeft = 100000;
let spainVotes = 0;
let argVotes = 0;

let selectedTeam = null;

function updatePollBar() {
    const total = spainVotes + argVotes;

    let spainPercent = 50;
    let argPercent = 50;

    if (total > 0) {
        spainPercent = (spainVotes / total) * 100;
        argPercent = (argVotes / total) * 100;
    }

    document.getElementById("spainSide").style.width = spainPercent + "%";
    document.getElementById("argSide").style.width = argPercent + "%";

    document.getElementById("spainPercent").textContent =
        Math.round(spainPercent) + "%";

    document.getElementById("argPercent").textContent =
        Math.round(argPercent) + "%";
}

async function vote(team) {

    const response = await fetch("/vote", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ team })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.error);
        return;
    }

    spainVotes = data.spainVotes;
    argVotes = data.argVotes;
    votesLeft = data.votesLeft;

    document.getElementById("spainVotes").textContent = spainVotes;
    document.getElementById("argVotes").textContent = argVotes;
    document.getElementById("votesLeft").textContent = votesLeft;

    updatePollBar();
}