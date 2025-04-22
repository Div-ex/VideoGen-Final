import { render, screen, waitFor } from '@testing-library/react';
import HistoryPage from '../HistoryPage';

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () =>
        Promise.resolve([
          {
            prompt: 'History of AI',
            video_url: 'http://localhost:5000/videos/sample.mp4',
          },
        ]),
    })
  );
});

test('renders video history correctly', async () => {
  render(<HistoryPage />);

  await waitFor(() => {
    expect(screen.getByText(/history of ai/i)).toBeInTheDocument();
    expect(screen.getByTestId('video-player')).toBeInTheDocument();
  });
});
