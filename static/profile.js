// Temporary Logout (Not complete)
document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("logoutBtn").addEventListener("click", function () {
        // window.location.replace("http://localhost:5000/");
        window.location.replace("https://playlog.onrender.com/");
    });
});

// Set greeting
let timeOfDay = "";
const updateGreeting = () => {
    const currentHour = new Date().getHours();
    if (currentHour >= 5 && currentHour < 12) {
        timeOfDay = "morning";
    } else if (currentHour >= 12 && currentHour < 18) {
        timeOfDay = "afternoon";
    } else {
        timeOfDay = "evening";
    }
    document.getElementById("timeOfDay").innerText = timeOfDay;
};
updateGreeting();

// Changing tabs
let currTab = "topTracks";
function handleTabChange(tab) {
    // Remove active class from tab buttons
    for (const button of tabButtons) {
        button.classList.remove("active");
    }
    currTab = tab;
    renderTracks();

    // Add active class to clicked button
    document.getElementById(tab).classList.add("active");
}
const tabButtons = document.getElementsByClassName("tab");
for (const button of tabButtons) {
    button.addEventListener("click", function (event) {
        handleTabChange(event.target.id);
    });
}
// Default active tab
document.getElementById("topTracks").classList.add("active");

// Tracks
const userTimezone = new Date().getTimezoneOffset() * 60 * 1000;

function renderTracks() {
    const list = document.getElementById("tracks");
    list.innerHTML = "";

    if (currTab == "topTracks") {
        JSON.parse(topTracks).forEach((track, idx) => {
            const item = document.createElement("li");
            item.innerHTML = `
                <div class="trackLeft">
                    <span class="idx">${idx + 1}</span>
                    <img class="songImg" src="${track.image_url}"/>
                    <div class="trackInfo">
                        <span class="trackName">${track.name}</span>
                        <span class="trackArtist">${track.artist}</span>
                    </div>
                </div>
                <div class="trackRight">
                    <span>Played ${track.played_count} times</span>
                    <a target="_blank" href="${track.song_link}">
                        <img class="spotifyIcon" src="../static/spotify.png" title="Open song on Spotify"></img>
                    </a>
                </div>
                `;
            list.appendChild(item);
        });
    } else if (currTab === "topArtists") {
        JSON.parse(topArtists).forEach((artist, idx) => {
            const item = document.createElement("li");
            item.innerHTML = `
                <div class="trackLeft">
                    <span class="idx">${idx + 1}</span>
                    <img class="songImg" src="${artist.image_url}"/>
                    <div class="trackInfo">
                        <span class="trackName">${artist.name}</span>
                    </div>
                </div>
                <a target="_blank" href="${artist.artist_link}">
                    <img class="spotifyIcon" src="../static/spotify.png" title="Open artist on Spotify"></img>
                </a>
                `;
            list.appendChild(item);
        });
    } else if (currTab === "recentlyPlayed") {
        JSON.parse(recentlyPlayed).forEach((track, idx) => {
            // Adjust recently played datetime to user's timezone
            const playedDatetime = new Date(track.played_datetime);
            const userDatetime = new Date(playedDatetime.getTime() - userTimezone);
            played_date = userDatetime.toLocaleDateString("en-US");
            played_time = userDatetime.toLocaleTimeString("en-US", { hour: "numeric", minute: "numeric", hour12: true });

            const item = document.createElement("li");
            item.innerHTML = `
                <div class="trackLeft">
                    <span class="idx">${idx + 1}</span>
                    <img class="songImg" src="${track.image_url}"/>
                    <div class="trackInfo">
                        <span class="trackName">${track.name}</span>
                        <span class="trackArtist">${track.artist}</span>
                    </div>
                </div>
                <div class="trackRight">
                    <span>${played_date}, ${played_time}</span>
                    <a target="_blank" href="${track.song_link}">
                        <img class="spotifyIcon" src="../static/spotify.png" title="Open song on Spotify"></img>
                    </a>
                </div>
                `;
            list.appendChild(item);
        });
    }
}
renderTracks();
