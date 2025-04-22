import { useState } from 'react';

function VideoGenerator() {
  const [prompt, setPrompt] = useState('');
  const [videoUrl, setVideoUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const generate = async () => {
    setLoading(true);
    const res = await fetch('http://localhost:5000/generate-video', {
      method: 'POST',
      credentials: 'include',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    const data = await res.json();
    setVideoUrl(data.video_url);
    setLoading(false);
  };

  return (
    <div className="generator">
      <textarea
        rows="3"
        placeholder="Type your prompt..."
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
      />
      <button onClick={generate} disabled={loading}>
        {loading ? 'Generating...' : 'Generate Video'}
      </button>

      {videoUrl && (
        <div className="video-output">
          <video width="500" controls>
            <source src={videoUrl} type="video/mp4" />
          </video>
          <a href={videoUrl} download={videoUrl.split('/').pop()}>
            <button className="download-button">Download Video</button>
          </a>
        </div>
      )}
    </div>
  );
}

export default VideoGenerator;
