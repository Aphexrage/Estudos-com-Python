async function sendQuestion() {
    const q = document.getElementById("question").value;

    const res = await fetch("http://localhost:8000/pergunta", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question: q })
    });

    const data = await res.json();
    document.getElementById("answer").innerText = data.answer;
}
