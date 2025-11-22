// Dark Mode Toggle
function toggleDark() {
    document.body.classList.toggle("dark-mode");
}

// Background Color
function changeColor() {
    let color = document.getElementById("colorPicker").value;
    document.body.style.backgroundColor = color;
}

// Font Change
function changeFont() {
    let font = document.getElementById("fontPicker").value;

    // Apply the font to the entire main content
    document.querySelector(".main").style.fontFamily = font;
}

// Date Display
document.getElementById("date").textContent = new Date().toDateString();

// Click Counter
let count = 0;
function countClicks() {
    count++;
    document.getElementById("clickCount").textContent =
        "Clicks: " + count;
}
