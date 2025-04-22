import { useEffect, useState } from 'react';

function HistoryPage() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    fetch('http://localhost:5000/my-history', { credentials: 'include' })
      .then(res => res.json())
      .then(data => setHistory(data));
  }, []);

  return (
    <div className="history">
      <h2>Your Past Videos</h2>
      {history.length === 0 ? (
        <p>No videos yet.</p>
      ) : (
        history.map((item, i) => (
          <div key={i} className="video-card">
            <p><strong>Prompt:</strong> {item.prompt}</p>
            <video width="500" controls data-testid="video-player">
              <source src={item.video_url} type="video/mp4" />
            </video>
            <a href={item.video_url} download={item.video_url.split('/').pop()}>
              <button className="download-button">Download</button>
            </a>
          </div>
        ))
      )}
    </div>
  );
}

export default HistoryPage;
