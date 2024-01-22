// Login
document.addEventListener("DOMContentLoaded", function () {
    // const redirectURI = "http://localhost:5000/callback"
    const redirectURI = "https://playlog.onrender.com/callback"

    // Login button
    document.getElementById("loginBtn").addEventListener("click", function () {
        // Define permissions
        scope = "user-read-private user-read-email user-top-read user-read-recently-played"

        // Redirect to Spotify for authorization
        const spotifyAuthUrl = "https://accounts.spotify.com/authorize";
        const params = {
            "client_id": "7351837820d04a438ea8fa4081178723",
            "response_type": "code",
            "redirect_uri": redirectURI,
            "scope": scope,
        };
        const authUrl = `${spotifyAuthUrl}?${new URLSearchParams(params)}`;

        // Redirect user to Spotify authorization page
        window.location.href = authUrl;
    });
});
