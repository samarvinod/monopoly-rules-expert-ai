async function askQuestion() {
  const questionInput = document.getElementById('question');
  const answerBox = document.getElementById('answer');
  const askBtn = document.getElementById('askBtn');
  const question = questionInput.value.trim();
  if (!question) return;
  askBtn.disabled = true;
  answerBox.innerHTML = 'Thinking...';
  try {
    const res = await fetch('http://localhost:8000/ask', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question })
    });
    if (!res.ok) throw new Error('Backend error');
    const data = await res.json();
    answerBox.innerHTML = `<span class="label">Answer:</span><br>${data.answer}`;
  } catch (e) {
    answerBox.innerHTML = 'Error: Could not reach backend.';
  }
  askBtn.disabled = false;
}
document.getElementById('question').addEventListener('keydown', function(e) {
  if (e.key === 'Enter') askQuestion();
}); 
