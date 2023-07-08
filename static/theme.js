// theme.js

function saveThemePreference(theme) {
	localStorage.setItem("themePreference", theme);
}

function loadThemePreference() {
	var themePreference = localStorage.getItem("themePreference");
	var theme = document.getElementsByTagName("link")[0];

	if (themePreference === "dark") {
		theme.setAttribute("href", "/static/dark.css");
	} else {
		theme.setAttribute("href", "/static/light.css");
	}
}

function toggleTheme() {
	var theme = document.getElementsByTagName("link")[0];

	if (theme.getAttribute("href") === "/static/light.css") {
		theme.setAttribute("href", "/static/dark.css");
		saveThemePreference("dark");
	} else {
		theme.setAttribute("href", "/static/light.css");
		saveThemePreference("light");
	}
}

loadThemePreference();

// Przypisanie funkcji toggleTheme() do przycisku
var button = document.getElementById("myButton");
button.addEventListener("click", toggleTheme);
