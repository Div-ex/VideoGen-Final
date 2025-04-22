import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import VideoGenerator from '../VideoGenerator';

beforeEach(() => {
  global.fetch = jest.fn(() =>
    Promise.resolve({
      json: () => Promise.resolve({ video_url: 'http://localhost/fake.mp4' }),
    })
  );
});

test('generates video from prompt', async () => {
  render(<VideoGenerator />);
  const textarea = screen.getByPlaceholderText(/type your prompt/i);
  const button = screen.getByText(/generate video/i);

  fireEvent.change(textarea, { target: { value: 'History of AI' } });
  fireEvent.click(button);

  expect(button).toBeDisabled();

  await waitFor(() => {
    expect(screen.queryByText(/download video/i)).toBeInTheDocument();
  });
});
